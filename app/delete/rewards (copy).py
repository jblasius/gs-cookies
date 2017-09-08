import re
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
from app import app
from config import SERVICE_KEY

"""
Get the Google Sheet data for a particualr girl's reward choices. 
The function will get data from 2018 Rewards Tracking. 
The function return a list of lists.
    reward_choices[0] = reward category
    reward_choices[1] = reward choice, long name
During testing only the specified data range is returned.
//TODO: Make the retrieval smart and filter the data given the girl's name.
"""
def get_reward_choices(girl_name):

    sheet_scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_KEY, sheet_scope)

    http_auth = credentials.authorize(Http())
    sheets_service = build('sheets', 'v4', http=http_auth)

    spreadsheetId = '1oiIxf5Nti1fIRV00eBHaDgJonJkGrrwp18yQNukzyzk'
    data_range = 'TestRange'
    rewards_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=data_range,
        majorDimension='COLUMNS').execute()
    reward_choices = rewards_result.get('values', [])

    if not reward_choices:
        return -1
    else:
        return reward_choices


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

    # Incoming url
    # https://drive.google.com/file/d/0BzC5F6zg91g4bWRVcHJBa0Z3UEk/view?usp=drivesdk
    #
    # Desired Outgoing url
    # https://docs.google.com/uc?id=0B4yfJJJSNrfuelE1QXlxWjlJcUE
    url_prefix = 'https://docs.google.com/uc?id='
    reward_pics = {}
    for reward in pics_data:
        match = re.search(r'(https://drive.google.com/file/d/)(\w+)(/view.+)', reward[1])
        if match:
            reward_pics[reward[0]] = url_prefix+match.group(2)
        else:
            reward_pics[reward[0]] = ''

    return reward_pics


