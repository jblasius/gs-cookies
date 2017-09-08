import re
import math
from re import sub
from datetime import date, timedelta
from decimal import Decimal
from flask import render_template, flash, redirect, session, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.models import *
from app.oauth_facebook import FacebookSignIn, external_auth
from app.sheet_data import *
from app.task import taskman
from app.forms import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home',
                           # user=g.user)
                           user=current_user)


@app.route('/login')
def login():
    return render_template('login.html',
                            title='Login')


@app.route('/authorize_facebook')
def authorize_facebook():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = FacebookSignIn()
    return oauth.authorize()


@app.route('/callback')
def show_preloader_start_authentication():

    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    # store in the session id of the asynchronous operation
    status_pending = AsyncOperationStatus.query.filter_by(code='pending').first()
    async_operation = AsyncOperation(async_operation_status_id=status_pending.id)
    db.session.add(async_operation)
    db.session.commit()
    # store in a session the id of asynchronous operation
    session['async_operation_id'] = str(async_operation.id)

    taskman.add_task(external_auth)

    return redirect(url_for('preloader'))


# renders a loader page
@app.route('/preloader')
def preloader():
    return render_template('preloader.html',
                           title='Waiting...')


# returns status of the async operation
@app.route('/get-status')
def get_status():
    if 'async_operation_id' in session:
        async_operation_id = session['async_operation_id']
        print async_operation_id
        # retrieve from database the status of the stored in session async operation
        async_operation = AsyncOperation.query.filter_by(id= \
        async_operation_id).join(AsyncOperationStatus).first()
        status = str(async_operation.status.code)
        print async_operation.status.code
    else:
        print "async operation not in session"
        return redirect(url_for(error))
    return status


@app.route('/success')
def success():
    if 'async_operation_id' in session:
        async_operation_id = session['async_operation_id']
        async_operation = AsyncOperation.query.filter_by(id=async_operation_id).join(User).first()
        user = User.query.filter_by(id=async_operation.user_profile_id).first()
        login_user(user, remember=True)
        flash('Logged in successfully.')
        # TODO: Add a redirect catch for the next URL (http://flask.pocoo.org/snippets/62/)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))


@app.route('/color', methods=['GET', 'POST'])
def color():
    selectedChoices = ChoiceObj('colors', session.get('selected'))
    form = ColorLookupForm(obj=selectedChoices)

    form.colors.choices = [(c, c) for c in allColors]

    if form.validate_on_submit():
        session['selected'] = form.colors.data
        return redirect(url_for('color'))
    else:
        print form.errors
    return render_template('color.html',
                           form=form,
                           selected=session.get('selected'))


