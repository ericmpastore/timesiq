import datetime as dt
import time
import tkinter as tk
import os.path
from tkinter import messagebox

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar():
    """
    Docstring for get_calendar

    Future: Will pull next time block from Google Calendar using API
    """

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
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
        now = dt.datetime.now(tz=dt.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")

def show_window():
    """
    Docstring for show_window

    Future: Will replace show_alert and show a running timer on the desktop rather than a pop-up
    """

def show_alert(title:str,message:str):
    """
    Docstring for show_alert

    Shows a pop up displaying timebox alerts to the user
    
    EPastore, 12/30/2025
    
    :param title: Display title for the title of the window
    :type title: str
    :param message: Message displayed by the popup
    :type message: str
    """
    root = tk.Tk() #instantiate the root window
    root.withdraw() #hide the root window
    root.attributes("-topmost", True) #show messagebox at front
    try:
        messagebox.showinfo(title,message,parent=root) #show the messagebox with title and message
    finally:
        root.destroy() #destroy the root window

def main(poll_seconds: float=1.0):
    """
    Docstring for main

    Runs the program when the user opens the python file or launches from CLI
    
    Epastore, 12/30/2025

    """
    last_50_mins = None
    last_55_mins = None
    last_60_mins = None

    print("TimeSiq is running. Press Ctrl-C in the console or close the application to quit.")

    while True:
        now = dt.datetime.now()
        minute = now.minute
        hour = now.hour
        day_key = now.date()

        hour_key = (day_key, hour)

        try: 
            #10 minute warning
            if minute == 50 and last_50_mins != hour_key:
                last_50_mins = hour_key
                show_alert("Time Block Warning: 10 Minutes Left",f"The time is {now.strftime('%I:%M %p')}. You have 10 minutes left in the current time block. \n Finish your current task and prepare to move to the next task.")
                print(f"The time is {now.strftime('%I:%M %p')}. You have 10 minutes left in the current time block. \n Finish your current task and prepare to move to the next task.")

            #5 minute warning
            elif minute == 55 and last_55_mins != hour_key:
                last_55_mins = hour_key
                show_alert("Time Block Warning: 5 Minutes Left",f"The time is {now.strftime('%I:%M %p')}. You have 5 minutes left in the current time block. \n Finish your current task and prepare to move to the next task.")
                print(f"The time is {now.strftime('%I:%M %p')}. You have 5 minutes left in the current time block. \n Finish your current task and prepare to move to the next task.")

            #hour warning, time to change
            elif minute == 60 and last_60_mins != hour_key:
                last_60_mins = hour_key
                show_alert("Time Block Complete",f"The time is {now.strftime('%I:%M %p')}. The current time block is complete. \n Move to the next task.")
                print(f"The time is {now.strftime('%I:%M %p')}. The current time block is complete. \n Move to the next task.")

        except tk.TclError as e:
            print(f"Popup Error: {e}")

        time.sleep(poll_seconds)

if __name__ == "__main__":
    main()