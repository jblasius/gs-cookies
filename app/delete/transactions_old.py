from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
# from app import app
from config import SERVICE_KEY
from datetime import datetime

"""
Get the Google Sheet transaction data for a specific girl as defined in session. 
The function will get data from 2018 Cookies. 
The function return a list of lists for the transaction data set
TODO Get query to work according to https://developers.google.com/chart/interactive/docs/querylanguage#setting-the-query-in-the-data-source-url
     and https://developers.google.com/chart/interactive/docs/spreadsheets#authorization
     There is a problem getting authentication for the spreadsheet in the https request
"""
def get_transactions(girl_name):

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
        if transaction[3] == girl_name and datetime.strptime(transaction[0], '%m/%d/%Y') < datetime.strptime('2/20/2017', '%m/%d/%Y'):
          transactions.append(transaction[:])

    if transactions == {}:
        return -2
    return transactions