@app.route('/goal')
@login_required
def goal():
    tempdate=datetime(2017,3,23)

    # Determine the start and stop dates
    first_monday = datetime.strptime(get_data_range('FirstMonday'), '%m/%d/%Y')
    last_date = datetime.strptime(get_data_range('LastDay'), '%m/%d/%Y')

    # Determine the current week number
    if tempdate < first_monday:
        week_num = 1
    elif tempdate > last_date:
        tempdate = last_day
        delta_ms = tempdate - first_monday
        delta_d = delta_ms.days
        week_num = int(math.floor((delta_d)/7+1))
    else:
        delta_ms = tempdate - first_monday
        delta_d = delta_ms.days
        week_num = int(math.floor((delta_d)/7+1))

    girl_info = get_girl_info(session['girl_name'])
    all_transactions = get_all_transactions(tempdate)
    
    #Calculate the following:
    # girl_total_goc (column 12, zero based)
    # troop_total_goc (column 12, zero based)
    # girl_total_sold (column 13, zero based)
    # troop_total_sold (column 13, zero based)
    girl_total = {}
    girl_total['sold'] = 0.0
    girl_total['week1_personal'] = 0.0
    girl_total['week2_personal'] = 0.0
    girl_total['week3_personal'] = 0.0
    girl_total['week4_personal'] = 0.0
    girl_total['week5_personal'] = 0.0
    girl_total['week6_personal'] = 0.0
    girl_total['week7_personal'] = 0.0
    girl_total['week8_personal'] = 0.0
    girl_total['week9_personal'] = 0.0
    girl_total['week1_booth'] = 0.0
    girl_total['week2_booth'] = 0.0
    girl_total['week3_booth'] = 0.0
    girl_total['week4_booth'] = 0.0
    girl_total['week5_booth'] = 0.0
    girl_total['week6_booth'] = 0.0
    girl_total['week7_booth'] = 0.0
    girl_total['week8_booth'] = 0.0
    girl_total['week9_booth'] = 0.0
    girl_goc = {}
    girl_goc['sold'] = 0.0
    girl_goc['week1'] = 0.0
    girl_goc['week2'] = 0.0
    girl_goc['week3'] = 0.0
    girl_goc['week4'] = 0.0
    girl_goc['week5'] = 0.0
    girl_goc['week6'] = 0.0
    girl_goc['week7'] = 0.0
    girl_goc['week8'] = 0.0
    girl_goc['week9'] = 0.0
    troop_total = {}
    troop_total['sold'] = 0.0
    troop_total['week1_personal'] = 0.0
    troop_total['week2_personal'] = 0.0
    troop_total['week3_personal'] = 0.0
    troop_total['week4_personal'] = 0.0
    troop_total['week5_personal'] = 0.0
    troop_total['week6_personal'] = 0.0
    troop_total['week7_personal'] = 0.0
    troop_total['week8_personal'] = 0.0
    troop_total['week9_personal'] = 0.0
    troop_total['week1_booth'] = 0.0
    troop_total['week2_booth'] = 0.0
    troop_total['week3_booth'] = 0.0
    troop_total['week4_booth'] = 0.0
    troop_total['week5_booth'] = 0.0
    troop_total['week6_booth'] = 0.0
    troop_total['week7_booth'] = 0.0
    troop_total['week8_booth'] = 0.0
    troop_total['week9_booth'] = 0.0
    troop_goc = {}
    troop_goc['sold'] = 0.0
    troop_goc['week1'] = 0.0
    troop_goc['week2'] = 0.0
    troop_goc['week3'] = 0.0
    troop_goc['week4'] = 0.0
    troop_goc['week5'] = 0.0
    troop_goc['week6'] = 0.0
    troop_goc['week7'] = 0.0
    troop_goc['week8'] = 0.0
    troop_goc['week9'] = 0.0

    for transaction in all_transactions:
        if transaction[3] == session['girl_name']:
            girl_goc['sold'] += float(transaction[12] or 0) #number as a string
            girl_total['sold'] += float(transaction[13] or 0) #number as a string
            if transaction[18] == "1":
                girl_goc['week1'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week1_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week1_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "2":
                girl_goc['week2'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week2_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week2_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "3":
                girl_goc['week3'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week3_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week3_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "4":
                girl_goc['week4'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week4_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week4_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "5":
                girl_goc['week5'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week5_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week5_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "6":
                girl_goc['week6'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week6_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week6_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "7":
                girl_goc['week7'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week7_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week7_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "8":
                girl_goc['week8'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week8_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week8_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "9":
                girl_goc['week9'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    girl_total['week9_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    girl_total['week9_booth'] += float(transaction[13] or 0)
        if transaction[17] == girl_info['troop']:
            troop_goc['sold'] += float(transaction[12] or 0) #number as a string
            troop_total['sold'] += float(transaction[13] or 0) #number as a string
            if transaction[18] == "1":
                troop_goc['week1'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week1_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week1_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "2":
                troop_goc['week2'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week2_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week2_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "3":
                troop_goc['week3'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week3_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week3_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "4":
                troop_goc['week4'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week4_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week4_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "5":
                troop_goc['week5'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week5_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week5_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "6":
                troop_goc['week6'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week6_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week6_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "7":
                troop_goc['week7'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week7_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week7_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "8":
                troop_goc['week8'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week8_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week8_booth'] += float(transaction[13] or 0)
            elif transaction[18] == "9":
                troop_goc['week9'] += float(transaction[12] or 0)
                if transaction[1] == "Personal":
                    troop_total['week9_personal'] += float(transaction[13] or 0)
                if transaction[1] == "Booth":
                    troop_total['week9_booth'] += float(transaction[13] or 0)

    girl_total['week2_personal_cumul'] = girl_total['week1_personal'] + girl_total['week2_personal']
    girl_total['week3_personal_cumul'] = girl_total['week2_personal_cumul'] + girl_total['week3_personal']
    girl_total['week4_personal_cumul'] = girl_total['week3_personal_cumul'] + girl_total['week4_personal']
    girl_total['week5_personal_cumul'] = girl_total['week4_personal_cumul'] + girl_total['week5_personal']
    girl_total['week6_personal_cumul'] = girl_total['week5_personal_cumul'] + girl_total['week6_personal']
    girl_total['week7_personal_cumul'] = girl_total['week6_personal_cumul'] + girl_total['week7_personal']
    girl_total['week8_personal_cumul'] = girl_total['week7_personal_cumul'] + girl_total['week8_personal']
    girl_total['week9_personal_cumul'] = girl_total['week8_personal_cumul'] + girl_total['week9_personal']

    girl_total['week2_booth_cumul'] = girl_total['week1_booth'] + girl_total['week2_booth']
    girl_total['week3_booth_cumul'] = girl_total['week2_booth_cumul'] + girl_total['week3_booth']
    girl_total['week4_booth_cumul'] = girl_total['week3_booth_cumul'] + girl_total['week4_booth']
    girl_total['week5_booth_cumul'] = girl_total['week4_booth_cumul'] + girl_total['week5_booth']
    girl_total['week6_booth_cumul'] = girl_total['week5_booth_cumul'] + girl_total['week6_booth']
    girl_total['week7_booth_cumul'] = girl_total['week6_booth_cumul'] + girl_total['week7_booth']
    girl_total['week8_booth_cumul'] = girl_total['week7_booth_cumul'] + girl_total['week8_booth']
    girl_total['week9_booth_cumul'] = girl_total['week8_booth_cumul'] + girl_total['week9_booth']

    # girl_goc['week2_cumul'] = girl_goc['week1'] + girl_goc['week2']
    # girl_goc['week3_cumul'] = girl_goc['week2_cumul'] + girl_goc['week3']
    # girl_goc['week4_cumul'] = girl_goc['week3_cumul'] + girl_goc['week4']
    # girl_goc['week5_cumul'] = girl_goc['week4_cumul'] + girl_goc['week5']
    # girl_goc['week6_cumul'] = girl_goc['week5_cumul'] + girl_goc['week6']
    # girl_goc['week7_cumul'] = girl_goc['week6_cumul'] + girl_goc['week7']
    # girl_goc['week8_cumul'] = girl_goc['week7_cumul'] + girl_goc['week8']
    # girl_goc['week9_cumul'] = girl_goc['week8_cumul'] + girl_goc['week9']

    troop_total['week2_personal_cumul'] = troop_total['week1_personal'] + troop_total['week2_personal']
    troop_total['week3_personal_cumul'] = troop_total['week2_personal_cumul'] + troop_total['week3_personal']
    troop_total['week4_personal_cumul'] = troop_total['week3_personal_cumul'] + troop_total['week4_personal']
    troop_total['week5_personal_cumul'] = troop_total['week4_personal_cumul'] + troop_total['week5_personal']
    troop_total['week6_personal_cumul'] = troop_total['week5_personal_cumul'] + troop_total['week6_personal']
    troop_total['week7_personal_cumul'] = troop_total['week6_personal_cumul'] + troop_total['week7_personal']
    troop_total['week8_personal_cumul'] = troop_total['week7_personal_cumul'] + troop_total['week8_personal']
    troop_total['week9_personal_cumul'] = troop_total['week8_personal_cumul'] + troop_total['week9_personal']

    troop_total['week2_booth_cumul'] = troop_total['week1_booth'] + troop_total['week2_booth']
    troop_total['week3_booth_cumul'] = troop_total['week2_booth_cumul'] + troop_total['week3_booth']
    troop_total['week4_booth_cumul'] = troop_total['week3_booth_cumul'] + troop_total['week4_booth']
    troop_total['week5_booth_cumul'] = troop_total['week4_booth_cumul'] + troop_total['week5_booth']
    troop_total['week6_booth_cumul'] = troop_total['week5_booth_cumul'] + troop_total['week6_booth']
    troop_total['week7_booth_cumul'] = troop_total['week6_booth_cumul'] + troop_total['week7_booth']
    troop_total['week8_booth_cumul'] = troop_total['week7_booth_cumul'] + troop_total['week8_booth']
    troop_total['week9_booth_cumul'] = troop_total['week8_booth_cumul'] + troop_total['week9_booth']

    # troop_goc['week2_cumul'] = troop_goc['week1'] + girl_goc['week2']
    # troop_goc['week3_cumul'] = troop_goc['week2_cumul'] + troop_goc['week3']
    # troop_goc['week4_cumul'] = troop_goc['week3_cumul'] + troop_goc['week4']
    # troop_goc['week5_cumul'] = troop_goc['week4_cumul'] + troop_goc['week5']
    # troop_goc['week6_cumul'] = troop_goc['week5_cumul'] + troop_goc['week6']
    # troop_goc['week7_cumul'] = troop_goc['week6_cumul'] + troop_goc['week7']
    # troop_goc['week8_cumul'] = troop_goc['week7_cumul'] + troop_goc['week8']
    # troop_goc['week9_cumul'] = troop_goc['week8_cumul'] + troop_goc['week9']

    # Determine the break points for the gauge chart color changes
    if week_num == 1:
        yellowFrom = 0.20
        yellowTo = 0.25
    elif week_num == 2:
        yellowFrom = 0.40
        yellowTo = 0.50
    elif week_num == 3:
        yellowFrom = 0.60
        yellowTo = 0.75
    elif week_num == 4:
        yellowFrom = 0.80
        yellowTo = 0.85
    elif week_num == 5:
        yellowFrom = 0.90
        yellowTo = 0.95
    elif week_num == 6:
        yellowFrom = 0.92
        yellowTo = 0.96
    elif week_num == 7:
        yellowFrom = 0.94
        yellowTo = 0.97
    elif week_num == 8:
        yellowFrom = 0.95
        yellowTo = 0.98
    elif week_num > 8:
        yellowFrom = 0.96
        yellowTo = 0.99

    # Set up the gauge chart options
    # https://developers.google.com/chart/interactive/docs/gallery/gauge
    chart1_options = {}
    chart1_options['total'] = float(girl_total['sold'])
    chart1_options['max'] = max(float(girl_info['goal']), float(girl_total['sold']))
    chart1_options['greenFrom'] = float(girl_info['goal'])*yellowTo
    chart1_options['greenTo'] = max(float(girl_info['goal']), float(girl_total['sold']))
    chart1_options['redFrom'] = float(girl_info['goal'])*0
    chart1_options['redTo'] = float(girl_info['goal'])*yellowFrom
    chart1_options['yellowFrom'] = float(girl_info['goal'])*yellowFrom
    chart1_options['yellowTo'] = float(girl_info['goal'])*yellowTo

    chart3_options = {}
    chart3_options['total'] = float(troop_total['sold'])
    chart3_options['max'] = max(float(girl_info['troop_goal']), float(troop_total['sold']))
    chart3_options['greenFrom'] = float(girl_info['troop_goal'])*yellowTo
    chart3_options['greenTo'] = max(float(girl_info['troop_goal']), float(troop_total['sold']))
    chart3_options['redFrom'] = float(girl_info['troop_goal'])*0
    chart3_options['redTo'] = float(girl_info['troop_goal'])*yellowFrom
    chart3_options['yellowFrom'] = float(girl_info['troop_goal'])*yellowFrom
    chart3_options['yellowTo'] = float(girl_info['troop_goal'])*yellowTo

    # Determine the percentage to goal
    percent = {}
    percent['goal'] = round(100*girl_total['sold'] / float(girl_info['goal']),1)
    percent['troop_goal'] = round(100*troop_total['sold'] /float(girl_info['troop_goal']),1)
    percent['goal_goc'] = round(100*girl_goc['sold'] / float(girl_info['goal_goc']),1)
    percent['troop_goal_goc'] = round(100*troop_goc['sold'] /float(girl_info['troop_goal_goc']),1)

    # Determine the picture to load based on the GoC percentage
    goc_pic = {}
    if percent['goal_goc'] < 10:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QWkyU2tRZ0I5VEU'
    elif percent['goal_goc'] < 20:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4R0tXLThfSnpNQTA'
    elif percent['goal_goc'] < 30:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4TzdibkFyNUhFRHc'
    elif percent['goal_goc'] < 40:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4WXZ3UGVxOENVdzA'
    elif percent['goal_goc'] < 50:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QktjSHM0eFF3dUU'
    elif percent['goal_goc'] < 60:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4b3NzSC0xam9ZekE'
    elif percent['goal_goc'] < 70:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4SHZ3cXExNW9fU28'
    elif percent['goal_goc'] < 80:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4Y29zbElyNzNhTTg'
    elif percent['goal_goc'] < 90:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4X08wRGJCY0w1VlE'
    elif percent['goal_goc'] < 100:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QXVwMWtjWWctUVk'
    elif percent['goal_goc'] >= 100:
        goc_pic['girl'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4WG9DaVh2WDBoZnc'
    
    if percent['troop_goal_goc'] < 10:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QWkyU2tRZ0I5VEU'
    elif percent['troop_goal_goc'] < 20:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4R0tXLThfSnpNQTA'
    elif percent['troop_goal_goc'] < 30:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4TzdibkFyNUhFRHc'
    elif percent['troop_goal_goc'] < 40:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4WXZ3UGVxOENVdzA'
    elif percent['troop_goal_goc'] < 50:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QktjSHM0eFF3dUU'
    elif percent['troop_goal_goc'] < 60:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4b3NzSC0xam9ZekE'
    elif percent['troop_goal_goc'] < 70:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4SHZ3cXExNW9fU28'
    elif percent['troop_goal_goc'] < 80:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4Y29zbElyNzNhTTg'
    elif percent['troop_goal_goc'] < 90:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4X08wRGJCY0w1VlE'
    elif percent['troop_goal_goc'] < 100:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4QXVwMWtjWWctUVk'
    elif percent['troop_goal_goc'] >= 100:
        goc_pic['troop'] = 'https://docs.google.com/uc?id=0BzC5F6zg91g4WG9DaVh2WDBoZnc'

    # Define messages for percentage to goal
    msg_goal_met = 'Congratulations on reaching your goal! YOU ROCK!'
    msg_goal_good = 'You\'re on track to meet your goal. Keep up the good work'
    msg_goal_okay = 'You\'re doing okay, but don\'t lose sight of your goal.'
    msg_goal_work = 'It may be a challenge to reach your goal. Think about other things you can do to increase your chances of success.'

    # Determine the message to display in regards to the percentage to goal.
    msg = {}
    if percent['goal'] < 100*yellowFrom:
        msg['goal'] = msg_goal_work
    elif percent['goal'] >= 100*yellowFrom and percent['goal'] < 100*yellowTo:
        msg['goal'] = msg_goal_okay
    elif percent['goal'] >= 100*yellowFrom and percent['goal'] < 100:
        msg['goal'] = msg_goal_good
    elif percent['goal'] >= 100:
        msg['goal'] = msg_goal_met

    # Determine if the gift of Caring patch has been achieved
    if girl_goc['sold'] >= 25:
        msg['goc'] = 'Congratulations! You\'ve earned the gift of Caring patch (25).'
    else:
        msg['goc'] = ''

    # Build the dictionaries to pass to HTML template
    info = {}
    info['today'] = tempdate.strftime("%m/%d/%Y")
    info['week_num'] = week_num

    return render_template('goal.html',
                           info=info,
                           girl_info=girl_info,
                           percent=percent,
                           chart1_options=chart1_options,
                           chart3_options=chart3_options,
                           girl_total=girl_total,
                           girl_goc=girl_goc,
                           troop_total=troop_total,
                           troop_goc=troop_goc,
                           goc_pic=goc_pic,
                           msg=msg,
                           title='Goal Status')


@app.route('/financials')
@login_required
def financials():
    tempdate=date(2017,2,20)

    transactions = get_girl_transactions(session['girl_name'])

    #Calculate the total number sold, total amount paid, and the
    # total amount due from the transaction data. For each transaction
    # the number sold in in column 14, the amount due is in column 15
    # and the amount paid is in column 16

    total_sold = 0
    total_due = 0
    total_paid = 0

    for transaction in transactions:
        total_sold += float(transaction[13] or 0) #zero based, nummer as a string
        total_due += Decimal(sub(r'[^\d\-.]', '', transaction[14])) #zero-based
        total_paid += Decimal(sub(r'[^\d\-.]', '', transaction[15])) #zero-based
        #https://stackoverflow.com/questions/8421922/how-do-i-convert-a-currency-string-to-a-floating-point-number-in-python

    return render_template('financials.html',
                           transactions=transactions,
                           info=[session['girl_name'],total_sold,tempdate.strftime("%A %B %d, %Y")],
                           totals=[total_due, total_paid, total_due-total_paid],
                           title='Financials')


@app.route('/incentives')
@login_required
def incentives():

    tempGirl = {}
    session['girl_name']
    tempGirl['num_sold'] = 420

    reward_choices = get_reward_choices(session['girl_name'])
    if reward_choices == -1:
        flash('Error retrieving rewards data.')
        return redirect(url_for('index'))

    reward_pics = get_reward_pics()
    if reward_pics == -1:
        flash('Error retrieving picture data.')
        return redirect(url_for('index'))

    # build a list of rewards choices for a particular girl
    # Each row of the list is a list of reward attributes
    # [0] = Package range
    # [1] = Reward name, long form
    # [2] = Reward image file URL from Google Sheet 2018 Reward Pics
    # [3] = Earned status
    # [4] = Minimum number for level
    Rewards = []
    for key, value in reward_choices.iteritems():
        # Search for Program Credit to find generic picture
        # Search for errors in the sheet and assign empty string to URL
        match = re.search(r'Program Credit', value)
        if match:
            this_pic = reward_pics['Program Credit']
        elif value == '#REF!':
            this_pic = ''
        else:
            try:
                this_pic = reward_pics[value]
            except KeyError:
                this_pic = ''

        # Determine minimum number of packages to earn a reward
        match = re.search(r'(\d+)(-)(\d+)', key)
        if match:
            min_number = int(match.group(1))
        else:
            min_number = 10000

        # Determine if the reward has been earned
        if tempGirl['num_sold'] > min_number:
            status = 'Yes'
        else:
            status = 'No'

        # Build the list that feeds the html table
        Rewards.append([key, value, this_pic, status, min_number])

    return render_template('incentives.html',
                           info=[session['girl_name'],tempGirl['num_sold']],
                           rewards=sorted(Rewards, key=lambda item: item[4]),
                           title='Incentives')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = GirlChoice()

    if form.validate_on_submit():

        #TODO Save the selected user/girl combination(s) to the database
        #     Make sure the db and session objects match
        session['girl_name'] = form.girl_choice.data

        return redirect(url_for('profile'))
    else:
        print form.errors

    return render_template('profile.html',
                           form=form,
                           title='My Account')


@app.route('/configuration')
@login_required
def configuration():
    configuration = get_configuration()

    return render_template('configuration.html',
                            configuration=configuration,
                            title='Configuration Data')


# renders an error page
@app.route('/error')
def error():
    return render_template('error.html',
                           title='Error')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
