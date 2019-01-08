import glob
import json
import os
import random


class Ur(object):

	roll_map = {0: 1, 1: 1, 2: 1,
				3: 2, 4: 2, 5: 2,
				6: 3,
				7: 4}

	gameover = False  # when True, the game will end
	board = None  # this will be loaded in new_game() or load_game()

	def new_game(self, game_id=None):
		"""Resets the board to the initial state, the beginning of a new game"""
		with open('new_game.json') as board_init:
			board_data = json.load(board_init)
		self.board = board_data
		self.roll()
		if game_id:
			self.save_game(game_id)
		else:
			self.save_game()

	def save_game(self, game_id=None):
		if game_id:
			filename = 'games/game_{}.json'.format(game_id)
			os.makedirs(os.path.dirname(filename), exist_ok=True)  # make required directories if not created yet
			with open(filename, 'w') as board_file:
				json.dump(self.board, board_file, indent=4)
		else:
			filename = 'games/game_1.json'
			os.makedirs(os.path.dirname(filename), exist_ok=True)  # make required directories if not created yet
			with open(filename, 'w') as board_file:
				json.dump(self.board, board_file, indent=4)

	def load_game(self, game_id=None):
		if game_id:
			with open('games/game_{}.json'.format(game_id)) as board_file:
				self.board = json.load(board_file)
		else:
			# default to game_1
			with open('games/game_1.json') as board_file:
				self.board = json.load(board_file)

	def reset_game(self, game_id):
		self.new_game()
		self.save_game(game_id=game_id)

	def get_all_game_ids(self):
		all_games = glob.glob("games/game_*.json")  # get all games in games/ directory
		game_ids = []
		for game in all_games:
			game_id = game.split('/')[-1].split('.')[0].split('_')[-1]
			game_ids.append(game_id)
		return game_ids

	def get_new_game_id(self):
		all_game_ids = self.get_all_game_ids()
		if all_game_ids:
			new_game_id = str(int(max(all_game_ids)) + 1)  # increment the current max id
		else:
			new_game_id = "1"  # initial game id
		return new_game_id

	def play(self):
		while not self.gameover:
			if not self.board["roll"]:
				self.roll()
			if self.can_move():
				move = self.get_move()
				landed_on_rosette = self.make_move(move)
				if not landed_on_rosette:
					self.change_turn()
				self.roll()
			else:
				print("You rolled {} and have no available moves. Skipping your turn.".format(self.board["roll"]))
				self.change_turn()
			self.save_game()

	def play_move(self, move):
		valid_move = self.validate_move(move)
		if valid_move:
			roll_again = self.make_move(move)
			if not roll_again:
				self.change_turn()
			self.roll()
			self.save_game()

	def roll(self):
		self.board["roll"] = self.roll_map[random.randint(0, 7)]

	def change_turn(self):
		if self.board["current_turn"] == "WHITE":
			self.board["current_turn"] = "BLACK"
		else:
			self.board["current_turn"] = "WHITE"

	def can_move(self):
		a_valid_move_exists = False
		# try all possible moves and see if any of them are valid
		for i in range(21):
			move = str(i)
			if self.validate_move(move, verbose=False):
				a_valid_move_exists = True
		return a_valid_move_exists

	def get_move(self):
		valid_move = False

		# ask for moves until a valid one is received
		while not valid_move:
			if self.board["current_turn"] == "WHITE":
				move = input("Roll: {}\nWhite's move: ".format(self.board["roll"]))
			else:
				move = input("Roll: {}\nBlack's move: ".format(self.board["roll"]))

			if move in ["quit", "gameover", "game over"]:
				self.gameover = True
				valid_move = True
			else:
				try:
					valid_move = self.validate_move(move)
				except (KeyError, ValueError) as e:
					print("Bad input. Try again.")

		return move

	def get_new_position(self, move):
		current_color = self.board["current_turn"].lower()
		appropriate_path = self.board["{}_path".format(current_color)]  # either 'white_path' or 'black_path'
		return str(appropriate_path[appropriate_path.index(move) + self.board["roll"]])

	def validate_move(self, move, verbose=True):
		if (int(move) < 0 or int(move) > 20):
			if verbose: print("Invalid move. You must choose a position between 0 and 20 (inclusive).")
			return False
		if move == "0" and self.board["available_{}".format(self.board["current_turn"]).lower()] == 0:
			if verbose: print("Invalid move. You have no more available pieces left.")
			return False
		if move != "0" and self.board[move]["current_piece"] != self.board["current_turn"]:
			if verbose: print("Invalid move. You do not have a piece there.")
			return False
		# either 'white_path' or 'black_path'
		appropriate_path = self.board["{}_path".format(self.board["current_turn"]).lower()]
		if (appropriate_path.index(move) + self.board["roll"]) > (len(appropriate_path) - 1):
			if verbose: print("Invalid move. You must roll the exact number of squares to get off the board.")
			return False
		new_position = self.get_new_position(move)
		if new_position != "21" and self.board[new_position]["current_piece"] == self.board["current_turn"]:
			if verbose: print("Invalid move. You would land on your own piece.")
			return False
		return True

	def make_move(self, move):
		if move in ["quit", "gameover", "game over"]:
			self.gameover = True
			return True

		if move == "0":
			# subtract one from either available_black or available_white
			self.board["available_{}".format(self.board["current_turn"]).lower()] -= 1
		else:
			self.board[move]["current_piece"] = None  # remove piece from old space

		new_position = self.get_new_position(move)

		if new_position == "21":
			self.complete_piece()
			return False  # return True so player can roll again, False to change turn
		else:
			if self.board[new_position]["current_piece"] in ["WHITE", "BLACK"]:
				self.overtake_opposing_piece()
			self.board[new_position]["current_piece"] = self.board["current_turn"]

		return self.board[new_position]["is_rosette"]  # return True so player can roll again, False to change turn

	def overtake_opposing_piece(self):
		if self.board["current_turn"] == "WHITE":
			print("Overtook a black piece!")
			# overtake a black piece
			self.board["available_black"] += 1
		else:
			# overtake a white piece
			self.board["available_white"] += 1
			print("Overtook a white piece!")

	def complete_piece(self):
		current_color = self.board["current_turn"].lower()
		self.board["completed_{}".format(current_color)] += 1
		if self.board["current_turn"] == "WHITE":
			print("White completed a piece and scored a point!")
		else:
			print("Black completed a piece and scored a point!")

		# check if the game is over
		if self.board["completed_white"] == 7 or self.board["completed_black"] == 7:
			self.gameover = True


if __name__ == '__main__':
	choice = input("New game? (y/n)\n(this overwrites existing game if it exists): ")
	if choice in ["y", "Y", "yes"]:
		game = Ur()
		game.new_game()
		game.play()
	else:
		game = Ur()
		game.load_game()
		game.play()
