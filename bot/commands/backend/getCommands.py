from ..commands_bot import commands_bot, load_commands
async def getCommands(data):
    """
    Função para obter os comandos disponíveis.
    Retorna um dicionário com os comandos ou levanta uma exceção em caso de erro.
    """
    try:
        # Retorna os comandos disponíveis
        return {"status": "success", "commands": list(commands_bot['backend'].keys())}
    except Exception as e:
        error_msg = f"Erro ao obter comandos: {e}"
        raise Exception(error_msg)  # Levanta a exceção