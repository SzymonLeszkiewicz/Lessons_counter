"""Google Calendar API authentication and events retrieval."""
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build


def authenticate_google_calendar():
    """Authenticate Google Calendar API and return service object.

    Args: None
    Returns:
        ""service"" (obj): Google Calendar service object.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost:8080/'
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(service, calendar_id, month, year):
    """Get events from Google Calendar in a given month and year.

    Args:
        ''service'' (obj): Google Calendar service object.
        ''calendar_id'' (str): Google Calendar ID.
        ''month'' (int): Month number.
        ''year'' (int): Year number.
    Returns:
        ''events'' (list): List of events in a given month and year.
    """
    print(f'Getting events for {month}/{year}, calendar: {calendar_id}')
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=31)
    end_date = end_date.replace(day=1)

    # Konwersja do formatu RFC3339
    time_min = start_date.isoformat() + 'Z'
    time_max = end_date.isoformat() + 'Z'

    events_result = service.events().list(calendarId=calendar_id,
                                          timeMin=time_min, timeMax=time_max,
                                          maxResults=2500, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def list_calendars(service):
    """List all available calendars.

    Args:
        ''service'' (obj): Google Calendar service object.
    Returns:
        ''calendarts_list'' (list): List of calendars.
    """
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    if not calendars:
        return 'No calendars found.'
    else:
        calendarts_list = []
        for calendar in calendars:
            calendarts_list.append(calendar['summary'])
        return calendarts_list
