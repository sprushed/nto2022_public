#!/usr/bin/env python3
from flask import Flask, g, session, request
from flask import redirect, url_for
from flask import render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import DictCursor
import functools

# please, i do not wanna make frontend
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm

from config import configure

app = Flask(__name__)
app = configure(app)
Bootstrap(app)

def get_db():
    if 'db' not in g:
        g.db = app.config['CONN_POOL'].getconn()
        g.db.autocommit = True
        g.cur = g.db.cursor(cursor_factory=DictCursor)
    return g.db, g.cur


@app.teardown_appcontext
def close_conn(e):
    cur = g.pop('cur', None)
    db = g.pop('db', None)
    if db is not None:
        cur.close()
        app.config['CONN_POOL'].putconn(db)


def login_required(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        abort(403)

    return inner_handle


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        username, password = form.username.data, form.password.data
        secret = request.args.get('secret')
        db, cur = get_db()
        cur.execute(
            "SELECT * FROM users WHERE username = %s;",
            (username,)
        )
        user = cur.fetchone()
        print(user)
        if user:
            flash("Register failed.", category="error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        cur.execute(
            f"INSERT INTO users(username, password, is_admin) VALUES ('{username}', '{hashed_password}', False)"
        )
        flash("Register success.")
        return redirect(url_for("login"))

    return render_template("register_user.html", form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username, password = form.username.data, form.password.data
        db, cur = get_db()
        cur.execute(
            "SELECT * FROM users WHERE username = %s;",
            (username,)
        )
        user = cur.fetchone()
        if user is None:
            flash("Failed to log in.", category="error")
            return redirect(url_for("login"))

        if not check_password_hash(user["password"], password):
            flash("Failed to log in.", category="error")
            return redirect(url_for("login"))

        session.clear()
        session['user_id'] = user["id"]
        session['is_admin'] = user["is_admin"]
        session['username'] = user["username"]
        session['secret'] = user["secret"]
        return redirect(url_for("index"))

    return render_template("login_user.html", form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have signed out.")
    return redirect(url_for('index'))


@app.route('/')
def index():
    user = session.get('user_id')
    if user is None:
        return render_template('index.html')

    return render_template('index.html')


@app.route('/admin')
@login_required
def admin():
    if session['is_admin']:
        return f"Hello, {session['username']}, here is your secret: {app.config['FLAG']}"
    else:
        return "Hello stranger"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1337)