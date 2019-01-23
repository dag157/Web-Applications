# -*- coding: utf-8 -*-
"""
	Treat yo self salon. Made by Dominick Gurnari
    dag157 4116630
    Pitt

    The styling was taken from minitwit on todd waits site
"""

import time
import datetime
import os
from hashlib import md5

from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

from models2 import db, Owner, Stylist, Patron, Appointment

# create our little application :)
app = Flask(__name__)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'salon.db')

app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.drop_all()
    db.create_all()
    o = Owner(username="owner", email="owner@gmail.com", pw_hash=generate_password_hash("pass"))
    db.session.add(o)
    db.session.commit()
    print('Initialized the database.')

#Dont use this please I made it when I didnt know how to use databases lol
@app.cli.command('bootstrap')
def bootstrap_data():
    """Creates the database tables."""
   
    ##
    ##   INITALIZE DATA BASE WITH EXAMPLES
    ##
    ##
    db.drop_all()
    db.create_all()

    o = Owner(username="owner", email="owner@gmail.com", pw_hash=generate_password_hash("pass"))

    db.session.add(o)
    db.session.commit()

    c1 = Patron("Michael", "michael@aol.com", generate_password_hash("michael"), o.user_idO)
    c2 = Patron("Angela", "angela@aol.com", generate_password_hash("angela"), o.user_idO)
    c3 = Patron("Kevin", "kevin@aol.com", generate_password_hash("kevin"), o.user_idO)
    c4 = Patron("Maher", "maher@aol.com", generate_password_hash("maher"), o.user_idO)
    c5 = Patron("Todd", "todd@aol.com", generate_password_hash("todd"), o.user_idO)

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)

    db.session.commit()

    s1 = Stylist("Jim", "jim@aol.com", generate_password_hash("jim"),o.user_idO)
    s2 = Stylist("Pam", "pam@aol.com", generate_password_hash("pam"),o.user_idO)
    s3 = Stylist("Dwight", "dwight@aol.com", generate_password_hash("dwight"),o.user_idO)
    
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)

    db.session.commit()

    new_slot = datetime.datetime(int("2018"), int("11"),int("13"), 11)
    new_slot2 = datetime.datetime(int("2018"), int("11"),int("14"), 15)
    new_slot3 = datetime.datetime(int("2018"), int("11"),int("15"), 14)
    new_slot4 = datetime.datetime(int("2018"), int("11"),int("16"), 18)
    new_slot5 = datetime.datetime(int("2018"), int("11"),int("17"), 12)


    appdone = Appointment(stylist_id=s1.username,client_id=c1.username,time=new_slot) 
    appdone2 = Appointment(stylist_id=s2.username,client_id=c3.username,time=new_slot2) 
    appdone3 = Appointment(stylist_id=s3.username,client_id=c2.username,time=new_slot3) 
    appdone4 = Appointment(stylist_id=s2.username,client_id=c5.username,time=new_slot4) 
    appdone5 = Appointment(stylist_id=s1.username,client_id=c4.username,time=new_slot5) 

    s1.app.append(appdone)
    c1.app.append(appdone) 

    s2.app.append(appdone2)
    c3.app.append(appdone2)

    s3.app.append(appdone3)
    c2.app.append(appdone3)

    s2.app.append(appdone4)
    c5.app.append(appdone4)

    s1.app.append(appdone5)
    c4.app.append(appdone5)

    db.session.add(appdone)
    db.session.add(appdone2)
    db.session.add(appdone3)
    db.session.add(appdone4)
    db.session.add(appdone5)

    db.session.commit()
   
    print('Initialized the database with examples.')


@app.before_request
def before_request():

    #SUPER IMPORTANT checks which user is in current session

    g.patron = None
    g.stylist = None
    g.owner = None

    if 'user_id' in session:
        g.patron = Patron.query.filter_by(user_id=session['user_id']).first()

    if 'user_idS' in session:
        g.stylist = Stylist.query.filter_by(user_idS=session['user_idS']).first()

    if 'user_idO' in session:
        g.owner = Owner.query.filter_by(user_idO=session['user_idO']).first()



