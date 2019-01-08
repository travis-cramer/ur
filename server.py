from flask import Flask, request, render_template, jsonify, redirect, url_for

from play import Ur


app = Flask(__name__)


@app.route("/")
def index():
	game = Ur()
	all_game_ids = game.get_all_game_ids()
	all_game_ids.sort()
	return render_template('home.html', game_ids=all_game_ids)

@app.route("/new_game/")
def new_game():
	game = Ur()
	game.new_game(game.get_new_game_id())
	return redirect(url_for('games'))

@app.route("/board/")
def board():
	game_id = request.args.get('game_id')
	return render_template('board.html', game_id=game_id)

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


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=False)