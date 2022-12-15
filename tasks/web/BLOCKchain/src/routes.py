from app import app
from os import environ
from flask import render_template, request, session, redirect, url_for
from db import add_accept_block, add_block, delete_accept_request, get_accept_requests, get_acceptors_by_block_id, get_block_by_id, get_blocks, get_latest_block_id, get_user, update_balance, update_block_status, user_exists, add_user, verify_user
from time import sleep

flag = "NTO{test}"
admin_name = "Test_admin"

if "flag" in environ:
    flag = environ.get('flag')
if "flag_price" in environ:
    flag_price = environ.get('flag_price')
if "balance_limit" in environ:
    balance_limit = environ.get('balance_limit')
if "admin_name" in environ:
    admin_name = environ.get('admin_name')

try:
    flag_price = int(flag_price)  # type: ignore
    balance_limit = int(balance_limit)  # type: ignore
except Exception as e:
    flag_price = 1337
    balance_limit = 100


@app.route('/', methods=['GET'])
def welcome_page():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username):
            msg = "Minecrafter exists"
        elif len(username) < 3:
            msg = "Username's length should be > 2"
        else:
            add_user(username, password)
            msg = "Successfully registered!"
    return render_template('register.html', message=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session["current_user"] = username
            return redirect(url_for('profile'))
        else:
            msg = "Invalid credentials"
    return render_template('login.html', message=msg)


@app.route('/profile')
def profile():
    msg = ""
    if session.get("current_user"):
        username, balance = get_user(session["current_user"])
        if "msg" in request.args:
            msg = request.args["msg"]
        return render_template('profile.html', username=username, balance=balance, message=msg)
    return redirect(url_for('welcome_page'))


@app.route('/buy_flag', methods=['GET'])
def buy_flag():
    if session.get("current_user"):
        username, balance = get_user(session["current_user"])
        if balance >= flag_price:
            msg = flag
        else:
            msg = "Not enough money"
        return redirect(url_for('profile', msg=msg))
    return redirect(url_for('welcome_page'))


@app.route('/my_blocks', methods=['GET', 'POST'])
def my_blocks():
    msg = ""
    if session.get("current_user"):
        # blocks = get_blocks(session["current_user"])
        username, balance = get_user(session["current_user"])
        blocks = get_blocks(session["current_user"])
        if request.method == "GET":
            return render_template('my_blocks.html', blocks=blocks, username=username, balance=balance, message=msg)
        else:
            if "block_operations" in request.form:
                ops = request.form["block_operations"]
                if admin_name in ops:  # type: ignore
                    msg = "Not allowed to steal from admin :)"
                elif ops.count(";") > 5:
                    msg = "Limit of operations is 5"
                else:
                    ops_parsed = ops.split(";")
                    block_text = "".join(ops_parsed)
                    add_block(session["current_user"], block_text)
                    id = get_latest_block_id(session["current_user"])[0]
                    acceptors = []
                    for line in ops_parsed:
                        if "gets" in line and "from" in line:
                            acceptor = line.split("from ")[-1]
                            if acceptor not in acceptors and get_user(acceptor):
                                acceptors.append(acceptor)
                                add_accept_block(id, block_text, acceptor)
                    msg = "Block created"
                    blocks = get_blocks(session["current_user"])
            return render_template('my_blocks.html', blocks=blocks, username=username, balance=balance, message=msg)
    return redirect(url_for('welcome_page'))


@app.route('/my_requests', methods=['GET', 'POST'])
def my_requests():
    if session.get("current_user"):
        reqs = get_accept_requests(session["current_user"])
        if request.method == "GET":
            return render_template('my_requests.html', reqs=reqs)
        else:
            block_id = int(request.form['block_id'])

            delete_accept_request(session["current_user"], block_id)
            reqs = get_accept_requests(session["current_user"])
            return render_template('my_requests.html', reqs=reqs)
    return redirect(url_for('welcome_page'))


@app.route('/block/<id>', methods=['GET'])
def block_page(id):
    msg = ""
    if session.get("current_user"):
        block = get_block_by_id(session["current_user"], id)
        if block:
            acceptors = get_acceptors_by_block_id(id)
            status = block[1]
            if len(acceptors) == 0 and status == "created":
                new_status = "In progress"
                update_block_status(id, new_status)
                text = block[0]
                text = text.replace("\r", "")
                ops = text.split("\n")
                balances_before = {}
                for line in ops:

                    words = line.split(" ")

                    if len(words) == 5 and words[1] == "gets" and words[3] == "from":
                        try:
                            x = int(words[2])
                            x += 1
                            x -= 1
                        except TypeError:
                            msg = "Not int in operation"
                            break
                        msg, balances_before = change_balance(
                            words[0], words[4], x, balances_before)
                        sleep(1)
                        if msg != "Ok":
                            break

                if msg == "Ok" and admin_name not in balances_before:
                    new_status = "Finished"
                elif msg == "Ok" and admin_name in balances_before:
                    for k, v in balances_before.items():
                        update_balance(k, v)
                    new_status = "Aborted - admin was griefed"
                else:
                    for k, v in balances_before.items():
                        update_balance(k, v)
                    new_status = "Aborted - error during processing"
                update_block_status(id, new_status)

            return render_template('block_page.html', username=session["current_user"], id=id, block=block, acceptors=acceptors, msg=msg, st=status)
    return redirect(url_for('welcome_page'))


def change_balance(receiver, giver, pay, balances_before):
    res = get_user(giver)
    if not res:
        return "No such giver", balances_before
    res2 = get_user(receiver)
    if not res2:
        return "No such receiver", balances_before
    giver_username, giver_balance = res
    receiver_username, receiver_balance = res2

    if pay < 0:
        return "Can't pay negative number. Aborted!", balances_before
    if giver_balance < pay:
        return "Not enough money. Aborted!", balances_before

    if receiver_balance + pay < flag_price and receiver_balance + pay > balance_limit:
        return "Griefing attempt. Aborted!", balances_before

    if giver not in balances_before:
        balances_before[giver] = giver_balance
    if receiver not in balances_before:
        balances_before[receiver] = receiver_balance
    update_balance(giver_username, giver_balance - pay)
    update_balance(receiver_username, receiver_balance + pay)

    return "Ok", balances_before


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome_page'))
