import sys
import re
from flask import render_template, flash, redirect, session, url_for, request, g
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
from datetime import datetime
from app import app, lm
from config import SERVICE_KEY
from app.rewards import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/rewards')
def rewards():

    Girl = {}
    Girl['name'] = 'Amber S.'
    Girl['num_sold'] = 43

    reward_choices = get_reward_choices('Name')
    if reward_choices == -1:
        flash('Error retrieving rewards data.')
        return redirect(url_for('index'))

    # sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(
    #     SERVICE_KEY, sheet_scope)

    # http_auth = credentials.authorize(Http())
    # sheets_service = build('sheets', 'v4', http=http_auth)

    # spreadsheetId = '1oiIxf5Nti1fIRV00eBHaDgJonJkGrrwp18yQNukzyzk'
    # data_range = 'TestRange'
    # rewards_result = sheets_service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId,
    #     range=data_range,
    #     majorDimension='COLUMNS').execute()
    # reward_choices = rewards_result.get('values', [])

    # if not reward_choices:
    #     flash('Error retrieving rewards data.')
    #     return redirect(url_for('index'))

    reward_pics = get_reward_pics()
    if reward_pics == -1:
        flash('Error retrieving picture data.')
        return redirect(url_for('index'))

    # Set up a dictionary of reward_name and image_path from
    # Google Sheet 2018 Reward Pics
    # reward_picsId = '1ceLLUkyiw57LJo1_Gl7RlS5VrgMbNcEGFmiupI_U_9s'
    # pics_range = 'PicsData'
    # pics_result = sheets_service.spreadsheets().values().get(
    #     spreadsheetId=reward_picsId, range=pics_range).execute()
    # pics_data = pics_result.get('values', [])

    # if not pics_data:
    #     flash('Error retrieving picture data.')
    #     return redirect(url_for('index'))

    # Incoming url
    # https://drive.google.com/file/d/0BzC5F6zg91g4bWRVcHJBa0Z3UEk/view?usp=drivesdk
    #
    # Desired Outgoing url
    # https://docs.google.com/uc?id=0B4yfJJJSNrfuelE1QXlxWjlJcUE
    # url_prefix = 'https://docs.google.com/uc?id='
    # reward_pics = {}
    # for reward in pics_data:
    #     match = re.search(r'(https://drive.google.com/file/d/)(\w+)(/view.+)', reward[1])
    #     if match:
    #         reward_pics[reward[0]] = url_prefix+match.group(2)
    #     else:
    #         reward_pics[reward[0]] = ''

    # build a list of rewards choices for a particular girl
    # Each row of the list is a list of reward attributes
    # [0] = Package range
    # [1] = Reward name, long form
    # [2] = Reward image file location from google Sheet 2018 Reward Pics
    # [3] = Earned status
    Rewards = []
    for row in reward_choices:
        # Remove dollar amount form program credit name to find generic picture
        # Search for errors in the sheet and assign empty string to URL
        match = re.search(r'Program Credit', row[1])
        if match:
            this_pic = reward_pics['Program Credit']
        elif row[1] == '#REF!':
            this_pic = ''
        else:
            try:
                this_pic = reward_pics[row[1]]
            except KeyError:
                this_pic = ''
        # Determine minimum number of packages to earn a reward
        match = re.search(r'(\d+)(-)(\d+)', row[0])
        if match:
            min_number = int(match.group(1))
        else:
            min_number = 10000

        # Determine of the reward has been earned
        if Girl['num_sold'] > min_number:
            status = 'Yes'
        else:
            status = 'No'

        # Build the list that feeds the html table
        Rewards.append([row[0], row[1], this_pic, status])

    return render_template('rewards.html',
                           rewards=Rewards,
                           title='Rewards')

        #reward_level, reward_choice, reward_pic, reward_earned_pic

