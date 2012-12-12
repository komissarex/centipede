"""
Some stuff needed by application
"""

import time, datetime, os
from werkzeug.wsgi import LimitedStream

def time_counter(start_time):
    """
    How much time before the nearest contest?
    :param start_time: Contest starting time
    :return: Time string
    """
    start = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
    diff = datetime.datetime.fromtimestamp(start) - datetime.datetime.now()
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

def get_lang_id(file):
    """
    File extension validator and identificator
    :param file: Input file
    :return: Language ID, if extension is valid, or None.
    """
    from lib.database import db_session
    from models import Language
    filename, ext = os.path.splitext(file)
    return db_session.query(Language.id).filter_by(file_ext = ext).first()


class StreamConsumingMiddleware(object):
    """
    Hook to fix Flask's dev server connection reset on big file submits
    More info at http://flask.pocoo.org/snippets/47/
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        stream = LimitedStream(environ['wsgi.input'],
            int(environ['CONTENT_LENGTH'] or 0))
        environ['wsgi.input'] = stream
        app_iter = self.app(environ, start_response)
        try:
            stream.exhaust()
            for event in app_iter:
                yield event
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
