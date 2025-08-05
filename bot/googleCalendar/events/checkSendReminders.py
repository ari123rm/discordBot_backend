# No seu script que contém a função checkSendReminders()

import discord
import os
import asyncio
from bot import bot
from logs import log_critical_error, log_info
from dotenv import load_dotenv
load_dotenv() 

from googleCalendar.functions.getCalendarService import getCalendarService as get_calendar_service
from googleCalendar.functions.getUpcomingEvents import getUpcomingEvents as get_upcoming_events

from googleCalendar.functions.getCalendarService import creds


REMINDER_CHANNEL_ID = int( os.getenv("REMINDER_CHANNEL_ID"))

async def checkSendReminders():
    """
    Função principal que verifica os eventos e envia os lembretes.
    Ela será executada a cada 24 horas.
    """
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            log_info("Verificando eventos na Google Agenda...")
            
            # Executa a função síncrona em um thread separado
            service = await asyncio.to_thread(get_calendar_service)
            events = await asyncio.to_thread(get_upcoming_events, service)
            
            channel = bot.get_channel(REMINDER_CHANNEL_ID)
            if channel is None:
                log_critical_error(f"Erro: Canal com ID {REMINDER_CHANNEL_ID} não encontrado.")
                continue

            if not events:
                log_info("Nenhum evento encontrado para amanhã.")
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    message = f"📢 **Lembrete de Evento para Amanhã:**\n" \
                              f"**Título:** {event['summary']}\n" \
                              f"**Horário:** {start}\n"
                    
                    await channel.send(message)
            
        except Exception as e:
            log_critical_error(f"Ocorreu um erro: {e}")

        # Espera 24 horas antes de verificar novamente
        await asyncio.sleep(24 * 60 * 60)