# centipede

A simple python-based test system for ACM-ICPC-like programming contests, started as university course work.

Current state: *unfinished* and *unmaintained*, so it must be considered just as some old Flask + sqlalchemy + other Python stuff training.

## installation
```
 # pip install virtualenv
 $ mkdir centipede
 $ cp -r /path_you_download_it/* ./centipede
 $ cd centipede
 $ virtualenv .env
 $ . .env/bin/activate
 $ pip install -r requirements.pip
```

## database init
```
 $ cd centipede
 $ . .env/bin/activate
 $ python
 >>> from lib.database import init_db
 >>> db_init()
```

## running
```
 $ cd centipede
 $ . .env/bin/activate
 $ python centipede.py
```

## configuration
All configuration is laid in config.py, which is pretty well commented.
