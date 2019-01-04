from flask import Flask

from play import Ur

app = Flask(__name__)


@app.route("/")
def games():
	return "<a href='/games/1'>game 1</a><p></p><a href='/games/2'>game 2<a>"

@app.route("/games/<game_id>")
def game(game_id):
	game = Ur()
	game.load_game(int(game_id))
	return "{}".format(game.board)