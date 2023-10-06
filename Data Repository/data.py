import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('D:\Data Repository\data-project-2023-401215-446700756266.json.', scope)
client = gspread.authorize(credentials)

# Open the Google Sheets document by URL
url = "https://docs.google.com/spreadsheets/d/1eRujNQYov-tZ8j9yvkah6lSzJOpNweMF/edit"
sheet = client.open_by_url(url).sheet1

# Get all the data from the sheet
data = sheet.get_all_records()

# Helper function to parse time strings to datetime objects
def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Analyze the data
for row in data:
    name = row['Name']
    shifts = row['Shifts'].split(', ')

    for i in range(len(shifts) - 6):
        consecutive_days = 0
        total_hours = 0

        for j in range(i, i + 7):
            start_time, end_time = shifts[j].split('-')
            start_time = parse_time(start_time)
            end_time = parse_time(end_time)
            hours_worked = (end_time - start_time).total_seconds() / 3600
            total_hours += hours_worked

            if hours_worked > 14:
                print(f"{name} worked for more than 14 hours on {start_time.date()}.")
                break

            if hours_worked < 10 and hours_worked > 1:
                print(f"{name} worked less than 10 hours between shifts on {start_time.date()}.")
                break

            if hours_worked >= 10:
                consecutive_days += 1
            else:
                break

        if consecutive_days == 7:
            print(f"{name} worked 7 consecutive days starting on {start_time.date()}.")

