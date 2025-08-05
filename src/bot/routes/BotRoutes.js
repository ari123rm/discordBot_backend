// src/routes/bot.js

import express from 'express';
import BotController from '../BotController.js';

const router = express.Router();

router.get('/start-bot', BotController.startBot);
router.get('/stop-bot', BotController.stopBot);
router.post('/commands/:command', BotController.sendCommand);
router.get('/commands',BotController.getCommands);

export default router;
