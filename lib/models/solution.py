# -*- coding: utf-8 -*-

from centipede import db
from lib.stuff import *

class Solution(db.Model):

    __tablename__ = u'solutions'

    # solutions statuses
    STATUS = {
        'accept': 'Accept',
        'error': {
            'ce': 'Compilation Error',
            'wa': 'Wrong Answer',
            'crash': 'Crash!',
            'tle': 'Time Limit Exceed',
            'mle': 'Memory Limit Exceed',
        },
        'waiting': {
            'compiling': 'Compiling...',
            'running': 'Running...',
            'queue': 'Waiting in queue...'
        }
    }

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    submitted = db.Column(db.TIMESTAMP, default = db.func.current_timestamp())
    time = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    status = db.Column(db.String)
    message = db.Column(db.Text)

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    lang_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    team_id = db.Column(db.String, db.ForeignKey('teams.team_id'))

    problem = db.relationship('Problem', backref = 'solutions')
    language = db.relationship('Language')

    def get_solution_path(self):
        """
        :return: Path to the solution file (without filename)
        """
        from centipede import centipede
        return os.path.join(centipede.config['SOLUTIONS_FOLDER'], str(self.team_id), str(self.problem_id))

    def get_solution_file(self):
        """
        :return: Full solution path with filename
        """
        filename = str(self.id) + self.language.file_ext
        return os.path.join(self.get_solution_path(), filename)

    def get_solution_tester(self):
        """
        :return: Tester instance for current solution
        """
        pass

    def update_status(self, status):
        self.status = status
        db.session.merge(self)
        db.session.commit()

    def update_message(self,message):
        self.message = message
        db.session.merge(self)
        db.session.commit()

    def __init__(self, problem_id, team_id, lang_id):
        self.problem_id = problem_id
        self.team_id = team_id
        self.lang_id = lang_id
        self.status = self.STATUS['waiting']['queue']



