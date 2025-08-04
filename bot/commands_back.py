import discord
import sys
from bot import bot
import logs  # Importa o módulo de logs para usar as funções de log


# --- FUNÇÕES DE COMANDO DO BOT ---
async def send_message_to_channel(data):
    """
    Função para enviar uma mensagem para um canal específico.
    Retorna um dicionário com o status da operação ou levanta uma exceção em caso de erro.
    """
    try:
        channel_id = int(data.get('channel_id'))
        message = data.get('message', 'Mensagem padrão.')
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
            # Não loga sucesso aqui, a resposta será enviada via stdin_listener
            return {"status": "success", "channel_id": channel_id, "message_sent": message}
        else:
            error_msg = f"Erro: Canal com ID {channel_id} não encontrado."
            # Usa log_error para enviar o erro
            raise ValueError(error_msg) # Levanta uma exceção para ser capturada no stdin_listener
    except (ValueError, TypeError) as e:
        error_msg = f"Erro nos dados para 'send_message': {e}"
        raise ValueError(error_msg) # Levanta a exceção
    except Exception as e:
        error_msg = f"Erro inesperado ao enviar mensagem: {e}"
        raise Exception(error_msg) # Levanta a exceção

# --- DICIONÁRIO DE COMANDOS ---
COMMANDS = {
    'send_message': send_message_to_channel,
    # Adicione outros comandos aqui
    # 'kick_user': kick_user_function, 
}