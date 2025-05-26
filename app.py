from flask import Flask, Response
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Set up credentials and scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

@app.route('/')
def export_csv():
    # Open the Google Sheet
    sheet = client.open("Your Google Sheet Name").worksheet("Sheet1")
    
    # Get all data as list of lists
    data = sheet.get_all_values()

    # Convert to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert to CSV
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
