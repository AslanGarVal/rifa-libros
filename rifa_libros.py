from __future__ import print_function
#setup for authentication and credentials
import os.path
from os import environ
from dotenv import dotenv_values, load_dotenv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
#setup for processing
import pandas as pd
import numpy as np

#env_path = os.path.join(os.path.dirname(__file__), ".env")
#dotenv_values(env_path)
load_dotenv()

print(environ.get("SPREADSHEET_ID"))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


