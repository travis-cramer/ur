from flask import Flask, request, render_template, jsonify

from play import Ur

app = Flask(__name__, static_folder='')


@app.route("/")
def games():
	return "<a href='/board?game_id=1'>game 1</a><p></p><a href='/board?game_id=2'>game 2<a>"

@app.route("/board/")
def board():
	game_id = request.args.get('game_id')
	return render_template('index.html', game_id=game_id)

@app.route("/games/<game_id>")
def game(game_id):
	game = Ur()
	game.load_game(game_id)
	return jsonify(game.board)

@app.route("/games/<game_id>/actions/move/")
def move(game_id):
	game = Ur()
	game.load_game(game_id)
	game.play_move(request.args.get('move'))
	return jsonify(game.board)

@app.route("/games/<game_id>/actions/reset/")
def reset(game_id):
	game = Ur()
	game.reset_game(game_id)
	return jsonify(game.board)