#main route after login
@app.route('/', methods=['GET', 'POST'])
def timeline():
	
    #CHECK FOR WHICH USER IS LOGGED IN

    if not g.patron:
        if not g.stylist:
            if not g.owner:
                return redirect(url_for('login'))

    if g.stylist:
        return redirect(url_for('timelineStyle'))
              
    return render_template('timeline2.html',workers=Owner.query.filter_by(username="owner").first().workers)

#current appointments for the stylist
@app.route('/currentapps', methods=['GET', 'POST'])
def timelineStyle():

    #
    # CURRENT APPOINTMENTS FOR THE STYLISTS
    # ITERATES THROUGH ALL POSSIBLE TIME FOR NEXT 30 DAYS
    # CHECKS CURRENT TIME AND COMPARES WITH APPOINTMENT DATABASE
    #

    if g.stylist:

        #grab important info

        profile_user_stylist = Stylist.query.filter_by(username=g.stylist.username).first()
        patronCheck = False
        work_dates = []
        available_list = []
        profile_user = profile_user_stylist

        #work hours
        work_dates_fixed = []
        work_time = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        booked = Stylist.query.filter_by(username=g.stylist.username).first().app

        booked_list = []

        #make a list of apps
        for m in booked:
            booked_list.append(m)

        #make a appointment within the next 30 days
        for i in range(30):
            for j in work_time:
                #get current and future dates
                des = datetime.datetime.now() + datetime.timedelta(i)

                #check if its today
                if i == 0:
                    #checks if the time is greater than the current time
                    if j > int(des.strftime("%H")):
                        if int(des.strftime("%w")) != 0 and int(des.strftime("%w")) != 1:
                            
                            #set base case

                            testy = "AVAILABLE"

                            #set the new time and add it to overall list
                            new_slot = datetime.datetime(int(des.strftime("%Y")), int(des.strftime("%m")),int(des.strftime("%d")), j)
                            work_dates.append(new_slot)

                            #iterate for each database object
                            for ds in booked_list:
                                #check for equalitity
                                n = datetime.datetime(int(ds.time[0:4]), int(ds.time[5:7]), int(ds.time[8:10]), int(ds.time[11:13]))
                                
                                if n.strftime("%A") == new_slot.strftime("%A"):
                                    if n.strftime("%B") == new_slot.strftime("%B"):
                                        if n.strftime("%d") == new_slot.strftime("%d"):
                                            if n.strftime("%Y") == new_slot.strftime("%Y"):
                                                if n.strftime("%I") == new_slot.strftime("%I"):
                                                    if n.strftime("%p") == new_slot.strftime("%p"):
                                                        print("hi")
                                                        testy = ds.client_id

                            available_list.append(testy)   
                else:
                    if int(des.strftime("%w")) != 0 and int(des.strftime("%w")) != 1:
                            #check in data base for another if

                        testy = "AVAILABLE"

                        new_slot = datetime.datetime(int(des.strftime("%Y")), int(des.strftime("%m")),int(des.strftime("%d")), j)
                        work_dates.append(new_slot)

                        for ds in booked_list:
                            n = datetime.datetime(int(ds.time[0:4]), int(ds.time[5:7]), int(ds.time[8:10]), int(ds.time[11:13]))
                            if n.strftime("%A") == new_slot.strftime("%A"):
                                if n.strftime("%B") == new_slot.strftime("%B"):
                                    if n.strftime("%d") == new_slot.strftime("%d"):
                                        if n.strftime("%Y") == new_slot.strftime("%Y"):
                                            if n.strftime("%I") == new_slot.strftime("%I"):
                                                if n.strftime("%p") == new_slot.strftime("%p"):
                                                    #print("hi")
                                                    testy = ds.client_id

                        available_list.append(testy) 
                        

        for i in work_dates:
            #print(i)
            work_dates_fixed.append(i.strftime("%A") + " " + i.strftime("%B") + " " + i.strftime("%d") + " " + i.strftime("%Y") + " " + i.strftime("%I") + " " + i.strftime("%p"))
    
    if not g.patron:
        if not g.stylist:
            if not g.owner:
                return redirect(url_for('login'))

              
    return render_template('timeline2.html',workers=Owner.query.filter_by(username="owner").first().workers, dates=work_dates, available=available_list)

