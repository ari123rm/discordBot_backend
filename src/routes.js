// routes/index.js

import express from 'express';
import botRoutes from './bot/routes/BotRoutes.js';    // Importa as rotas do bot
//import userRoutes from './users.js';  // Importa as rotas de usuários (exemplo)

const router = express.Router();

// Aqui você "monta" os roteadores individuais
// O primeiro argumento define o prefixo da URL para essas rotas.
router.use('/bot', botRoutes);
//router.use('/users', userRoutes); // Exemplo: rotas para /users

export default router; 