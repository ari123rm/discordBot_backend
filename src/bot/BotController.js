import BotService from "./BotService.js";


class BotController {
  static async startBot(req, res) {
    try {
      const result = await BotService.startBot();
      res.status(200).json({ message: 'Bot started successfully', data: result });
    } catch (error) {
      res.status(500).json({ message: 'Error starting bot', error: error.message });
    }
  }

  static async stopBot(req, res) {
    try {
      const result = await BotService.stopBot();
      res.status(200).json({ message: 'Bot stopped successfully', data: result });
    } catch (error) {
      res.status(500).json({ message: 'Error stopping bot', error: error.message });
    }
  }

  static async sendCommand(req, res) {
    const action = req.params.command; // Obtém o comando da URL
    const { data } = req.body;
    try {
      const result = await BotService.sendCommand(action, data);
      res.status(200).json({ message: 'Command sent successfully', data: result });
    } catch (error) {
      res.status(500).json({ message: 'Error sending command', error: error.message });
    }
  }
}

export default BotController;