# commands/commands.py
import discord
import os
import importlib
from bot import bot
from google.oauth2.credentials import Credentials
# This dictionary will store all the loaded command modules.
events_bot = {}
from dotenv import load_dotenv # Importe a função
load_dotenv() 
CALENDAR_ID = os.getenv("CALENDAR_ID")  
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('token.json', SCOPES) 

async def load_calendar(dir):
    """
    Loads all commands dynamically from a directory and stores them in the global 'commands' dictionary.
    """
    # The path to the directory is relative to the project root.
    backend_dir_path = f'bot/googleCalendar/{dir}'

    # Check if the directory exists.
    if not os.path.isdir(backend_dir_path):
        print(f"Command directory '{backend_dir_path}' not found.")
        return

    # Create a sub-dictionary for the given directory if it doesn't already exist.
    if dir not in events_bot:
        events_bot[dir] = {}

    # Iterate over the files in the directory.
    for filename in os.listdir(backend_dir_path):
        # Ensure we're only loading .py files and ignoring __init__.py.
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            try:
                # Import the module dynamically using the full package path.
                module = importlib.import_module(f'googleCalendar.{dir}.{module_name}')
                
                print(f"Module '{module_name}' loaded successfully.")
                
                # Store the loaded module in the global 'commands' dictionary.
                events_bot[dir][module_name] = module.__getattribute__(module_name)
            
            except ImportError as e:
                print(f"Error importing module '{module_name}': {e}")
            except Exception as e:
                print(f"Unexpected error processing module '{module_name}': {e}")

async def create_events_task():

    for event_name, event_func in events_bot["events"].items():
        bot.loop.create_task(event_func())


async def calendar():
    await load_calendar("events")
    await load_calendar("commands")

    await create_events_task()