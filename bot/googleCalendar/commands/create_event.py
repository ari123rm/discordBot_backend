import datetime
import asyncio

from googleapiclient.discovery import build
import discord
from bot import bot
from googleCalendar.calendar import creds,CALENDAR_ID
@bot.tree.command()
async def create_event(
    interaction:discord.Interaction,

    titulo: str,
    data_inicio: str,
    data_fim: str,
    descricao: str = None
):
    """
    Cria um evento no Google Agenda.

    Args:
        titulo (str): O título do evento.
        data_inicio (str): A data e hora de início do evento no formato DD/MM/AAAA HH:MM.
        data_fim (str): A data e hora de término do evento no formato DD/MM/AAAA HH:MM.
        descricao (str, opcional): Uma descrição para o evento.

    Returns:
        dict: O evento criado retornado pela API do Google Agenda, ou None em caso de erro.
    """
    try:
        # Analisar as strings de data e hora
        start_dt = datetime.datetime.strptime(data_inicio, "%d/%m/%Y %H:%M")
        end_dt = datetime.datetime.strptime(data_fim, "%d/%m/%Y %H:%M")

        # Validação básica de datas
        if start_dt >= end_dt:
            await interaction.response.send_message("❌ A data/hora de início deve ser anterior à data/hora de término.",ephemeral=True)
            return None

        # Obter o serviço da Google Agenda
        service = build('calendar', 'v3', credentials=creds)

        # Estrutura do evento para a API do Google Agenda
        event = {
            'summary': titulo,
            'description': descricao,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'America/Fortaleza',  # Ajuste para o fuso horário desejado
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'America/Fortaleza',  # Ajuste para o fuso horário desejado
            },
        }

        # Inserir o evento no calendário
        created_event = await asyncio.to_thread(
            service.events().insert,
            calendarId=CALENDAR_ID,
            body=event
        )

        created_event.execute()
        await interaction.response.send_message(f"Evento criado com sucesso",ephemeral=True) 

    except ValueError:
        await interaction.response.send_message("❌ Formato de data/hora inválido. Use DD/MM/AAAA HH:MM (ex: 05/08/2025 14:30).",ephemeral=True)
        return None
    except Exception as e:
        await interaction.response.send_message(f"❌ Ocorreu um erro ao criar o evento: {e}",ephemeral=True)
        return None 