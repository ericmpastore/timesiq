import datetime as dt
import time
import tkinter as tk
from tkinter import messagebox

def get_calendar():
    """
    Docstring for get_calendar

    Future: Will pull next time block from Google Calendar using API
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