import datetime
import os
import asyncio
from googleCalendar.calendar import CALENDAR_ID

# A função agora recebe time_min e time_max como parâmetros opcionais
def getUpcomingEvents(service, time_min=None, time_max=None):
    """
    Busca eventos em um intervalo de tempo específico e os retorna.
    Se time_min e time_max não forem fornecidos, busca eventos para o dia seguinte.
    A função retorna uma lista de dicionários com os eventos.
    """
    # Se os parâmetros não forem fornecidos, usa a lógica original para o dia seguinte
    if time_min is None or time_max is None:
        tomorrow_start = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        ).isoformat() + 'Z'
        tomorrow_end = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).replace(
            hour=23, minute=59, second=59, microsecond=0
        ).isoformat() + 'Z'
        time_min = tomorrow_start
        time_max = tomorrow_end

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])