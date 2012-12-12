# -*- coding: utf-8 -*-

from lib.database import Base
from sqlalchemy import Column, Integer, String, Text


class Team(Base):

    __tablename__ = u'teams'

    id = Column(Integer, primary_key = True, autoincrement = True)
    team_id = Column(String(50), unique = True)
    name = Column(String(50), unique = True)
    institution = Column(String(50))
    members = Column(Text)
    password = Column(String(50))

    def generate_team_id(self):
        """
        Generate an unique TEAM_ID for team login
        (something like "57001ABC")
        """
        import random, string
        self.team_id = '%05d%s' % (self.id + 0xDEAD,
                                   ''.join(random.choice(string.uppercase.replace('0', '')) for x in range(3)))

    def __init__(self, name, institution, members, password):
        self.password = password
        self.name = name
        self.institution = institution
        self.members = members


