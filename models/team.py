# -*- coding: utf-8 -*-

from centipede import db

class Team(db.Model):

    __tablename__ = u'teams'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_id = db.Column(db.String(50), unique = True)
    team_name = db.Column(db.String(50), unique = True)
    institution = db.Column(db.String(50))
    team_members = db.Column(db.Text)
    password = db.Column(db.String(50))

    def generate_team_id(self):
        import random, string
        self.team_id = '%05d%s' % (self.id + 0xDEAD, ''.join(random.choice(string.uppercase.replace('0', '')) for x in range(3)))

    def __init__(self, team_name, institution, team_members, password):
        self.password = password
        self.team_name = team_name
        self.institution = institution
        self.team_members = team_members


