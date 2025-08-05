# events/calendar/commands/create_event.py

import discord
from discord.ext import commands
from google.oauth2.credentials import Credentials
import datetime
import asyncio
from googleCalendar.functions.getCalendarService import getCalendarService as get_calendar_service

# Define the Cog class
class CalendarEvents(commands.Cog):
    def __init__(self, bot: commands.Bot, creds: Credentials, calendar_id: str):
        self.bot = bot
        self.creds = creds
        self.calendar_id = calendar_id

    @discord.app_commands.command(name="create_event")
    @discord.app_commands.describe(
        titulo="O título do evento.",
        data_inicio="Data e hora de início (DD/MM/AAAA HH:MM).",
        data_fim="Data e hora de término (DD/MM/AAAA HH:MM).",
        descricao="Uma descrição para o evento (opcional)."
    )
    async def create_event(
        self,
        interaction: discord.Interaction,
        titulo: str,
        data_inicio: str,
        data_fim: str,
        descricao: str = None
    ):
        """Cria um novo evento no Google Agenda."""
        await interaction.response.defer(thinking=True)

        try:
            start_dt = datetime.datetime.strptime(data_inicio, "%d/%m/%Y %H:%M")
            end_dt = datetime.datetime.strptime(data_fim, "%d/%m/%Y %H:%M")

            if start_dt >= end_dt:
                await interaction.followup.send("❌ A data/hora de início deve ser anterior à data/hora de término.")
                return

            service = await asyncio.to_thread(get_calendar_service, self.creds)

            event = {
                'summary': titulo,
                'description': descricao,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'America/Fortaleza',
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'America/Fortaleza',
                },
            }

            created_event = await asyncio.to_thread(
                service.events().insert(calendarId=self.calendar_id, body=event).execute
            )

            event_link = created_event.get('htmlLink')
            response_message = (
                f"✅ Evento '{titulo}' criado com sucesso!\n"
                f"📅 Início: {start_dt.strftime('%d/%m/%Y %H:%M')}\n"
                f"⏰ Fim: {end_dt.strftime('%d/%m/%Y %H:%M')}\n"
                f"🔗 Link: {event_link}"
            )
            await interaction.followup.send(response_message)

        except ValueError:
            await interaction.followup.send("❌ Formato de data/hora inválido. Use DD/MM/AAAA HH:MM (ex: 05/08/2025 14:30).")
        except Exception as e:
            print(f"Erro ao criar evento: {e}")
            await interaction.followup.send(f"❌ Ocorreu um erro ao criar o evento. Detalhes: `{e}`")