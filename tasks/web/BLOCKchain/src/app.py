from db import cursor, connection
from flask import Flask

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "Minecraftetomoyazhizhn!"

import routes

@app.before_first_request
def init_db():
    query = """
        CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username varchar(255),
            password varchar(255),
            balance INTEGER
    )"""
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS blocks(
            id INT PRIMARY KEY AUTO_INCREMENT,
            block_author_username varchar(256),
            block_text varchar(2048),
            status varchar(256)
    )"""
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS to_accept(
            id INT PRIMARY KEY AUTO_INCREMENT,
            block_id INTEGER,
            block_text varchar(2048),
            acceptor_username varchar(256)
    )"""
    cursor.execute(query)

    query = """
    INSERT INTO users (username, password, balance) VALUES ('kub036', 'Cr33p3rEnjoyer', 99999999)
    """
    cursor.execute(query)

    connection.commit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
