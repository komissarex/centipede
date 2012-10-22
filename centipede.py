# -*- coding: utf-8 -*- 

from flask import Flask, request, redirect, url_for, session, flash
from flask.templating import render_template
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy
from hashlib import md5
import time, datetime 

centipede = Flask(__name__)
centipede.config.from_pyfile('configuration.py')
centipede.secret_key = centipede.config['SECRET']

db = SQLAlchemy(centipede)

def time_counter():
    start = time.mktime(time.strptime(centipede.config['START_TIME'], '%Y-%m-%d %H:%M:%S'))
    diff = datetime.datetime.fromtimestamp(start) - datetime.datetime.now()
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

@centipede.route('/')
def index():
    return render_template('index.html', counter = time_counter())

@centipede.route('/registration', methods = ['GET', 'POST'])
def register():
    from forms.registration import RegistrationForm
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        from models import Team
        team = Team(form.team_name.data, form.institution.data, form.team_members.data, md5(form.password.data).hexdigest())
        db.session.add(team)
        try:
            db.session.flush()
        except:
            form.team_name.errors.append(u'Команда с таким названием уже зарегистрирована.')
        else:
            team.generate_team_id()
            db.session.commit()
            session['team_id'] = team.team_id
            return render_template('registration_success.html', team_id = team.team_id, active_register = True)
    return render_template('registration.html', form = form, active_registration = True)

@centipede.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        from models import Team
        if Team.query.filter_by(team_id = request.form['team_id'], password = md5(request.form['password']).hexdigest()).first():
            session['team_id'] = request.form['team_id']
            flash(u'Вход в систему выполнен успешно', 'alert-success')
            return redirect(url_for('index'))
        else:
            flash(u'Команда с таким TEAM_ID и паролем не найдена.', 'alert-error')
            return redirect(url_for('login'))
    return render_template('login.html')

@centipede.route('/logout')
def logout():
    session.pop('team_id', None)
    flash(u'Вы вышли из системы', 'alert-success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    centipede.run(host = 'localhost', port = 8080, debug = True)