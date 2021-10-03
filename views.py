import os

from flask import Flask, render_template, redirect,\
    url_for, session, request, jsonify
from flask_bootstrap import Bootstrap

from logic import Game

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = os.environ.get('SECRET_KEY', 'dev')


@app.route('/', methods=['POST', 'GET'])
def index():
    game_json = session.get('game')
    state = None
    n = None
    m = None
    if game_json is not None:
        game = Game.from_json(game_json)
        state = game.state
        n = game.n
        m = game.m
    return render_template("index.html", state=str(state),
                           n=n, m=m)


@app.route('/_next_state')
def get_next_state():
    n = request.args.get('n')
    m = request.args.get('m')
    state = request.args.get('state')
    nxt = request.args.get('nxt')
    game = Game(int(state), int(n), int(m))
    if int(nxt):
        game.next_state()
    session['game'] = game.to_json()
    return jsonify(n=game.n, m=game.m, state=str(game.state))