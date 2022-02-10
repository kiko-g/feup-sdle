import os
import pickle
import sys
import time

from flask import Flask, request
from flask_cors import CORS

FLASK_PORT_OFFSET = 5000


def load_users():
    with open(os.path.join(sys.path[0], "users.pickle"), 'rb') as f:
        return pickle.load(f)


def write_users(users) -> None:
    with open(os.path.join(sys.path[0], "users.pickle"), 'wb') as f:
        pickle.dump(users, f)


def pop_last_user():
    users = load_users()
    users.pop()
    write_users(users)


app = Flask(__name__)
cors = CORS()


@app.route('/time')
def get_current_time() -> dict:
    return {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))}


@app.route('/register', methods=["POST"])
def register() -> dict:
    users = load_users()
    username = request.get_json()['username']
    password = request.get_json()['password']
    print(f"Username Register {username}")
    for user in users:
        if user['username'] == username:
            return {'success': False, 'user': None, 'error': 'Username already in use.'}
    serial_id = int(users[-1]['id']) + 1
    users.append({
        'id': f"{serial_id}",
        'username': username,
        'password': password
    })

    write_users(users)

    return {'success': True, 'user': users[-1], 'error': None, 'port': int(users[-1]['id']) + FLASK_PORT_OFFSET}


@app.route('/login', methods=["POST"])
def login() -> dict:
    users = load_users()
    username = request.get_json()['username']
    password = request.get_json()['password']

    for user in users:
        if user['username'] == username and user['password'] == password:
            return {'success': True, 'user': user, 'error': None, 'port': int(user['id']) + FLASK_PORT_OFFSET}

    return {'success': False, 'user': None, 'error': 'Incorrect credentials'}
