// server.js

// Importa os módulos necessários
import express from 'express';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import swaggerUi from 'swagger-ui-express';
import swaggerSpec from './swagger.js'; 
import {EXTERNAL_URL,PORT} from './src/env.js'; // Importa a configuração do ambiente
import botService from './src/bot/BotService.js'; // Importa a função para iniciar o bot
// Importa o roteador principal que contém todas as rotas
import allRoutes from './src/routes.js';

// Define __dirname para ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express(); 


// Middlewares para servir arquivos estáticos e para interpretar JSON
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Rota principal que envia a página de controle
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use('/api', allRoutes); // Monta as rotas do arquivo index.js

botService.startBot();


app.listen(PORT, () => {
  console.log(`Painel de controle rodando em ${EXTERNAL_URL}`);
  console.log(`API Docs no ${EXTERNAL_URL}/docs`);
});  