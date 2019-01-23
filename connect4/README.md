# Connect 4 II: The Revenge-- Dominick A Gurnari

Name: Dominick Gurnari
Pitt ID: dag157 4116630

## Installation

1. Run `pip install -r requirements.txt` in a Python 3.7+ virtual environment
2. Set the `FLASK_APP=connect4.py` environment variable and run `flask devinit`
3. Run `flask run` and navigate to `localhost:5000`

Things to note:
Add a new game with a user by putting in the username of your opponent.
If it doesn't exist, you won't get a game with them.

Only the user who created a game may delete it(they must click on the game first).

CLEAR LOCALSTORAGE AND BROWSING DATA BEFORE RUNNING MY APPLICATION OR ELSE IT'LL BREAK (PROBABLY)

DO NOT CLEAR LOCALSTORAGE IN THE MIDDLE OF A GAME, it'll mess it up
(decided not to send whole board back to players since our rubric say we shouldn't)

I have polling set to 1 second, so you may need to click on something pretty hard in order to make it work. Also give stuff time, clicking too fast is a bad idea.


