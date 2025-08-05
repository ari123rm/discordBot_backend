import discord
import asyncio
import sys
import threading
import json
import os
from logs import log_success, log_error, log_info, log_critical_error # Importa as funções de log

current_dir = os.path.dirname(os.path.abspath(__file__))
from bot import bot, BOT_TOKEN ,setup_bot
from commands.commands_bot import load_commands, commands_bot
from events.events import load_events, create_events_task
from googleCalendar.calendar import calendar


if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


# --- FUNÇÃO QUE ESCUTA OS COMANDOS DO NODE.JS ---
def stdin_listener():
    """
    Executa em uma thread separada para escutar o stdin sem bloquear o bot.
    Processa comandos JSON recebidos via stdin e envia respostas JSON via stdout/stderr.
    """
    for line in sys.stdin:
        # Inicializa request_id como None para garantir que sempre tenha um valor
        request_id = None 
        try:
            # Loga a linha bruta recebida para depuração
            log_info(f"DEBUG: Linha bruta recebida do stdin: {line.strip()}")
            
            command_data = json.loads(line)
            
            # Loga os dados parseados para depuração
            log_info(f"DEBUG: Dados do comando parseados: {command_data}")

            action = command_data.get('action')
            data = command_data.get('data')
            # Garante que request_id seja None se não estiver presente
            request_id = command_data.get('requestId') 

            log_info(f"Comando recebido: action={action}, data={data}, requestId={request_id}")

            if action in commands_bot['backend']:
                coro = commands_bot['backend'][action](data) # Chama a função de comando
                
                # Executa a função assíncrona de forma segura na event loop principal do bot
                future = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                
                try:
                    result = future.result() # Espera o resultado da execução do comando
                    # Usa log_success para enviar a resposta de sucesso
                    log_success(request_id, result, "Comando executado com sucesso.")
                except Exception as e:
                    # Captura erros da execução do comando e usa log_error
                    error_message = f"Erro na execução do comando '{action}': {e}"
                    # Passa o request_id correto para o log_error
                    log_error(request_id, error_message, str(e)) 

            else:
                # Comando não reconhecido
                error_message = f"Erro: Comando '{action}' não reconhecido."
                # Passa o request_id correto para o log_error
                log_error(request_id, error_message) 

        except json.JSONDecodeError:
            # Erro de decodificação JSON no input do stdin - usa log_critical_error
            # Não há um request_id válido aqui, então não passamos um.
            log_critical_error(f"Recebido dado inválido (não é JSON) via stdin: {line.strip()}", "JSONDecodeError")
        except Exception as e:
            # Outros erros inesperados ao processar comandos do stdin - usa log_critical_error
            # Se request_id for None aqui, log_critical_error não o usará.
            log_critical_error(f"Erro inesperado ao processar comando do stdin: {e}", str(e))

@bot.event
async def on_ready():
    await load_commands('backend')  # Carrega os comandos do diretório 'backend'
    await load_commands('discord')
    await calendar()
    #sincs = await bot.tree.sync()
    #log_info(f'Comandos sincronizados: {len(sincs)}')
    log_info(f'Bot logado como {bot.user}')
    log_info('Bot está pronto para receber comandos do painel.')
    await create_events_task()
    # Inicia a tarefa de verificação de eventos

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    # Inicia a thread que escuta o stdin em background
    listener_thread = threading.Thread(target=stdin_listener, daemon=True)
    listener_thread.start()

    # Inicia o bot
    try:
        bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure:
        # Erro de login - usa log_critical_error
        log_critical_error("Token do bot inválido. Verifique seu token.", "LoginFailure")
    except Exception as e:
        # Outros erros na inicialização do bot - usa log_critical_error
        log_critical_error(f"Ocorreu um erro ao iniciar o bot: {e}", str(e))

