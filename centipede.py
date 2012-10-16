# -*- coding: utf-8 -*- 

from flask import Flask
from flask.templating import render_template
import time, datetime 

import configuration

centipede = Flask(__name__)
centipede.config.from_object(configuration.Init)

def time_counter(timedelta):
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%s ч. %s мин. %s сек.' % (hours, minutes, seconds)

@centipede.route('/')
def index():
    start = time.mktime(time.strptime(centipede.config['START_TIME'], '%Y-%m-%d %H:%M:%S'))
    diff = datetime.datetime.fromtimestamp(start) - datetime.datetime.now()
    return render_template('index.html', counter = time_counter(diff))

if __name__ == '__main__':
    centipede.run(host = 'localhost', port = 8080, debug = True)