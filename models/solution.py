# -*- coding: utf-8 -*-

from lib.database import Base, db_session
from sqlalchemy import *
from lib.stuff import *
from sqlalchemy.orm import relationship

class Solution(Base):

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

    id = Column(Integer, primary_key = True, autoincrement = True)
    submitted = Column(TIMESTAMP, default = func.current_timestamp())
    time = Column(Integer)
    memory = Column(Integer)
    status = Column(String)
    message = Column(Text)

    problem_id = Column(Integer, ForeignKey('problems.id'))
    lang_id = Column(Integer, ForeignKey('languages.id'))
    team_id = Column(String, ForeignKey('teams.team_id'))

    problem = relationship('Problem', backref = 'solutions')
    language = relationship('Language')

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
        db_session.merge(self)
        db_session.commit()

    def update_message(self,message):
        self.message = message
        db_session.merge(self)
        db_session.commit()

    def __init__(self, problem_id, team_id, lang_id):
        self.problem_id = problem_id
        self.team_id = team_id
        self.lang_id = lang_id
        self.status = self.STATUS['waiting']['queue']



