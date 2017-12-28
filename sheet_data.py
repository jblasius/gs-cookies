from datetime import date
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
# from app import app
from config import SERVICE_KEY
from datetime import datetime
from werkzeug.contrib.cache import FileSystemCache


"""
Get the Google Sheet configuration data. 
The function will get data from 2018 Cookies. 
The function return a dictionary of key, value
for each configuration setting.
"""
def get_configuration():

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_range = 'configuration'
    data_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId, range=data_range).execute()
    return_data = data_result.get('values', [])

    if not return_data:
        return -1

    configuration = {}
    for row in return_data:
        configuration[row[0]] = row[1]

    cc = FileSystemCache('/var/www/html/gs-cookies/cache/config',
                        default_timeout=300)

    if cc.get('first_monday') is None:
        for key, value in configuration.iteritems():
            cc.set(key, value)

    return configuration


"""
Get the Google Sheet data for the specified data range. 
The function will get data from 2018 Cookies. 
The function return a single value.
TODO: Make function work with a data range larger than a single cell
"""
def get_data_range(range_name):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId, range=range_name).execute()
    return_data = data_result.get('values', [])

    if not return_data:
        return -1

    for data_line in return_data:
        requested_data=(data_line[0])
    return requested_data


"""
Get the Google Sheet data for a specific girl. 
The function will get data from 2018 Cookies. 
The function return a dictionary of name, troop, goal, goc_goal, and troop_goal.
"""
def get_girl_info(girl_name):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_range = 'GirlData'
    girls_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId,
        range=data_range).execute()
    girl_list = girls_result.get('values', [])

    if not girl_list:
        return -1

    girl_info = {}
    for girl in girl_list:
        if girl[0] == girl_name:
            girl_info['name'] = girl[0]
            girl_info['troop'] = girl[1]
            girl_info['goal'] = girl[2]
            girl_info['goal_goc'] = girl[3]

    for girl in girl_list:
        if girl[0] == girl_info['troop']:
            girl_info['troop_goal'] = girl[2]
            girl_info['troop_goal_goc'] = girl[3]
            #TODO Find a way to exit the if loop after getting the answer

    return girl_info


"""
Get the Google Sheet data for names of all girls. 
The function will get data from 2018 Cookies. 
The function return a dictionary of girl and troop.
"""
def get_girl_names():

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_range = 'GirlData'
    girls_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId,
        range=data_range).execute()
    girl_list = girls_result.get('values', [])

    if not girl_list:
        return -1

    girl_names = {}
    for girl in girl_list:
        if (girl[0] != "2196") and (girl[0] != "730"):
            girl_names[girl[0]] = girl[1]

    return girl_names


"""
Get the Google Sheet data for a particualr girl's reward choices. 
The function will get data from 2018 Rewards Tracking. 
The function return a list of lists.
    reward_choices[0] = reward category
    reward_choices[1] = reward choice, long name
"""
def get_reward_choices(girl_name):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    spreadsheetId = '1oiIxf5Nti1fIRV00eBHaDgJonJkGrrwp18yQNukzyzk'
    data_range = 'GirlRewardChoices'
    rewards_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=data_range).execute()
    reward_choices = rewards_result.get('values', [])

    if not reward_choices:
        return -1

    girl_choices = {}
    if reward_choices[0][0] == 'Name':
        reward_category = []
        reward_category = reward_choices[0]
        del reward_category[0]
    for reward_choice in reward_choices:
        if reward_choice[0] == girl_name:
            i = 1
            for reward_cat in reward_category:
                girl_choices[reward_cat] = reward_choice[i]
                i += 1
            break
    if girl_choices == []:
        return -1
    return girl_choices


"""
Get the Google Sheet data for reward icon url. 
The function will get data from 2018 Reward Pics. 
The function return a dictionary of URLs for each reward (long name).
"""
def get_reward_pics():

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    reward_picsId = '1ceLLUkyiw57LJo1_Gl7RlS5VrgMbNcEGFmiupI_U_9s'
    pics_range = 'PicsData'
    pics_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=reward_picsId, range=pics_range).execute()
    pics_data = pics_result.get('values', [])

    if not pics_data:
        return -1

    # Required url format
    # https://docs.google.com/uc?id=0B4yfJJJSNrfuelE1QXlxWjlJcUE
    url_prefix = 'https://docs.google.com/uc?id='
    reward_pics = {}
    for reward in pics_data:
        if reward[1]:
            reward_pics[reward[0]] = url_prefix+reward[1]
        else:
            reward_pics[reward[0]] = ''

    return reward_pics


"""
Get the Google Sheet transaction data for a specific girl as defined in session. 
The function will get data from 2018 Cookies. 
The function return a list of lists for the transaction data set
TODO Get query to work according to https://developers.google.com/chart/interactive/docs/querylanguage#setting-the-query-in-the-data-source-url
     and https://developers.google.com/chart/interactive/docs/spreadsheets#authorization
     There is a problem getting authentication for the spreadsheet in the https request
"""
def get_girl_transactions(girl_name, today):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_range = 'Data'
    trans_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId,
        range=data_range).execute()
    trans_list = trans_result.get('values', [])

    if not trans_list:
        return -1

    transactions = []
    for transaction in trans_list:
        # if transaction[3] == girl_name and datetime.strptime(transaction[0], '%m/%d/%Y') < datetime.strptime('2/20/2017', '%m/%d/%Y'):
        if transaction[3] == girl_name and datetime.strptime(transaction[0], '%m/%d/%Y') < today:
          transactions.append(transaction[:])

    if transactions == {}:
        return -2
    return transactions


"""
Get the Google Sheet transaction data for a specific girl as defined in session. 
The function will get data from 2018 Cookies. 
The function return a list of lists for the transaction data set
TODO Get query to work according to https://developers.google.com/chart/interactive/docs/querylanguage#setting-the-query-in-the-data-source-url
     and https://developers.google.com/chart/interactive/docs/spreadsheets#authorization
     There is a problem getting authentication for the spreadsheet in the https request
"""
def get_all_transactions(tempdate):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    fileId = '1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A'
    data_range = 'Data'
    trans_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=fileId,
        range=data_range).execute()
    trans_list = trans_result.get('values', [])

    if not trans_list:
        return -1

    transactions = []
    for transaction in trans_list:
        if (transaction[0] != 'Date' and transaction[0] != ''):
            # if datetime.strptime(transaction[0], '%m/%d/%Y') < datetime.strptime('2/20/2017', '%m/%d/%Y'):
            if datetime.strptime(transaction[0], '%m/%d/%Y') <= tempdate:
                transactions.append(transaction[:])

    if transactions == {}:
        return -2
    return transactions
