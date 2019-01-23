#from flask import Flask, request, session, render_template, abort
from models import db, Player, Game
import datetime
import os

import time
from hashlib import md5

import json
from flask import jsonify
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash



app = Flask(__name__)
app.secret_key = "Dev Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "connect4.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/home")
def home():

	games = []
	leaderboardAll = []
	leaderboardAlls = []
	leaderboardAll2 = []
	leaderboardAlls2 = []
	playerNames = []

	best = Game.query.all()
	best2 = Game.query.all()

	for i in best:
		if i.winner_id is not None:
			leaderboardAll.append(i)

	leaderboardAll.sort(key=lambda x: x.turn, reverse=False)

	for k in range(len(leaderboardAll)):
		if k < 10:
			leaderboardAlls.append(leaderboardAll[k])

	

	#best = db.session.query(Game).get(game_id)
	

	if g.user:

		for i in best2:
			if i.winner_id is not None:
				if i.player_one_id == g.user.id or i.player_two_id == g.user.id:
					leaderboardAll2.append(i)

		leaderboardAll2.sort(key=lambda x: x.turn, reverse=False)

		for k in range(len(leaderboardAll2)):
			if k < 10:
				leaderboardAlls2.append(leaderboardAll2[k])

		currPlayer = Player.query.filter_by(id=session['user_id']).first()
		#games = []
		gameExists = Game.query.filter_by(player_one_id=currPlayer.id).first()
		gameExists2 = Game.query.filter_by(player_two_id=currPlayer.id).first()

		if gameExists:
			games = games + Game.query.filter_by(player_one_id=currPlayer.id).all()

		if gameExists2:
			games = games + Game.query.filter_by(player_two_id=currPlayer.id).all()

	return render_template("landing.html", games=games, leaderboard1=leaderboardAlls, leaderboard2=leaderboardAlls2)


@app.route("/game/<game_id>/")
def game(game_id=None):

	game = db.session.query(Game).get(game_id)

	if g.user.id == game.player_one_id or g.user.id == game.player_two_id or g.user:

		if game_id:
			#game = db.session.query(Game).get(game_id)
			return render_template("game.html", game=game)

	return abort(404)

@app.route("/game/<game_id>/delete")
def gameDelete(game_id=None):

	game = db.session.query(Game).get(game_id)

	if g.user.id == game.player_one_id:

		if game_id:
			#game = db.session.query(Game).get(game_id)
			db.session.delete(game)
			db.session.commit()
			return redirect(url_for('home'))

	return abort(404)

# CLI Commands
@app.cli.command("initdb")
def init_db():
    """Initializes database and any model objects necessary for assignment"""
    db.drop_all()
    db.create_all()

    print("Initialized Connect 4 Database.")


