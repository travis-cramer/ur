The Royal Game of Ur
--------------------

The Roayal Game of Ur is an ancient board game. This is a repo (in progress) with the server and client code for running an in-broswer version of this game.

Currently, it only runs locally as a python script from your command line. The only dependency is Python 2.

Run
```
python play.py
```
to start the game!

How to move:
To move a piece, enter the board index (see Board Indexing below) where the piece you want to move is located. For example, if you want to move a new piece from off the board onto the board, enter "0" (without the quotes). If you are playing as black, and you want to move your piece that's sitting on square 8, enter "8".

Unfortunately, the board is not visible in the terminal application. You must use your mind to visualize and remember where all the pieces are as you play. It is primarily a debugging tool for now to ensure we have the correct rules and logic in place.

NOTE: if you want to begin a game from a particular game state / position (very useful for exploring edge cases), edit the game_1.json file in the games/ directory. Then, choose not to start a new game when you re-launch the program.

Board Indexing
--------------
Below is a picture representing the index encoding of each square that we have chosen to use. The bottom of the board is white's side and the top is black's. There are also indexes "0" and "21" (not shown here) which represent the two offboard positions, with "0" being where pieces begin and "21" being where pieces finish.

![alt text](https://www199.lunapic.com/editor/working/154657390376193862?2342992322)


How to Install
--------------
1. Create a new directory on your local machine. Call it anything you want, perhaps "ur" or "20squares". On Unix/Linux:
```
mkdir ur
```
2. Move into that directory. On Unix/Linux:
```
cd ur/
```
3. If you haven't before, install virtualenv. (https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
4. Then, create a virtualenv called "env" using python 3 within your "ur" or "20squares" directory. On Unix/Linux:
```
virtualenv -p python3 env
```
5. Activate it. On Unix/Linux:
```
. env/bin/activate
```
6. If you don't have it, install git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
7. Then, clone this github repo within your "ur" or "20squares" directory:
```
git clone https://github.com/pyracmon/20squares
```
8. Move into the cloned repo:
```
cd 20squares/
```
9. Install all requirements listed in "requirements.txt" (with your virtualenv activated):
```
pip install -r requirements.txt
```
10. Start the server:
```
FLASK_APP=server.py flask run
```
11. Go to the url that the server is running on (this will be listed in the terminal output).
12. Enjoy :)