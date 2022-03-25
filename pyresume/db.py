import json
import os.path

from config import get_settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

settings = get_settings()


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                settings.credentials, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_database():
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def extract_data(sheet, page: str) -> list:
    result = (
        sheet.values()
        .get(spreadsheetId=settings.spreadsheet, range=page)
        .execute()
    )
    values = iter(result.get("values", []))
    if not values:
        print("No data found.")
        return []

    headers = next(values, [])
    data_rows = []
    for row in values:
        data = {}
        for cell_pos, cell in enumerate(row):
            if headers[cell_pos].endswith("_json"):
                cell = json.loads(cell)
            data[headers[cell_pos]] = cell
        data_rows.append(data)
    return data_rows


def get_resume(sheet) -> dict:
    target_spreadsheet = sheet.get(spreadsheetId=settings.spreadsheet).execute()
    resume_sessions = (
        s["properties"]["title"] for s in target_spreadsheet["sheets"]
    )
    return {
        session: extract_data(sheet, session) for session in resume_sessions
    }
