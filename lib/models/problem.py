# -*- coding: utf-8 -*-

from centipede import db

class Contest(db.Model):

    __tablename__ = u'contests'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    problems = db.relationship('Problem', backref = 'contest')

class Problem(db.Model):

    __tablename__ = u'problems'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    input = db.Column(db.String)
    output = db.Column(db.String)
    time = db.Column(db.Integer, default = 1)
    memory = db.Column(db.Integer, default = 64)
    hint = db.Column(db.String)

    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'), default = None)

    examples = db.relationship('Example')
    tests = db.relationship('Test')

class Example(db.Model):

    __tablename__ = u'examples'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    input = db.Column(db.Text)
    output = db.Column(db.Text)

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))

class Test(db.Model):

    __tablename__ = u'tests'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    input = db.Column(db.Text)
    output = db.Column(db.Text)

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))