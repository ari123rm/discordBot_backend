// Carrega as variáveis de ambiente do arquivo .env
import 'dotenv/config';

// Acessa o token do Discord. Se não existir, o valor será 'undefined'.
export const DISCORD_TOKEN = process.env.DISCORD_TOKEN;

// Define a porta. Se o valor em process.env.PORT for vazio ou nulo, 
// ele usará o valor padrão 3000.
export const PORT = parseInt(process.env.PORT, 10) || 3000;

// Define a URL externa. Se a variável não existir no .env,
// ela usará o valor padrão `http://localhost:<porta>`.
export const EXTERNAL_URL = process.env.EXTERNAL_URL || `http://localhost:${PORT}`;


export default { DISCORD_TOKEN, PORT, EXTERNAL_URL };
