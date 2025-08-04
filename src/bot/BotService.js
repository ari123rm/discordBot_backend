import { spawn } from 'child_process';
import crypto from 'crypto'; // Importa o módulo crypto para gerar IDs únicos

// Variável para armazenar o processo do bot Python
let botProcess = null;

// Um mapa para armazenar as promessas pendentes, indexadas pelo requestId
const pendingRequests = new Map();

/**
 * Configura os listeners para as saídas stdout e stderr do processo do bot Python.
 * Processa mensagens JSON para resolver/rejeitar promessas pendentes.
 */
function setupBotProcessListeners() {
    if (!botProcess) return;

    // Remove listeners antigos para evitar duplicação em reinícios do bot
    botProcess.stdout.removeAllListeners('data');
    botProcess.stderr.removeAllListeners('data');
    botProcess.removeAllListeners('close');

    // Ouve dados na saída padrão do bot (stdout)
    botProcess.stdout.on('data', (data) => {
        const message = data.toString().trim();
        // console.log(`[Saída do Bot - RAW]: ${message}`); // Para depuração do formato bruto
        try {
            const response = JSON.parse(message);
            // Verifica se a resposta é uma mensagem estruturada com requestId e status
            if (response.requestId && pendingRequests.has(response.requestId)) {
                const { resolve, reject } = pendingRequests.get(response.requestId);
                if (response.status === "success") {
                    resolve(response.data); // Resolve a promessa com os dados de sucesso
                } else if (response.status === "error") {
                    // Rejeita a promessa com uma mensagem de erro do bot
                    reject(new Error(response.message || 'Erro desconhecido do bot.'));
                }
                pendingRequests.delete(response.requestId); // Remove a promessa do mapa após processar
            } else {
                // Loga mensagens que não são respostas de requisição (ex: log_info do Python)
                console.log(`[Bot INFO]: ${message}`);
            }
        } catch (e) {
            // Se não for um JSON válido, loga como uma mensagem informativa geral
            console.log(`[Bot Log]: ${message}`);
        }
    });

    // Ouve dados na saída de erro padrão do bot (stderr)
    botProcess.stderr.on('data', (data) => {
        const message = data.toString().trim();
        // console.error(`[Console do Bot - RAW]: ${message}`); // Para depuração do formato bruto
        try {
            const errorResponse = JSON.parse(message);
            // Verifica se a resposta de erro é uma mensagem estruturada com requestId e status
            if (errorResponse.requestId && pendingRequests.has(errorResponse.requestId)) {
                const { reject } = pendingRequests.get(errorResponse.requestId);
                // Rejeita a promessa com a mensagem de erro do bot
                reject(new Error(errorResponse.message || 'Erro desconhecido do bot.'));
                pendingRequests.delete(errorResponse.requestId); // Remove a promessa do mapa
            } else {
                // Loga mensagens de erro que não são respostas de requisição (ex: log_error, log_critical_error do Python)
                console.error(`[Bot ERRO]: ${message}`);
            }
        } catch (e) {
            // Se não for um JSON de erro válido, loga como um erro geral
            console.error(`[Bot Console]: ${message}`);
        }
    });

    // Ouve o evento de fechamento do processo do bot
    botProcess.on('close', (code) => {
        console.log(`Processo do bot encerrado com código ${code}`);
        // Rejeita todas as promessas pendentes se o bot for encerrado inesperadamente
        pendingRequests.forEach(({ reject }, requestId) => {
            reject(new Error(`O bot foi encerrado inesperadamente (código: ${code}).`));
            pendingRequests.delete(requestId);
        });
        botProcess = null;
    });
}

