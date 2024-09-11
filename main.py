import os
import requests
from flask import Flask, request, jsonify
import gspread
from google.oauth2.gdch_credentials import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/update_exchange_rate', methods=['GET'])
def update_exchange_rate():
    # Get parameters
    update_from = request.args.get('update_from', default=datetime.now().strftime('%Y%m%d'))
    update_to = request.args.get('update_to', default=datetime.now().strftime('%Y%m%d'))

    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('neat-veld-435215-t2-c04d86e537db.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = client.open("https://docs.google.com/spreadsheets/d/1y42L4u2hKywqWI92vj9AnekNxUeSbxzQmbjORxQ2JPc/edit?gid=0#gid=0").sheet1

    # Fetch exchange rate data from API for each date in the range
    current_date = datetime.strptime(update_from, '%Y%m%d')
    end_date = datetime.strptime(update_to, '%Y%m%d')
    while current_date <= end_date:
        response = requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={current_date.strftime("%Y%m%d")}&json')
        data = response.json()

        # Update Google Sheet with data
        for item in data:
            row = [current_date.strftime('%Y-%m-%d'), item['cc'], item['rate']]
            sheet.append_row(row)

        current_date += timedelta(days=1)

    return 'Exchange rates updated successfully!'

if __name__ == '__main__':
    app.run(debug=True)

print()































