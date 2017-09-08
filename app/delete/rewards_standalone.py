#
# https://developers.google.com/api-client-library/python/auth/service-accounts
#
#from flask import current_app, redirect, url_for, request, session
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
#from app import app


scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '../service_key.json', scopes)

http_auth = credentials.authorize(Http())

service = build('sheets', 'v4', http=http_auth)

spreadsheetId = '1oiIxf5Nti1fIRV00eBHaDgJonJkGrrwp18yQNukzyzk'
header_range = 'RewardLevels'
data_range = 'RewardChoices_Amber'

result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetId, range=header_range).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    for value in values:
        print value


