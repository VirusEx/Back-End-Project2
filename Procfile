# users: sandman2ctl -p $PORT sqlite+pysqlite:///users.db
# timelines: sandman2ctl -p $PORT sqlite+pysqlite:///timelines.db
# user-queries: datasette -p $PORT --reload users.db
# timeline-queries: datasette -p $PORT --reload timelines.db

users: gunicorn --access-logfile - --capture-output users:__hug_wsgi__
timelines: gunicorn --access-logfile - --capture-output posts:__hug_wsgi__

# timelines1: gunicorn -p $PORT sqlite+pysqlite:///timeline.db
# timelines2: gunicorn -p $PORT sqlite+pysqlite:///timeline.db
# timelines3: gunicorn -p $PORT sqlite+pysqlite:///timeline.db
