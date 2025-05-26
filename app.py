from flask import Flask, Response
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Define the Google Sheets access scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate using the credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# ✅ Your actual master Google Sheet name
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
