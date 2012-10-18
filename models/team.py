from centipede import Base

from sqlalchemy import Column, Integer, String, Text


class Team(Base):
    
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key = True)
    contest_id = Column(String(50))
    password = Column(String(50))
    team_name = Column(String(50), unique = True)
    institution = Column(String(50))
    team_members = Column(Text)

    def __init__(self, contest_id, password, team_name, institution, team_members):
        self.contest_id = contest_id
        self.password = password
        self.team_name = team_name
        self.institution = institution
        self.team_members = team_members


