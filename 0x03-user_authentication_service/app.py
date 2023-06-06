#!/usr/bin/env python3
"""
Basic Flask app for a minimal WSGI application
"""
from flask import Flask, jsonify, request, abort
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """
    Index route that returns a json paylod
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Registers a user using AUTH
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Creates a new session for a user on valid information
    stores in a cookie and returns it as a header
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
