from __future__ import print_function
#setup para autenticacion y credenciales
import os.path
from os import environ
from dotenv import dotenv_values, load_dotenv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
#setup para procesamiento
import pandas as pd
import numpy as np


load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = environ.get("SPREADSHEET_ID")
SPREADSHEET_RANGE = environ.get("SPREADSHEET_RANGE")
TOKEN_NAME = environ.get("TOKEN")

def get_credentials(scopes, token_name):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # Si no hay credenciales validas, permite al usuario loguearse
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                token_name, scopes)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para corridas posteriores
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_data(creds):
    service = build('sheets', 'v4', credentials = creds)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId = SPREADSHEET_ID, range = SPREADSHEET_RANGE).execute()
    values = result.get('values', [])

    df = pd.DataFrame(values[1:], columns = values[0])
    return df

def sortear(df):
    df2 = df.assign(Titulos = df["¿Qué títulos te interesan?"].map(lambda s: s.split(","))).\
        drop(columns = "¿Qué títulos te interesan?").explode("Titulos") 
    grouped_titles = df2.groupby("Titulos")

    sorteados = []
    libros = []
    libros_sorteados = {}
    for title in grouped_titles:
        libro = title[0]
        candidatos = list(title[1]["Contacto (mail, teléfono, fb, lo que sea realmente)"])
        sorteado = np.random.choice(candidatos)
    
        repetido = True
        while repetido:
            #print(candidatos)
            if sorteado not in sorteados:
                sorteados.append(sorteado)
                libros.append(libro)
                break
            if candidatos.remove(sorteado) is not None:
                sorteado = np.random.choice(candidatos.remove(sorteado))
            else: 
                break
    
    libros_sorteados["libros"] = libros
    libros_sorteados["sorteados"] = sorteados

    df3 = pd.DataFrame(libros_sorteados)
    return df3

def main():
    creds = get_credentials(SCOPES, TOKEN_NAME)
    data = get_data(creds)
    sorteados = sortear(data)

    print(sorteados)

if __name__ == "__main__":
    main()