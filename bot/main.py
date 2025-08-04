# bot/main.py

import discord
import asyncio
import sys
import threading
import json
from bot import bot, BOT_TOKEN  
from commands_back import COMMANDS
import commands_user
import events  

# --- FUNÇÃO QUE ESCUTA OS COMANDOS DO NODE.JS ---
def stdin_listener():
    """
    Executa em uma thread separada para escutar o stdin sem bloquear o bot.
    """
    for line in sys.stdin:
        try:
            # Tenta decodificar a linha como JSON
            command_data = json.loads(line)
            action = command_data.get('action')
            data = command_data.get('data')

            print(f"Comando recebido: action={action}, data={data}")

            if action in COMMANDS:
                # Pega a função correspondente do dicionário
                coro = COMMANDS[action](data)
                
                # Executa a função assíncrona de forma segura na event loop principal do bot
                future = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                future.result() # Você pode esperar o resultado se precisar

        except json.JSONDecodeError:
            print(f"Erro: Recebido dado inválido (não é JSON): {line.strip()}")
        except Exception as e:
            print(f"Erro ao processar comando do stdin: {e}")

@bot.event
async def on_ready():
    print(f'Bot logado como {bot.user}')
    print('Bot está pronto para receber comandos do painel.')

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    # Inicia a thread que escuta o stdin em background
    listener_thread = threading.Thread(target=stdin_listener, daemon=True)
    listener_thread.start()

    # Inicia o bot
    try:
        bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure:
        print("Erro: Token do bot inválido. Verifique seu token.")
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar o bot: {e}")