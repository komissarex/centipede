# -*- coding: utf-8 -*-

from lib.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Contest(Base):

    __tablename__ = u'contests'

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(100))
    description = Column(Text)
    start = Column(DateTime)
    end = Column(DateTime)

    problems = relationship('Problem', backref = 'contest')

class Problem(Base):

    __tablename__ = u'problems'

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(100))
    content = Column(String)
    input = Column(String)
    output = Column(String)
    time = Column(Integer, default = 1)
    memory = Column(Integer, default = 64)
    hint = Column(String)

    contest_id = Column(Integer, ForeignKey('contests.id'), default = None)

    examples = relationship('Example')
    tests = relationship('Test')

class Example(Base):

    __tablename__ = u'examples'

    id = Column(Integer, primary_key = True, autoincrement = True)
    input = Column(Text)
    output = Column(Text)

    problem_id = Column(Integer, ForeignKey('problems.id'))

class Test(Base):

    __tablename__ = u'tests'

    id = Column(Integer, primary_key = True, autoincrement = True)
    input = Column(Text)
    output = Column(Text)

    problem_id = Column(Integer, ForeignKey('problems.id'))