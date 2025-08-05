from googleapiclient.discovery import build

from googleapiclient.discovery import Resource
from googleCalendar.calendar import creds
def getCalendarService() -> Resource:
    """
    Conecta-se à API do Google Agenda e retorna o objeto de serviço.
    
    Esta função autentica as credenciais e constrói um cliente da API do Google Calendar.

    Returns:
        Resource: O objeto de serviço para interagir com a API do Google Agenda.
    """
    service = build('calendar', 'v3', credentials=creds)
    return service