// Objeto que representa o serviço do bot
const botService = {
    /**
     * Inicia o processo do bot Python.
     * @returns {Promise<{ message: string }>} Objeto com mensagem de sucesso.
     * @throws {Error} Se o bot já estiver em execução.
     */
    async startBot() {
        if (botProcess) {
            console.log('Tentativa de iniciar o bot, mas ele já está em execução.');
            throw new Error('O bot já está em execução.');
        }

        console.log('Recebida requisição para iniciar o bot...');
        const command = process.platform === 'win32' ? 'py' : 'python3';
        botProcess = spawn(command, ['-u', 'bot/main.py']);

        // Configura os listeners para o novo processo do bot
        setupBotProcessListeners();

        return { message: 'Bot iniciado com sucesso!' };
    },

    /**
     * Envia um comando de desligamento para o bot e encerra o processo.
     * @returns {Promise<{ message: string }>} Objeto com mensagem de sucesso.
     * @throws {Error} Se o bot não estiver em execução ou se houver falha na comunicação.
     */
    async stopBot() {
        if (!botProcess) {
            console.log('Tentativa de parar o bot, mas ele não está em execução');
            throw new Error('O bot não está em execução.');
        }

        console.log('Recebida requisição para parar o bot...');

        // O comando de desligamento não precisa de requestId, pois ele encerra o processo
        const shutdownCommand = JSON.stringify({ action: 'shutdown' });

        try {
            botProcess.stdin.write(shutdownCommand + '\n');
            console.log('Comando de desligamento enviado para o bot.');

            // Aguarda um momento para permitir que o bot se desconecte graciosamente
            await new Promise(resolve => setTimeout(resolve, 3000)); // 3 segundos de atraso

            if (botProcess) {
                botProcess.kill(); // Envia um sinal de encerramento ao processo
                console.log('Processo do bot encerrado.');
                botProcess = null;
            }
            return { message: 'Comando de parada enviado. O bot está desligando...' };

        } catch (error) {
            console.error('Falha ao enviar comando de desligamento para o bot:', error);
            if (botProcess) {
                botProcess.kill();
                botProcess = null;
            }
            throw new Error('Falha ao se comunicar com o bot, mas o processo foi encerrado.');
        }
    },

    /**
     * Envia um comando genérico para o bot em execução e aguarda uma resposta.
     * @param {string} action A ação a ser executada pelo bot.
     * @param {any} data Os dados associados à ação.
     * @returns {Promise<any>} Uma promessa que resolve com os dados da resposta do bot ou rejeita com um erro.
     * @throws {Error} Se o bot não estiver em execução ou se houver falha na comunicação.
     */
    async sendCommand(action, data) {
        if (!botProcess) {
            throw new Error('O bot não está em execução.');
        }

        // Gera um ID de requisição único para rastrear a resposta
        const requestId = crypto.randomUUID();

        // Cria uma nova promessa que será resolvida ou rejeitada quando o bot responder
        const promise = new Promise((resolve, reject) => {
            // Armazena as funções resolve e reject no mapa de requisições pendentes
            pendingRequests.set(requestId, { resolve, reject });

            // Define um timeout para a requisição (ex: 10 segundos)
            setTimeout(() => {
                if (pendingRequests.has(requestId)) {
                    pendingRequests.delete(requestId);
                    reject(new Error(`Timeout: O bot não respondeu ao comando '${action}' (ID: ${requestId}) a tempo.`));
                }
            }, 10000); // 10 segundos de timeout
        });

        // Constrói o comando a ser enviado como uma string JSON, incluindo o requestId
        const commandToSend = JSON.stringify({ action, data, requestId });

        try {
            // Escreve o comando na entrada padrão do processo do bot
            botProcess.stdin.write(commandToSend + '\n');
            console.log(`Comando enviado para o bot: ${commandToSend}`);
            // Retorna a promessa. O controller aguardará por ela.
            return promise;

        } catch (error) {
            console.error('Falha ao enviar comando para o bot:', error);
            // Rejeita a promessa imediatamente se houver um erro de escrita no stdin
            if (pendingRequests.has(requestId)) {
                const { reject } = pendingRequests.get(requestId);
                reject(new Error('Falha ao se comunicar com o bot.'));
                pendingRequests.delete(requestId);
            }
            throw new Error('Falha ao se comunicar com o bot.');
        }
    }
};

export default botService;
