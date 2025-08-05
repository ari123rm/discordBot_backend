import discord
import os
import asyncio
from bot import bot
from logs import log_critical_error, log_info
from dotenv import load_dotenv
load_dotenv() 

from googleCalendar.functions.getCalendarService import getCalendarService as get_calendar_service
from googleCalendar.functions.getUpcomingEvents import getUpcomingEvents 

from googleCalendar.functions.getCalendarService import creds

REMINDER_CHANNEL_ID = int( os.getenv("REMINDER_CHANNEL_ID"))

from datetime import datetime, timedelta, timezone
import pytz 

# Use o fuso horário correto para sua região
TIMEZONE = pytz.timezone("America/Sao_Paulo") 

# Crie sets para rastrear os lembretes enviados para evitar repetição
one_hour_reminders_sent = set()
five_minutes_reminders_sent = set()

async def checkUrgentReminders():
    await bot.wait_until_ready()
    
    # Executa a cada 1 minuto
    while not bot.is_closed():
        try:
            
            service = await asyncio.to_thread(get_calendar_service)
            
            now = datetime.now(TIMEZONE)
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)
            
            # Use o método recomendado para lidar com fusos horários e UTC
            time_min_str = start_of_day.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            time_max_str = end_of_day.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            
            events = await asyncio.to_thread(getUpcomingEvents, service, time_min=time_min_str, time_max=time_max_str)
            
            channel = bot.get_channel(REMINDER_CHANNEL_ID)
            if channel is None:
                log_critical_error(f"Erro: Canal com ID {REMINDER_CHANNEL_ID} não encontrado.")
                continue

            if events:
                for event in events:
                    start_str = event['start'].get('dateTime')
                    if not start_str:
                        continue 

                    event_id = event['id']
                    event_time = datetime.fromisoformat(start_str).astimezone(TIMEZONE)
                    time_diff = event_time - now
                    
                    one_hour_before = timedelta(hours=1)
                    five_minutes_before = timedelta(minutes=5)

                    message = None
                    # Lembrete de 1 hora antes
                    # O "and event_id not in one_hour_reminders_sent" evita a repetição
                    if timedelta(minutes=55) < time_diff <= one_hour_before and event_id not in one_hour_reminders_sent:
                        message = f"⏰ **Lembrete: Daqui a 1 hora!**\n" \
                                  f"**Título:** {event['summary']}\n" \
                                  f"**Horário:** {event_time.strftime('%H:%M')}"
                        one_hour_reminders_sent.add(event_id)
                    
                    # Lembrete na hora do evento
                    # O "and event_id not in five_minutes_reminders_sent" evita a repetição
                    elif timedelta(minutes=0) < time_diff <= five_minutes_before and event_id not in five_minutes_reminders_sent:
                        message = f"🚨 **Lembrete: O evento começa em breve!**\n" \
                                  f"**Título:** {event['summary']}\n" \
                                  f"**Horário:** {event_time.strftime('%H:%M')}"
                        five_minutes_reminders_sent.add(event_id)

                    if message:
                        await channel.send(message)
        
        except Exception as e:
            log_critical_error(f"Ocorreu um erro em checkUrgentReminders: {e}")

        # Espera 1 minuto antes de verificar novamente
        await asyncio.sleep(60)