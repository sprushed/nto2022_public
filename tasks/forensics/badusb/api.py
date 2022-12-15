from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
import sqlite3
import random
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
db = sqlite3.connect(":memory:", check_same_thread=False)
page = open("main.html").read()

def record(id, key):
    # check if id exists
    c = db.cursor()
    c.execute("SELECT * FROM keys WHERE id=?", (id,))
    if c.fetchone() is None:
        db.execute("INSERT INTO keys VALUES (?, ?)", (id, key))
        db.commit()
        return True
    else:
        return False


def db_init():
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS keys (id text, key blob)")
    db.commit()


@app.get("/gen_key/{id}")
def gen_key(id: str):
    key = random.randbytes(32)
    if record(id, key):
        return {"key": key.hex()}
    else:
        return JSONResponse(status_code=409, content={"error": "id already exists"})


@app.get("/keys")
def get_keys():
    c = db.cursor()
    c.execute("SELECT * FROM keys")
    keys = c.fetchall()
    encoded_keys = []
    for key in keys:
        encoded_keys.append({"id": key[0], "key": key[1].hex()})

    return encoded_keys


@app.get("/")
def get_home():
    return HTMLResponse(page)


@app.get("/cryptor.exe")
def get_cryptor():
    return FileResponse("cryptor.exe")


def init_data():
    key_id = "9d92cd5e-de53-423a-a972-f4c7a6554d68"
    key = bytes.fromhex(
        "e9612a5963f4f2deb6eabd92f5e5e135aabfdff6e173f944179686521395e243"
    )
    record(key_id, key)


@app.on_event("startup")
def startup():
    db_init()
    init_data()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