@app.route('/login', methods=['GET', 'POST'])
def login():

    #
    # LOGS THE USER IN
    # ERROR CHECKS FOR EXISITNG USERS
    # ALSO CHECKS IF THE USER EXISTS TO BEGIN WITH
    #

    """Logs the user in."""
    if g.patron:
	    return redirect(url_for('timeline'))
    if g.stylist:
        return redirect(url_for('timeline'))
    if g.owner:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':

        user = Patron.query.filter_by(username=request.form['username']).first()
        user2 = Stylist.query.filter_by(username=request.form['username']).first()
        user3 = Owner.query.filter_by(username=request.form['username']).first()

        patronBool = False
        stylistBool = False
        ownerBool = False
        passExists = False
        userExists = False

        if user is None:
            error = 'Invalid username'
            pass
        else:
            patronBool = True
            userExists = True
            if check_password_hash(user.pw_hash, request.form['password']):
                passExists = True

        if user2 is None:
            error = 'Invalid username'
            pass
        else:
            stylistBool = True
            userExists = True
            if check_password_hash(user2.pw_hash, request.form['password']):
                passExists = True

        if user3 is None:
            error = 'Invalid username'
            pass
        else:
            ownerBool = True
            print('OWNER')
            userExists = True
            print(request.form['password'])
            if check_password_hash(user3.pw_hash, request.form['password']) == True:
                print('OWNER2')
                passExists = True
        
        if userExists == True:
            if passExists == False:
                error = 'Invalid password'
            else:
                
                flash('You were logged in')

                if patronBool == True:
                    session['user_id'] = user.user_id
                elif stylistBool == True:
                    session['user_idS'] = user2.user_idS
                else:
                    session['user_idO'] = user3.user_idO
                return redirect(url_for('timeline'))
                
    return render_template('login2.html', error=error)

@app.route('/public')
def public_timeline(username):
	"""Displays the latest messages of all users."""
    #
    # REDIRECTS TO YOUR MAIN PAGE
    #

	return render_template('timeline2.html', messages=[])


