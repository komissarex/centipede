# -*- coding: utf-8 -*- 

from flask import Flask, request, redirect, url_for, session, flash, abort
from flask.templating import render_template
from hashlib import md5

from lib.stuff import *

centipede = Flask(__name__)
centipede.config.from_pyfile('config.py')
centipede.secret_key = centipede.config['SECRET']

@centipede.route('/')
def index():
    return render_template('index.html')

@centipede.route('/registration', methods = ['GET', 'POST'])
def register():
    """
    Registration form
    """
    from lib.forms.registration import RegistrationForm
    from lib.database import db_session
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        from models import Team
        team = Team(form.team_name.data, form.institution.data,
                    form.team_members.data, md5(form.password.data).hexdigest())
        db_session.add(team)
        # trying to add to db
        try:
            db_session.flush()
        except:
            form.team_name.errors.append(u'Команда с таким названием уже зарегистрирована.')
        else:
            # if success, generate TEAM_ID
            team.generate_team_id()
            db_session.commit()
            # store session
            session['team_id'] = team.team_id
            return render_template('registration_success.html', team_id = team.team_id, active_register = True)
    return render_template('registration.html', form = form, active_registration = True)

@centipede.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Login form
    """
    if request.method == 'POST':
        from models import Team
        from lib.database import db_session
        if Team.query.filter_by(team_id = request.form['team_id'],
                                password = md5(request.form['password']).hexdigest()).first():
            session['team_id'] = request.form['team_id']
            flash(u'Вход в систему выполнен успешно', 'alert-success')
            return redirect(request.referrer)
        else:
            flash(u'Команда с таким TEAM_ID и паролем не найдена.', 'alert-error')
            return redirect(url_for('login'))
    return render_template('login.html')

@centipede.route('/logout')
def logout():
    """
    Logout action
    """
    session.pop('team_id', None)
    flash(u'Вы вышли из системы', 'alert-success')
    return redirect(url_for('index'))

@centipede.route('/problems')
def problems():
    """
    Problems list
    """
    from models import Problem
    from lib.database import db_session
    problems = db_session.query(Problem.id, Problem.title).order_by(Problem.id).all()
    return render_template('problems.html', problems = problems, active_problems = True)

@centipede.route('/problems/<int:id>')
def problem_view(id):
    """
    View a single problem
    :param id: Problem id
    """
    from models import Problem
    problem = Problem.query.get(id) or abort(404)
    return render_template('problem_view.html', problem = problem)

@centipede.route('/submit', methods = ['GET', 'POST'])
def submit():
    """
    Action for solution submit
    """
    if request.method == 'POST':
        from models import Solution
        from lib.database import db_session
        file = request.files['file']
        if not file:
            flash(u'Эмм, может стоит таки приложить решение?', 'alert-error')
            return redirect(request.referrer)
        lang_id = get_lang_id(file.filename)
        if lang_id:
            # Create solution in database
            team_id = session['team_id']
            problem_id = request.form['problem_id']
            solution = Solution(problem_id, team_id, lang_id)
            db_session.add(solution)
            db_session.commit()

            # Store solution file
            path = solution.get_solution_path()
            solution_file = solution.get_solution_file()
            if not os.path.exists(path):
                os.makedirs(path)
            file.save(solution_file)

            from lib.testers import c
            tester = c.CTester(solution)
            tester.start()

        else:
            flash(u'Неверное расширение файла!', 'alert-error')
            return redirect(request.referrer)
    return redirect(url_for('status'))

@centipede.errorhandler(413)
def big_file_error_handler(e):
    """
    Error handler for RequestEntityTooLarge exception,
    which raises for upload some big files
    """
    flash(u'Размер файла превышает 2 МБ!', 'alert-error')
    return redirect(request.referrer)

@centipede.route('/status')
def status():
    """
    Status page for monitoring submitted solutions
    """
    from models import Solution
    from sqlalchemy import desc
    solutions = Solution.query.filter_by(team_id = session['team_id']).order_by(desc(Solution.id)).all()
    return render_template('status.html', active_status = True, solutions = solutions)

@centipede.route('/solution/<int:id>')
def solution(id):
    """
    Get solution source
    :param id: Solution ID
    """
    from models import Solution
    solution = Solution.query.get(id) or abort(404)
    if session['team_id'] == solution.team_id:
        content = file(solution.get_solution_file()).read()
        return render_template('get_solution.html', content = content, solution = solution)

if __name__ == '__main__':
    centipede.wsgi_app = StreamConsumingMiddleware(centipede.wsgi_app) # fix for connection reset on big files upload
    # development web server start
    centipede.run(host = "localhost", port = 8080, debug = True)