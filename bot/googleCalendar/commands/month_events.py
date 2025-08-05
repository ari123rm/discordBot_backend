import datetime
import asyncio

from googleapiclient.discovery import build
import discord
from bot import bot
from googleCalendar.calendar import creds, CALENDAR_ID

@bot.tree.command()
async def month_events(
    interaction: discord.Interaction
):
    """
    Lista todos os eventos do Google Agenda para o mês atual.

    Args:
        interaction (discord.Interaction): O objeto de interação do Discord.

    Returns:
        None
    """
    try:
        await interaction.response.defer() # Defer a resposta para que o bot não expire antes de buscar os eventos

        # Obter a data atual
        now = datetime.datetime.now()

        # Calcular o primeiro dia do mês atual
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calcular o último dia do mês atual
        # Para isso, vamos para o primeiro dia do próximo mês e subtraímos um microssegundo
        if now.month == 12:
            last_day_of_month = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(microseconds=1)
        else:
            last_day_of_month = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(microseconds=1)

        # Obter o serviço da Google Agenda
        service = build('calendar', 'v3', credentials=creds)

        # Fazer a requisição para listar os eventos
        # Usamos asyncio.to_thread para executar a chamada bloqueante da API em um thread separado
        events_result = await asyncio.to_thread(
            service.events().list,
            calendarId=CALENDAR_ID,
            timeMin=first_day_of_month.isoformat() + 'Z',  # 'Z' indica UTC
            timeMax=last_day_of_month.isoformat() + 'Z',  # 'Z' indica UTC
            singleEvents=True,
            orderBy='startTime'
        )
        events = events_result.execute().get('items', [])

        if not events:
            await interaction.followup.send("🗓️ Não há eventos agendados para este mês.",ephemeral=True)
            return

        # Construir a mensagem com os eventos
        response_message = "🗓️ **Eventos para o mês de " + now.strftime("%B de %Y") + ":**\n\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Formatar as datas para exibição
            if 'dateTime' in event['start']:
                start_dt = datetime.datetime.fromisoformat(start)
                end_dt = datetime.datetime.fromisoformat(end)
                
                # As datas já devem vir com o fuso horário correto da API ou em UTC,
                # e fromisoformat() as interpreta corretamente.
                # Não é necessário subtrair horas manualmente aqui, pois isso causaria um ajuste duplo.
                formatted_start = start_dt.strftime("%d/%m/%Y %H:%M")
                formatted_end = end_dt.strftime("%d/%m/%Y %H:%M")
            else: # Evento de dia inteiro
                formatted_start = datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
                formatted_end = datetime.datetime.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")


            summary = event['summary']
            description = event.get('description', 'Sem descrição')
            
            response_message += f"**{summary}**\n"
            response_message += f"  📅 Início: {formatted_start}\n"
            response_message += f"  🏁 Fim: {formatted_end}\n"
            response_message += f"  📝 Descrição: {description}\n\n"
        
        await interaction.followup.send(response_message,ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"❌ Ocorreu um erro ao listar os eventos: {e}",ephemeral=True)

