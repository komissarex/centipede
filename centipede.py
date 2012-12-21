# -*- coding: utf-8 -*- 

from flask import Flask, request, redirect, url_for, session, flash, abort
from flask.templating import render_template
from threading import BoundedSemaphore
from hashlib import md5
from importlib import import_module

from lib.stuff import *

centipede = Flask(__name__)
centipede.config.from_pyfile('config.py')
centipede.secret_key = centipede.config['SECRET']

global tester_semaphore
tester_semaphore = BoundedSemaphore(centipede.config['SAME_TIME_THREADS'])

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
        if Team.query.filter_by(team_id = request.form['team_id'].encode("utf-8"),
                                password = md5(request.form['password'].encode("utf-8")).hexdigest()).first():
            session['team_id'] = request.form['team_id']
            flash(u'Вход в систему выполнен успешно', 'alert-success')
            return redirect(url_for('index'))
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

@centipede.route('/problem/<int:id>')
def problem(id):
    """
    View a single problem
    :param id: Problem id
    """
    from models import Problem
    problem = Problem.query.get(id) or abort(404)
    return render_template('problem.html', problem = problem)

@centipede.route('/problemset/', defaults = {'page': 1})
@centipede.route('/problemset/page/<int:page>')
def problemset(page):
    """
    Problems list
    """
    from models import Problem, Solution
    from lib.database import db_session
    from lib.pagination import Pagination

    per_page = centipede.config['PER_PAGE']
    total = Problem.query.count()
    problems = db_session.query(Problem.id, Problem.title).order_by(Problem.id).\
        limit(per_page).offset((page - 1) * per_page).all()
    pagination = Pagination(page, per_page, total)

    for problem in problems:
        problem.total = Solution.query.filter_by(problem_id = problem.id).count()
        problem.success = Solution.query.filter_by(
            problem_id = problem.id,
            status = Solution.STATUS['tested']['accept']
        ).count()
    return render_template('problemset.html', problems = problems, active_problems = True, pagination = pagination)

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


            tester_module = import_module('lib.testers.{tester_name}'.format(tester_name = solution.language.tester_name))
            tester = tester_module.Tester(solution, tester_semaphore)
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
    flash(u'Размер файла превышает 256 КБ!', 'alert-error')
    return redirect(request.referrer)

@centipede.route('/status/', defaults = {'page': 1})
@centipede.route('/status/page/<int:page>')
def status(page):
    """
    Status page for monitoring submitted solutions
    """
    from models import Solution
    from sqlalchemy import desc
    from lib.pagination import Pagination

    if 'team_id' in session:
        per_page = centipede.config['PER_PAGE']
        total = Solution.query.filter_by(team_id = session['team_id']).count()
        solutions = Solution.query.filter_by(team_id = session['team_id']).order_by(desc(Solution.id)).\
                    limit(per_page).offset((page - 1) * per_page).all()
        pagination = Pagination(page, per_page, total)
        return render_template('status.html', active_status = True, solutions = solutions, pagination = pagination)
    else:
        return redirect(url_for('index'))

@centipede.route('/solution/<int:id>')
def solution(id):
    """
    Get solution source
    :param id: Solution ID
    """
    from models import Solution
    solution = Solution.query.get(id) or abort(404)
    if session['team_id'] == solution.team_id:
        try:
            content = file(solution.get_solution_file()).read().encode("utf-8")
        except UnicodeDecodeError:
            content = 'INCORRECT FILE'
        return render_template('get_solution.html', content = content, solution = solution)

@centipede.route('/help/about/')
def about():
    """
    Help page
    """
    return render_template('help/about.html')

@centipede.errorhandler(404)
def page_not_found(error):
    """ 404 error handler """
    return render_template('page_not_found.html', referrer = request.referrer), 404

def url_for_other_page(page):
    """
    Pagination helper for Jinja
    """
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
centipede.jinja_env.globals['url_for_other_page'] = url_for_other_page

# development web server starting
if __name__ == '__main__':
    centipede.wsgi_app = StreamConsumingMiddleware(centipede.wsgi_app) # fix for connection reset on big files upload
    centipede.run(host = "localhost", port = 8080, debug = True)