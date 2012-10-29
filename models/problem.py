# -*- coding: utf-8 -*-

from centipede import db

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

    examples = db.relationship('Example', backref = 'problem', lazy = 'dynamic')

class Example(db.Model):

    __tablename__ = u'examples'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    input = db.Column(db.String)
    output = db.Column(db.String)

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
