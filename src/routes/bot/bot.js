// src/routes/bot.js

import express from 'express';
import BotController from '../../controllers/BotController.js';

const router = express.Router();

router.get('/start-bot', BotController.startBot);
router.get('/stop-bot', BotController.stopBot);
router.post('/send-command', BotController.sendCommand);

export default router;