@app.route('/register', methods=['GET', 'POST'])
def register():

    #
    #
    #   REGISTERS PATRON
    #   CHECKS FOR EXISITNG USERS
    #


    """Registers the user."""
    if g.patron:
        return redirect(url_for('timeline'))
    if g.stylist:
        return redirect(url_for('timeline'))
    if g.owner:
        return redirect(url_for('timeline'))
    
    error = None
    if request.method == 'POST':
        user3 = Owner.query.filter_by(username="owner").first()
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        elif get_user_id2(request.form['username']) is not None:
            error = 'The username is already taken'
        elif get_user_id3(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db.session.add(Patron(request.form['username'], request.form['email'], generate_password_hash(request.form['password']), user3.user_idO))
            db.session.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register2.html', error=error)

@app.route('/registerStylist', methods=['GET', 'POST'])
def registerStylist():
    """Registers the user."""
   
   #
   # REGISTERS A STYLIST
   # SIMILAR METHOD ABOVE BUT I COPIED IT SINCE
   # THIS WAS ONE OF THE FIRST THINGS I DID ON THE PROJECT
   #
    
    error = None
    if request.method == 'POST':
        user3 = Owner.query.filter_by(username="owner").first()
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        elif get_user_id2(request.form['username']) is not None:
            error = 'The username is already taken'
        elif get_user_id3(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            s = Stylist(request.form['username'], request.form['email'], generate_password_hash(request.form['password']),user3.user_idO)
            db.session.add(s)

            

            db.session.commit()
            flash('You have successfully registered a stylist')
            return redirect(url_for('registerStylist'))
    return render_template('registerStylist.html', error=error)


@app.route('/logout')
def logout():

    #
    # LOGS OUT USERS AND POPS
    # REDIRECTS TO LOGIN SCREEN
    #

    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    session.pop('user_idS', None)   
    session.pop('user_idO', None)
    return redirect(url_for('login'))


def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = Patron.query.filter_by(username=username).first()
	return rv.user_id if rv else None


def get_user_id2(username):
	"""Convenience method to look up the id for a username."""
	rv = Stylist.query.filter_by(username=username).first()
	return rv.user_idS if rv else None

def get_user_id3(username):
	"""Convenience method to look up the id for a username."""
	rv = Owner.query.filter_by(username=username).first()
	return rv.user_idO if rv else None

def gravatar_url(email, size=80):
	"""Return the gravatar image for the given email address."""
	return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
		(md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.route('/<username>')
def user_timeline(username):
    
    #
    #
    #  DISPLAYS THE OWNER AND PATRON ALL APPOINTMENTS THAT THE STYLISY HAS
    #  IT DISPLAYS BOOKED IF FULL
    #
    #

    profile_user = Patron.query.filter_by(username=username).first()
    profile_user_stylist = Stylist.query.filter_by(username=username).first()

    allava = True

    if g.owner or g.patron:

        patronCheck = False
        

        work_dates = []
        available_list = []

        if profile_user is not None:
            patronCheck = True
            booked_list = []

            booked = Patron.query.filter_by(username=username).first().app

            for m in booked:
                booked_list.append(m.time)
                available_list.append(m.stylist_id)
                

            for ds in booked_list:
                n = datetime.datetime(int(ds[0:4]), int(ds[5:7]), int(ds[8:10]), int(ds[11:13]))
                if n > datetime.datetime.now():
                    work_dates.append(n)
                    

            
        elif profile_user_stylist is not None:
            patronCheck = False
            profile_user = profile_user_stylist

            work_dates_fixed = []
            work_time = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

            booked = Stylist.query.filter_by(username=username).first().app

            booked_list = []

            for m in booked:
                booked_list.append(m)

            for i in range(8):
                for j in work_time:
                    des = datetime.datetime.now() + datetime.timedelta(i)

                    if i == 0:
                        if j > int(des.strftime("%H")):
                            if int(des.strftime("%w")) != 0 and int(des.strftime("%w")) != 1:

                                if g.owner:
                                    testy = "AVAILABLE"
                                else:
                                    testy = True

                                new_slot = datetime.datetime(int(des.strftime("%Y")), int(des.strftime("%m")),int(des.strftime("%d")), j)
                                work_dates.append(new_slot)

                                for ds in booked_list:
                                    n = datetime.datetime(int(ds.time[0:4]), int(ds.time[5:7]), int(ds.time[8:10]), int(ds.time[11:13]))
                                    if n.strftime("%A") == new_slot.strftime("%A"):
                                        if n.strftime("%B") == new_slot.strftime("%B"):
                                            if n.strftime("%d") == new_slot.strftime("%d"):
                                                if n.strftime("%Y") == new_slot.strftime("%Y"):
                                                    if n.strftime("%I") == new_slot.strftime("%I"):
                                                        if n.strftime("%p") == new_slot.strftime("%p"):
                                                            
                                                            allava = False
                                                            if g.owner:
                                                                testy = ds.client_id
                                                            else:
                                                                testy = False

                                available_list.append(testy)   
                    else:
                        if int(des.strftime("%w")) != 0 and int(des.strftime("%w")) != 1:
                            

                            if g.owner:
                                testy = "AVAILABLE"
                            else:
                                testy = True

                            new_slot = datetime.datetime(int(des.strftime("%Y")), int(des.strftime("%m")),int(des.strftime("%d")), j)
                            work_dates.append(new_slot)

                            for ds in booked_list:
                                n = datetime.datetime(int(ds.time[0:4]), int(ds.time[5:7]), int(ds.time[8:10]), int(ds.time[11:13]))
                                if n.strftime("%A") == new_slot.strftime("%A"):
                                    if n.strftime("%B") == new_slot.strftime("%B"):
                                        if n.strftime("%d") == new_slot.strftime("%d"):
                                            if n.strftime("%Y") == new_slot.strftime("%Y"):
                                                if n.strftime("%I") == new_slot.strftime("%I"):
                                                    if n.strftime("%p") == new_slot.strftime("%p"):
                                                        allava = False
                                                        if g.owner:
                                                            testy = ds.client_id
                                                        else:
                                                            testy = False

                            available_list.append(testy) 

            for i in work_dates:
                work_dates_fixed.append(i.strftime("%A") + " " + i.strftime("%B") + " " + i.strftime("%d") + " " + i.strftime("%Y") + " " + i.strftime("%I") + " " + i.strftime("%p"))

        elif profile_user_stylist is None:
            abort(404)
        elif profile_user is None:
            abort(404)

    return render_template('profilepage2.html', profile_user=profile_user, person=patronCheck, dates=work_dates, available=available_list, allava=allava)

@app.route('/request_appointments', methods=['GET', 'POST'])
def requestAppointments():
    
    #
    #
    # REQUEST AN APPOINTMENT
    #
    #


    app = request.args.get('appointment_date')

    if app is None:
        app = "Requested"

    error = None

    if request.method == 'POST':

        if app == "Requested":
            flash('You have already registered for this slot')
            return redirect(url_for('requestAppointments'))

        client = Patron.query.filter_by(username=g.patron.username).first()
        s = Stylist.query.filter_by(username=request.args.get('styname')).first()

        appdone = Appointment(stylist_id=s.username,client_id=client.username,time=app) 
        s.app.append(appdone)
        client.app.append(appdone) 
        db.session.add(appdone)
        db.session.commit()

        flash('You have successfully registered a an appointment for ' + app)
        return redirect(url_for('requestAppointments'))

    return render_template('requestAppointment.html', error=error, currapp=app)

@app.route('/cancel', methods=['GET', 'POST'])
def cancelAppointments():
    
    #
    # CANCEL AN APPOINTMENT
    #

    app = request.args.get('appointment_date')

    if app is None:
        app = "Cancelled"

    error = None

    if request.method == 'POST':

        if app == "Requested":
            flash('You have already registered for this slot')
            return redirect(url_for('requestAppointments'))

        client = Patron.query.filter_by(username=g.patron.username).first()
        s = Stylist.query.filter_by(username=request.args.get('styname')).first()
        t = Appointment.query.all()

        appdone = Appointment(stylist_id=s.username,client_id=client.username,time=app) 

        for j in t:
            if j.stylist_id == appdone.stylist_id:
                if j.client_id == appdone.client_id:
                    if j.time == appdone.time:
                        db.session.delete(j)

        for j in s.app:
            if j.stylist_id == appdone.stylist_id:
                if j.client_id == appdone.client_id:
                    if j.time == appdone.time:
                        pass

        for j in client.app:
            if j.stylist_id == appdone.stylist_id:
                if j.client_id == appdone.client_id:
                    if j.time == appdone.time:
                        pass

        db.session.commit()

        flash('You have successfully registered a an appointment for ' + app)
        return redirect(url_for('cancelAppointments'))

    return render_template('cancelAppointment.html', error=error, currapp=app)

app.jinja_env.filters['gravatar'] = gravatar_url


