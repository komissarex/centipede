# -*- coding: utf-8 -*-

from lib.database import Base
from sqlalchemy import Column, Integer, String

class Language(Base):
    """
    Available programming languages
    """

    __tablename__ = u'languages'

    id = Column(Integer, primary_key = True, autoincrement = True)
    file_ext = Column(String(10), unique = True) # language file extension
    name = Column(String(50))
    tester_name = Column(String(20)) # name for tester module

