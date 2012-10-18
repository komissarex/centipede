# -*- coding: utf-8 -*- 

from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from forms.registration import RegistrationForm
from flask.ext.sqlalchemy import SQLAlchemy

import time, datetime 

centipede = Flask(__name__)
centipede.config.from_pyfile('configuration.py')
centipede.secret_key = centipede.config['SECRET']

centipede.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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

@centipede.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('register/success'))
    return render_template('register.html', form = form)

@centipede.route('/register/success', methods=['GET', 'POST'])
def register_success():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

if __name__ == '__main__':
    centipede.run(host = 'localhost', port = 8080, debug = True)