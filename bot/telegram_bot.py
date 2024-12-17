from telegram import Bot

from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    def __init__(self):
        self.bot = Bot(TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_message(self, message):
        """
        Send a message to the configured Telegram chat.
        """
        await self.bot.send_message(chat_id=self.chat_id, text=message)
