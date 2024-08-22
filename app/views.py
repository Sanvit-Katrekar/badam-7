''' Contains all routes and backend logic in the web application '''

from flask import request, url_for, redirect, render_template, flash, g, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db, redis_db
from app.constants import *
from app.forms import *
from app.models import *
from app.utils import *
#from app.puzzle import Puzzle
from .cards.cards_logic import *
from .cards.utils import *
import os

@app.route('/')
def index():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('home'))
	return redirect(url_for('register'))

@app.route('/rules')
def rules():
	return render_template('rules.html', title='Rules')


# === User login methods ===

@app.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
	return User.query.get(id)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		print("Val is:", form.username.data)
		user = User.query.filter_by(username=form.username.data.lower().strip()).first()
		print("User is:", user)
		if user is not None and user.check_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
		else:
			flash('Invalid username or password.')
	return render_template('login.html', title='Login', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			flash('ID already taken!')
			return render_template('register.html', title='Register', form=form)
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			flash('Username already taken!')
			return render_template('register.html', title='Register', form=form)	
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

# ========================

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'GET':
		if session.get('is_user_finished') is None:
			session['is_user_finished'] = False
			print(f"User: {session['_user_id']} connected")
			player_list_obj: dict | None = load_obj('players')
			if player_list_obj is None:
				player_list = []
				current_player_index = 0
			else:
				player_list = player_list_obj['player_list']
				current_player_index = player_list_obj['current_player_index']
			print("List is:", player_list)
			player = User.query.filter_by(id=session['_user_id']).first()
			print("Player requesting is:", player)
			print("Player session is:", session['is_user_finished'])
			if not session['is_user_finished'] and player not in player_list:
				player_list.append(player)
				player_list_obj = {
					"player_list": player_list,
					"current_player_index": current_player_index
				}
				write_obj('players', player_list_obj)
				print("New list:", player_list)
				return redirect(url_for('play'))
			else:
				print("Not added")
				print("Old list:", player_list)
		deck = Deck()
		hands = [Hand() for _ in range(6)]
		deck.distribute_cards(hands)
		hands = hands[:2]

		return render_template(
			'home.html',
			title='Home',
			hands=hands
		)
	
	if request.method == 'POST':
		session['game_id'] = 1
		return redirect(url_for('play'))

@app.route('/player-finish')
@login_required
def player_finish():
	print("Player finis")
	session['is_user_finished'] = True
	players_obj = load_obj('players')
	player_list: list = players_obj['player_list']
	current_player_index = players_obj['current_player_index']
	if session['_user_id'] == player_list[current_player_index].id:
		current_player_index = (current_player_index + 1) % (len(player_list) - 1)
	for i, player in enumerate(player_list):
		print(repr(player.id), repr(session['_user_id']))
		if str(player.id) == session['_user_id']:
			player_list.pop(i)
			break
	if not player_list:
		return redirect(url_for('game_over'))
	players_obj = {
		"player_list": player_list,
		"current_player_index": current_player_index
	}
	write_obj('players', players_obj)
	return redirect(url_for('play'))

@app.route('/update-state', methods=['POST'])
@login_required
def update_status():
	req = request.get_json()
	hand = Hand()
	for card_json in req['hand']:
		hand.add_card(Card.from_json(card_json))
	board_json = req['board']
	board_matrix = []
	for slot in board_json:
		if slot is None:
			board_matrix.append(slot)
			continue
		cards = []
		for card_json in slot:
			cards.append(Card.from_json(card_json))
		board_matrix.append(cards)
	board = load_obj('board')
	board['matrix'] = board_matrix
	write_obj("hand-"+session["_user_id"], hand)
	write_obj("board", board)

	player_list_obj = load_obj('players')
	index = player_list_obj['current_player_index']
	player_list_obj['current_player_index'] = (index + 1) % len(player_list_obj['player_list'])
	write_obj('players', player_list_obj)
	print("Updated state, broadcasting:")
	return redirect(url_for('play'))

@app.route('/play', methods=['GET', 'POST'])
@login_required
def play():
	if request.method == 'GET':
		print("Displaying players:")
		print(load_obj('players'))
		player_hand = load_obj('hand-'+session['_user_id'])

		board_obj = load_obj('board')
		if board_obj is None:
			deck = Deck()
			matrix = [None for _ in range(EMPTY_SLOTS)]
			matrix[EMPTY_SLOTS//2] = deck.cards
			board = {
				"matrix": matrix,
				"display": DEFAULT_CARD_STACK_DISPLAY.value
			}
			write_obj("board", board)
		return render_template(
			'play.html',
			hand=player_hand,
			board=load_obj('board'),
			players=load_obj('players'),
			is_user_finished=session['is_user_finished']
		)

@app.route('/return-chance')
@login_required
def return_chance():
	players_obj = load_obj('players')
	n_players = len(players_obj['player_list'])
	current_player_index = players_obj['current_player_index']
	current_player_index = (current_player_index - 1) % n_players
	players_obj['current_player_index'] = current_player_index
	write_obj('players', players_obj)
	return redirect(url_for('play'))

@app.route('/show-stack', methods=['POST'])
@login_required
def show_stack():
	req = request.get_json()
	board_json = req['board']
	board_matrix = []
	for slot in board_json:
		if slot is None:
			board_matrix.append(slot)
			continue
		cards = []
		for card_json in slot:
			cards.append(Card.from_json(card_json))
		board_matrix.append(cards)
	board_obj = load_obj('board')
	board_obj['matrix'] = board_matrix
	board_obj['display'] = not board_obj['display']
	write_obj('board', board_obj)
	return redirect(url_for('play'))

@app.route('/distribute-cards')
@login_required
def distribute_cards():
	deck = Deck()
	matrix = [None for _ in range(EMPTY_SLOTS)]
	display_status = DEFAULT_CARD_STACK_DISPLAY
	players_obj = load_obj('players')
	player_list = players_obj['player_list']
	hands = [Hand() for _ in range(len(player_list))]
	deck.distribute_cards(hands)

	# Updating hands
	for i, player in enumerate(player_list):
		write_obj(f'hand-{player.id}', hands[i])

	# Updating board
	board = {
		"matrix": matrix,
		"display": display_status.value
	}
	write_obj("board", board)

	return redirect(url_for('play'))

@app.route('/sort-cards', methods=['POST'])
@login_required
def sort_cards():
	cardsResponse = request.get_json()['cards']
	hand = Hand()
	for card in cardsResponse:
		hand.add_card(Card.from_json(card))
	hand.sort()
	write_obj("hand-"+session["_user_id"], hand)
	return redirect(url_for('play'))

@app.route('/game-over')
@login_required
def game_over():
	# Reset finish status
	session['is_user_finished'] = False

	# Reset board
	deck = Deck()
	matrix = [None for _ in range(EMPTY_SLOTS)]
	matrix[EMPTY_SLOTS//2] = deck.cards
	display_status = DEFAULT_CARD_STACK_DISPLAY
	board = {
		"matrix": matrix,
		"display": display_status.value
	}
	write_obj("board", board)

	# Delete players and their hands
	redis_db.delete("players")
	for key in redis_db.scan_iter("hand-*"):
		redis_db.delete(key)
	return redirect(url_for('home'))

# ====================