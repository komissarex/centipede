"""
SQLAlchemy init
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from centipede import centipede


engine = create_engine(centipede.config['DATABASE_URI'], convert_unicode = True)

db_session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine,
        expire_on_commit = False
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

def db_init():
    """
    Database initialization script
    """
    import models
    Base.metadata.create_all(bind = engine)