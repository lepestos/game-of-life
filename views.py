import os

from flask import Flask, render_template, redirect,\
    url_for, session, request, jsonify
from flask_bootstrap import Bootstrap

from forms import GameForm
from logic import Game

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = os.environ.get('SECRET_KEY', 'dev')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = GameForm()
    if form.validate_on_submit():
        state = form.state.data
        game = Game.from_str(state, sep='\r\n')
        session['n'] = game.n
        session['m'] = game.m
        session['state'] = game.binary_state()
        return redirect(url_for('index'))
    n, m, state = session.get('n'), session.get('m'), session.get('state')
    return render_template("index.html",form=form,
                           n=n, m=m, state=state)

@app.route('/_next_state')
def get_next_state():
    n = request.args.get('n')
    m = request.args.get('m')
    state = request.args.get('state')
    game = Game.from_number(int(state), int(n), int(m))
    game.next_state()
    return jsonify(n=game.n, m=game.m, state=game.binary_state())