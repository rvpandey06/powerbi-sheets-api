from flask import Flask, Response
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

app = Flask(__name__)

def get_gspread_client():
    # Load credentials from environment variable
    google_creds_json = os.environ.get("GOOGLE_CREDS")

    if not google_creds_json:
        raise Exception("GOOGLE_CREDS environment variable not set.")

    creds_dict = json.loads(google_creds_json)

    # Set up credentials
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    return client

@app.route('/')
def export_csv():
    try:
        client = get_gspread_client()

        # Open your Google Sheet by name and worksheet name
        spreadsheet = client.open("Your Google Sheet Name")  # 🔁 Replace with your actual sheet name
        worksheet = spreadsheet.worksheet("Sheet1")          # 🔁 Replace with actual worksheet if needed

        data = worksheet.get_all_values()

        if not data:
            return "No data found in the Google Sheet.", 404

        df = pd.DataFrame(data[1:], columns=data[0])  # Skip header row for data, use row 0 as column names
        csv_data = df.to_csv(index=False)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"}
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