@app.cli.command("devinit")
def init_dev_data():
    """Initializes database with data for development and testing"""
    db.drop_all()
    db.create_all()
    print("Initialized Connect 4 Database.")

    ga = Game()
    db.session.add(ga)

    p1 = Player(username="tow", birthday=datetime.datetime.strptime('11/06/1991', '%m/%d/%Y').date(), pw_hash=generate_password_hash("tow"))
    p2 = Player(username="twaits", birthday=datetime.datetime.strptime('01/14/1987', '%m/%d/%Y').date(), pw_hash=generate_password_hash("twaits"))

    db.session.add(p1)
    print("Created %s" % p1.username)
    db.session.add(p2)
    print("Created %s" % p2.username)

    ga.player_one = p1
    ga.player_two = p2

    db.session.commit()
    print("Added dummy data.")

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['email']:
			error = 'You have to enter a valid birthdate'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
            #p1 = Player(username="tow", birthday=datetime.datetime.strptime('11/06/1991', '%m/%d/%Y').date(), pw_hash=generate_password_hash("tow"))
			db.session.add(Player(username=request.form['username'], birthday=datetime.datetime.strptime(request.form['email'],'%m/%d/%Y').date(), pw_hash=generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)

def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = Player.query.filter_by(username=username).first()
	return rv.id if rv else None

@app.route('/', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':

		user = Player.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user.pw_hash, request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user.id
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route("/new_item", methods=["POST"])
def addGame():

	if g.user:
		#ga = Game()
		#db.session.add(ga)

		p1 = Player.query.filter_by(id=session['user_id']).first()
		p2 = Player.query.filter_by(username=request.form["one"]).first()

		if p2 is None:
			print("Doesn't exist")
			flash("User doesn't exist")
			
		else:

			ga = Game()
			db.session.add(ga)
			
			ga.player_one = p1
			ga.player_two = p2

			db.session.commit()

		return "OK!"

@app.route("/items", methods=["GET"])
def get_games():

	games = []
	gameinfo = []
	gameList = []
	

	if g.user:
		currPlayer = Player.query.filter_by(id=session['user_id']).first()
		#games = []
		gameExists = Game.query.filter_by(player_one_id=currPlayer.id).first()
		gameExists2 = Game.query.filter_by(player_two_id=currPlayer.id).first()

		if gameExists:
			#games = games + Game.query.filter_by(player_one_id=currPlayer.id).all()
			gameList = Game.query.filter_by(player_one_id=currPlayer.id).all()
			for i in gameList:
				gameinfo.append(str(i.id))

				p1 = Player.query.filter_by(id=i.player_one_id).first()
				p2 = Player.query.filter_by(id=i.player_two_id).first()

				gameinfo.append(p1.username)
				gameinfo.append(p2.username)
				games.append(gameinfo)
				gameinfo = []
			
			#games.append(gameList)

		if gameExists2:
			#games = games + Game.query.filter_by(player_two_id=currPlayer.id).all()
			gameList = Game.query.filter_by(player_two_id=currPlayer.id).all()
			for i in gameList:
				gameinfo.append(str(i.id))
				p1 = Player.query.filter_by(id=i.player_one_id).first()
				p2 = Player.query.filter_by(id=i.player_two_id).first()

				gameinfo.append(p1.username)
				gameinfo.append(p2.username)
				games.append(gameinfo)
				gameinfo = []

	#print(games)
	#return jsonify
	return json.dumps(games, default=str)

@app.route("/game/<game_id>/update", methods=["POST"])
def updateGame(game_id=None):
	#print(request.form)
	pippo =  request.form.to_dict()
	#print(pippo)
	game = db.session.query(Game).get(game_id)

	#json.loads(input)
	#turn back to string

	if g.user.id == game.player_one_id or g.user.id == game.player_two_id:

		for key, value in pippo.items():
			#print(key)
			key = json.loads(key)
			count = 0
			for item in key:

				#print(item)
				print(item)
				if count == 0:
					game.game_over = bool(json.dumps(item, default=str).title())
				if count == 1:
					game.turn = json.dumps(item, default=str)
				if count == 2:
					game.temp_game_key = json.dumps(item, default=str)
					#for k in key[item]:
					#	print(k)
					for k,p in item.items():
						print(k)
						if k == 'player':
							print(p)
							for keys, values in p.items():
								if keys == "winner":
									if bool(values) == True:
										game.winner_id = g.user.id
								#print(keys)
								#print(values)
							
				if count == 3:
					game.game_board = json.dumps(item, default=str)
				db.session.commit()
				count = count + 1
					
	return "OK!"

@app.route("/game/<game_id>/board", methods=["GET"])
def updatedGameBoard(game_id=None):
	games = []
	game2 = []

	game = db.session.query(Game).get(game_id)

	print(game.temp_game_key)

	if game.temp_game_key is not None:

		game2.append('x')
		game2.append('x')
		game2.append('x')
		game2.append('x')
	
		for i, k in json.loads(game.temp_game_key).items():

			if i == "col":
				game2[1] = k
			elif i == "row":
				game2[0] = k
			elif i == "color":
				game2[2] = k
			else:
				game2[3] = k
			print(i)
			print(k)
			#game2.append(k)

		#game2.append(game.temp_game_key)
		game2.append(game.turn)
		if(game.winner_id is not None):
			game2.append("true")
		else:
			game2.append("false")
		print(game2)

		if game2[0] is not None:
			return json.dumps(game2, default=str)

	return json.dumps(game2,default=str)
	

@app.route("/game/<game_id>/entireboard", methods=["GET"])
def receiveEntireGameBoard(game_id=None):
	games = []

	game = db.session.query(Game).get(game_id)

	games.append(game.game_board)
	games2 = game.game_board
	print(games2)
	#games.append()

	return json.dumps(games2, default=str)
	pass

@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('login'))

@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = Player.query.filter_by(id=session['user_id']).first()

if __name__ == "__main__":
    app.run(threaded=True)

