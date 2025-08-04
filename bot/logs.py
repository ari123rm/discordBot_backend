import sys
import json

def log_success(request_id, data, message="Operação concluída com sucesso."):
    """
    Envia uma mensagem de sucesso estruturada (JSON) para a saída padrão (stdout).
    Esta função é usada para enviar respostas de sucesso de volta ao backend Node.js.

    Args:
        request_id (str): O ID da requisição original do Node.js.
        data (any): Os dados resultantes da operação.
        message (str, optional): Uma mensagem descritiva do sucesso. Padrão para "Operação concluída com sucesso.".
    """
    response = {
        "requestId": request_id,
        "status": "success",
        "message": message,
        "data": data
    }
    # Imprime o JSON para stdout, que será lido pelo processo Node.js
    print(json.dumps(response))

def log_error(request_id, error_message, error_details=None):
    """
    Envia uma mensagem de erro estruturada (JSON) para a saída de erro padrão (stderr).
    Esta função é usada para enviar mensagens de erro e exceções para o backend Node.js.

    Args:
        request_id (str): O ID da requisição original do Node.js.
        error_message (str): Uma mensagem descritiva do erro.
        error_details (any, optional): Detalhes adicionais sobre o erro (ex: traceback, dados de erro). Padrão para None.
    """
    error_response = {
        "requestId": request_id,
        "status": "error",
        "message": error_message,
        "details": error_details
    }
    # Imprime o JSON para stderr, que será lido pelo processo Node.js
    print(json.dumps(error_response), file=sys.stderr)

def log_info(message):
    """
    Envia uma mensagem informativa simples para a saída padrão (stdout).
    Usado para logs gerais que não são respostas diretas a uma requisição.

    Args:
        message (str): A mensagem informativa a ser logada.
    """
    print(f"[INFO]: {message}")

def log_warning(message):
    """
    Envia uma mensagem de aviso simples para a saída de erro padrão (stderr).

    Args:
        message (str): A mensagem de aviso a ser logada.
    """
    print(f"[AVISO]: {message}", file=sys.stderr)

def log_critical_error(message, details=None):
    """
    Envia uma mensagem de erro crítica simples para a saída de erro padrão (stderr).
    Usado para erros que não estão diretamente ligados a uma requisição específica.

    Args:
        message (str): A mensagem de erro crítica.
        details (any, optional): Detalhes adicionais sobre o erro. Padrão para None.
    """
    if details:
        print(f"[ERRO CRÍTICO]: {message} - Detalhes: {details}", file=sys.stderr)
    else:
        print(f"[ERRO CRÍTICO]: {message}", file=sys.stderr)
