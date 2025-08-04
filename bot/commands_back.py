import discord
from bot import bot


async def send_message_to_channel(data):
    """Função para enviar uma mensagem para um canal específico."""
    try:
        channel_id = int(data.get('channel_id'))
        message = data.get('message', 'Mensagem padrão.')
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
            print(f"Mensagem enviada para o canal {channel_id}")
        else:
            print(f"Erro: Canal com ID {channel_id} não encontrado.")
    except (ValueError, TypeError) as e:
        print(f"Erro nos dados para 'send_message': {e}")
    except Exception as e:
        print(f"Erro inesperado ao enviar mensagem: {e}")



COMMANDS = {
    'send_message': send_message_to_channel,
    
    # Adicione outros comandos aqui
    # 'kick_user': kick_user_function, 
}