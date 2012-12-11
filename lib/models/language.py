# -*- coding: utf-8 -*-

from centipede import db

class Language(db.Model):
    """
    Available rogramming languages
    """

    __tablename__ = u'languages'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    file_ext = db.Column(db.String(10), unique = True) # language file extension
    name = db.Column(db.String(50))
    tester_name = db.Column(db.String(20)) # name for tester module

