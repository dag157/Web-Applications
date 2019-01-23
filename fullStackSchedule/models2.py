from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

appointments = db.Table('appointments',
	db.Column('stylist_id', db.Integer, db.ForeignKey('stylist.user_idS'), primary_key=True),
	db.Column('patron_id', db.Integer, db.ForeignKey('patron.user_id'), primary_key=True),
    db.Column('appointment_time',  db.String(200), nullable=True)
)

class Owner(db.Model):
    user_idO = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    pw_hash = db.Column(db.String(64), nullable=False)
    workers = db.relationship('Stylist', backref='owner', lazy=True)
    clients = db.relationship('Patron', backref='ownerp', lazy=True)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Stylist(db.Model):
    user_idS = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    pw_hash = db.Column(db.String(64), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.user_idO'), nullable=False)
    appointments = db.relationship('Patron', secondary=appointments, lazy='subquery', backref=db.backref('stylists', lazy=True))
    app = db.relationship('Appointment', backref="style", lazy=True)

    def __init__(self, username, email, pw_hash, owner_id):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash
        self.owner_id = owner_id

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Patron(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    pw_hash = db.Column(db.String(64), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.user_idO'), nullable=False)
    app = db.relationship('Appointment', backref="clie", lazy=True)

    def __init__(self, username, email, pw_hash, owner_id):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash
        self.owner_id = owner_id

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Appointment(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    stylist_id = db.Column(db.String(80), db.ForeignKey('stylist.username'))
    client_id = db.Column(db.String(80), db.ForeignKey('patron.username'))
    time = db.Column(db.String(80), nullable=False)
