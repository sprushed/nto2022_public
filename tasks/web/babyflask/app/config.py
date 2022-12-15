import os
import psycopg2
from psycopg2 import pool


def configure(app):
    app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'nosecrets?'

    app.config['FLAG'] = os.getenv('FLAG')
    app.config['DB_HOST'] = os.getenv('DB_HOST') or 'db'
    app.config['DB_PORT'] = int(os.getenv('DB_PORT')) or 5432
    app.config['DB_USER'] = os.getenv('DB_USER') or 'moderator'
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD') or 'moderator'
    app.config['DATABASE'] = os.getenv('POSTGRES_DB') or 'nto'

    app.config['CONN_POOL'] = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=32,
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        user = app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DATABASE']
    )

    return app