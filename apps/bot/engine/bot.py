import telegram
import logging
from django.conf import settings
from telegram.ext import Updater


class Bot:
    def __init__(self):
        token = settings.TELEGRAM_TOKEN
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.logging = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        dispatcher = self.updater.dispatcher

    def start(self):
        """
        Handle the traffic of your bot with polling technique or define a webhook
        """
        self.updater.start_polling()
        self.logging.info(f"[BOT] Running at https://t.me/{self.bot.username}")
        self.updater.idle()
