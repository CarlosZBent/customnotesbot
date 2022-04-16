import logging

import telegram
from django.conf import settings
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

from apps.bot.engine import commands, inlines


class Bot:
    def __init__(self):
        token = settings.TELEGRAM_TOKEN
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_error_handler(self.__error_handler)
        self.__set_actions()

    def __error_handler(self, update, context):
        """
        Error handler for the bot
        """
        try:
            raise context.error
        except telegram.TelegramError as e:
            self.logger.error(e.message)

        self.logger.error(f"[BOT] Error: {context.error}")

    def __set_actions(self):
        """
        Define the actions of your bot
        """
        start_handler = CommandHandler('start', commands.start)
        add_note_handler = CommandHandler('add_note', commands.add_note)
        inline_handler = InlineQueryHandler(inlines.inline_query)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(add_note_handler)
        self.dispatcher.add_handler(inline_handler)

        self.bot.set_my_commands([
            ('start', 'Start the bot'),
            ('add_note', 'Add a note to the bot'),
        ])

    def start(self):
        """
        Handle the traffic of your bot with polling technique or define a webhook
        """
        self.updater.start_polling()
        self.logger.info(f"[BOT] Running at https://t.me/{self.bot.username}")
        self.updater.idle()
