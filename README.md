The Royal Game of Ur
--------------------

The Roayal Game of Ur is an ancient board game. This repo contains the server and client code for running an in-broswer version of it.

See the installation instructions below to run your own server of the game. Or, you can immediately demo the game hosted here: http://35.235.77.173:5000/

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
OR
python3 -m virtualenv env
```
5. Activate it. On Unix/Linux:
```
source env/bin/activate
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
python server.py
```
11. Go to the url that the server is running on (this will be listed in the terminal output).
12. Play :)

Board Indexing
--------------
Below is a picture representing the index encoding of each square that we have chosen to use. The bottom of the board is white's side and the top is black's. There are also indexes "0" and "21" (not shown here) which represent the two offboard positions, with "0" being where pieces begin and "21" being where pieces finish.

![alt text](/images/ur-board-indexes.gif?raw=true)
