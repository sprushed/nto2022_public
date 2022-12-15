import MySQLdb

connection = MySQLdb.connect(
    host="mysql",
    user="MisterCreeper",
    passwd="MrsZombie",
    db="BlockNaBlock",
)

cursor = connection.cursor()


def user_exists(username):
    query = "SELECT id FROM users WHERE username=%s"
    cursor.execute(query, (username,))

    user = cursor.fetchone()
    return user


def add_user(username, password):
    query = "INSERT INTO users (username, password, balance) VALUES (%s, %s, 10)"
    cursor.execute(query, (username, password, ))

    connection.commit()


def verify_user(username, password):
    query = "SELECT id FROM users WHERE username=%s and password=%s"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    return user


def get_user(username):
    query = "SELECT username, balance FROM users WHERE username=%s"
    cursor.execute(query, (username, ))

    user = cursor.fetchone()
    return user


def get_latest_block_id(username):
    query = "SELECT id FROM blocks WHERE block_author_username=%s"
    cursor.execute(query, (username, ))

    id = cursor.fetchall()[-1]
    return id


def get_accept_requests(username):
    query = "SELECT block_id, block_text FROM to_accept WHERE acceptor_username=%s"
    cursor.execute(query, (username, ))

    reqs = cursor.fetchall()
    return reqs


def delete_accept_request(username, block_id):
    query = "DELETE FROM to_accept WHERE acceptor_username=%s and block_id=%s"
    cursor.execute(query, (username, block_id))

    connection.commit()


def delete_user(username):
    query = "DELETE FROM users WHERE username=%s"
    cursor.execute(query, (username))

    connection.commit()


def add_block(username, block_text):
    query = "INSERT INTO blocks (block_author_username, block_text, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, block_text, "created"))

    connection.commit()


def get_blocks(username):
    query = "SELECT id, status from blocks where block_author_username=%s"
    cursor.execute(query, (username, ))

    blocks = cursor.fetchall()
    return blocks


def get_acceptors_by_block_id(id):
    query = "SELECT acceptor_username FROM to_accept WHERE block_id=%s"
    cursor.execute(query, (id, ))

    accs = cursor.fetchall()
    return accs


def get_block_by_id(username, id):
    query = "SELECT block_text, status from blocks where block_author_username=%s and id=%s"
    cursor.execute(query, (username, id))

    block = cursor.fetchone()
    return block


def add_accept_block(block_id, block_text, acceptor):
    query = "INSERT INTO to_accept (block_id, block_text, acceptor_username) VALUES (%s, %s, %s)"
    cursor.execute(query, (block_id, block_text, acceptor))

    connection.commit()


def update_balance(username, new_bal):
    query = "UPDATE users SET balance=%s where username=%s"
    cursor.execute(query, (new_bal, username))

    connection.commit()


def update_block_status(id, new_status):
    query = "UPDATE blocks SET status=%s where id=%s"
    cursor.execute(query, (new_status, id))

    connection.commit()
