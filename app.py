from flask import Flask, Response
import gspread
import pandas as pd
import os
import json
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Define the Google Sheets access scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Read credentials JSON string from environment variable
credentials_info = os.getenv("GOOGLE_CREDENTIALS_JSON")
credentials_dict = json.loads(credentials_info)

# Authenticate using credentials dict
creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
client = gspread.authorize(creds)

# Your actual master Google Sheet name
SHEET_NAME = "Master Sales Data"

@app.route('/')
def home():
    return '✅ Google Sheets to Power BI API is running!'

@app.route('/data')
def get_data():
    try:
        sheet = client.open(SHEET_NAME).sheet1      # Open your Google Sheet
        data = sheet.get_all_records()              # Fetch all rows
        df = pd.DataFrame(data)                     # Convert to DataFrame
        csv_data = df.to_csv(index=False)           # Convert to CSV format

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=data.csv"}
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
