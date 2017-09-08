from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
# from app import app
from config import SERVICE_KEY

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


