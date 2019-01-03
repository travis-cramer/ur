import json
import random


class Ur(object):

	roll_map = {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3, 7: 4}

	gameover = False  # when True, the game will end
	board = None  # this will be loaded in init_board()

	def init_board(self):
		"""Resets the board to initial state, the beginning of a new game"""
		with open('board_init.json') as board_init:
			board_data = json.load(board_init)
		self.board = board_data
		self.save_board()

	def save_board(self):
		with open('board.json', 'w') as board_file:
			json.dump(self.board, board_file, indent=4)

	def load_board(self):
		with open('board.json') as board_file:
			self.board = json.load(board_file)

	def roll(self):
		self.board["roll"] = self.roll_map[random.randint(0, 7)]

	def get_move(self):
		valid_move = False

		# ask for moves until a valid one is received
		while not valid_move:
			if self.board["current_turn"] == "WHITE":
				move = raw_input("Roll: {}\nWhite's move: ".format(self.board["roll"]))
			else:
				move = raw_input("Roll: {}\nBlack's move: ".format(self.board["roll"]))

			if move in ["quit", "gameover", "game over"]:
				self.gameover = True
				valid_move = True
			else:
				try:
					valid_move = self.validate_move(move)
				except (KeyError, ValueError) as e:
					print("Bad input. Try again.")

		return move

	def change_turn(self):
		if self.board["current_turn"] == "WHITE":
			self.board["current_turn"] = "BLACK"
		else:
			self.board["current_turn"] = "WHITE"
		self.roll()

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
		appropriate_path = self.board["{}_path".format(self.board["current_turn"]).lower()]  # either 'white_path' or 'black_path'
		if (appropriate_path.index(move) + self.board["roll"]) > len(appropriate_path):
			if verbose: print("Invalid move. You must roll the exact number of squares to get off the board.")
			return False
		if self.board[self.get_new_position(move)]["current_piece"] == self.board["current_turn"]:
			if verbose: print("Invalid move. You would land on your own piece.")
			return False
		return True

	def overtake_opposing_piece(self):
		if self.board["current_turn"] == "WHITE":
			print("Overtook a black piece!")
			# overtake a black piece
			self.board["available_black"] += 1
		else:
			# overtake a white piece
			self.board["available_white"] += 1
			print("Overtook a white piece!")

	def get_new_position(self, move):
		appropriate_path = self.board["{}_path".format(self.board["current_turn"]).lower()]  # either 'white_path' or 'black_path'
		return str(appropriate_path[appropriate_path.index(move) + self.board["roll"]])

	def can_move(self):
		a_valid_move_exists = False
		# try all possible moves and see if any of them are valid
		for i in range(21):
			move = str(i)
			if self.validate_move(move, verbose=False):
				a_valid_move_exists = True
		return a_valid_move_exists

	def play_move(self, move):
		if move in ["quit", "gameover", "game over"]:
			self.gameover = True
			return True

		if move == "0":
			self.board["available_{}".format(self.board["current_turn"]).lower()] -= 1  # subtract one from either available_black or available_white
		else:
			self.board[move]["current_piece"] = None  # remove piece from old space

		new_position = self.get_new_position(move)

		if self.board[new_position]["current_piece"] and self.board[new_position]["current_piece"] != self.board["current_turn"]:
			self.overtake_opposing_piece()
		self.board[new_position]["current_piece"] = self.board["current_turn"]

		return self.board[new_position]["is_rosette"]  # return True so player can roll again, False to change turn

	def play(self):
		self.load_board()
		while not self.gameover:
			if not self.board["roll"]:
				self.roll()
			if self.can_move():
				move = self.get_move()
				landed_on_rosette = self.play_move(move)
				if not landed_on_rosette:
					self.change_turn()
			else:
				print("You rolled {} and have no available moves. Skipping your turn.".format(self.board["roll"]))
				self.change_turn()
			self.save_board()


if __name__ == '__main__':
	choice = raw_input("New game? (y/n)\n(this overwrites existing game if it exists): ")
	if choice in ["y", "Y", "yes"]:
		game = Ur()
		game.init_board()
		game.play()
	else:
		game = Ur()
		game.play()
