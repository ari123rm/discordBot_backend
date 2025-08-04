import { spawn } from 'child_process';
let botProcess = null;
export default {
    async startBot(req, res) {
        if (botProcess) {
            console.log('Tentativa de iniciar o bot, mas ele já está em execução.');
            return res.status(400).json({ message: 'O bot já está em execução.' });
        }

        console.log('Recebida requisição para iniciar o bot...');
        const command = process.platform === 'win32' ? 'py' : 'python3';
        botProcess = spawn(command, ['-u', 'bot/main.py']); // O argumento '-u' força a saída a não ter buffer, o que é bom para logs em tempo real

        botProcess.stdout.on('data', (data) => {
            console.log(`[Saída do Bot]: ${data.toString().trim()}`);
        });

        botProcess.stderr.on('data', (data) => {
            console.error(`[Console do Bot]: ${data.toString().trim()}`);
        });

        botProcess.on('close', (code) => {
            console.log(`Processo do bot encerrado com código ${code}`);
            botProcess = null;
        });

        res.json({ message: 'Bot iniciado com sucesso!' });
    },

    async stopBot(req, res) {
    if (!botProcess) {
        console.log('Tentativa de parar o bot, mas ele não está em execução.');
        return res.status(400).json({ message: 'O bot não está em execução.' });
    }
    
    console.log('Recebida requisição para parar o bot...');
    
    // Create a shutdown command to be sent to the bot
    const shutdownCommand = JSON.stringify({ action: 'shutdown' });
    
    try {
        // Send the shutdown command to the bot's stdin
        // The '\n' is crucial for the Python script to know the message has ended.
        botProcess.stdin.write(shutdownCommand + '\n');
        console.log('Comando de desligamento enviado para o bot.');

        // Wait for a moment to allow the bot to disconnect gracefully
        // before terminating the process. You can adjust this delay.
        setTimeout(() => {
            if (botProcess) {
                botProcess.kill();
                console.log('Processo do bot encerrado.');
                botProcess = null;
            }
        }, 3000); // 3-second delay
        
        res.json({ message: 'Comando de parada enviado. O bot está desligando...' });
    
    } catch (error) {
        console.error('Falha ao enviar comando de desligamento para o bot:', error);
        // Fallback: If sending the command fails, kill the process anyway
        botProcess.kill();
        botProcess = null;
        res.status(500).json({ message: 'Falha ao se comunicar com o bot, mas o processo foi encerrado.' });
    }
},
    async sendCommand(req, res) {
        // Verifica se o bot está rodando
        if (!botProcess) {
            return res.status(400).json({ message: 'O bot não está em execução.' });
        }

        // Pega o comando do corpo da requisição
        const { action, data } = req.body;

        // Formata o comando como uma string JSON
        const command = JSON.stringify({ action, data });

        try {
            // Escreve o comando no stdin do processo do bot
            // O '\n' (nova linha) é CRUCIAL para que o Python saiba que a mensagem terminou.
            botProcess.stdin.write(command + '\n');
            
            console.log(`Comando enviado para o bot: ${command}`);
            res.json({ message: 'Comando enviado com sucesso!' });

        } catch (error) {
            console.error('Falha ao enviar comando para o bot:', error);
            res.status(500).json({ message: 'Falha ao se comunicar com o bot.' });
        }
    }

}