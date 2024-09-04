from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os.path
import json

# Scopes nécessaires pour lire et écrire dans Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    # Le fichier token.json stocke les tokens d'accès de l'utilisateur.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si il n'existe pas de token valide, demande à l'utilisateur de se connecter
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Enregistre les credentials pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Date de début et de fin pour chercher les événements
    start_date = datetime.datetime(2024, 1, 1, 0, 0, 0).isoformat() + 'Z'  # 'Z' indique UTC time
    end_date = datetime.datetime(2026, 1, 1, 0, 0, 0).isoformat() + 'Z'


    # Lister les calendriers accessibles
    calendar_list_result = service.calendarList().list().execute()
    calendars = calendar_list_result.get('items', [])

    for calendar in calendars:
        print(f"ID: {calendar['id']}, Summary: {calendar['summary']}")

    # Appeler l'API pour lister les événements
    events_result = service.events().list(calendarId='family01788173089440970045@group.calendar.google.com', timeMin=start_date, timeMax=end_date,singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    i = 0
    for event in events:
        # if "LABO" in event['summary']:
        if event["creator"]["email"] == "electriklara05@gmail.com":
            i += 1
            # print(json.dumps(event))
            print(f"{i}")
            print(f"Suppression de l'événement : {event['summary']}")
            service.events().delete(calendarId='family01788173089440970045@group.calendar.google.com', eventId=event['id']).execute()
            # break
            # exit()
    print(f"Number ellement to deleted : {i}")

    # Filtrer et supprimer les événements par mot-clé dans le titre
    # keyword = "Mot-clé"
    # for event in events:
    #     if keyword in event['summary']:
    #         print(f"Suppression de l'événement : {event['summary']}")
    #         service.events().delete(calendarId='primary', eventId=event['id']).execute()

if __name__ == '__main__':
    main()