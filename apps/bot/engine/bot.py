import logging

import telegram
from django.conf import settings
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler

from apps.bot.engine import commands, inlines, callbacks
from apps.bot.engine.states import NoteState


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
        self.dispatcher.add_handler(CommandHandler('start', commands.start))
        self.dispatcher.add_handler(CallbackQueryHandler(callbacks.show_notes, pattern='show_notes'))
        self.dispatcher.add_handler(CallbackQueryHandler(callbacks.back_to_main, pattern='back_to_main'))
        self.dispatcher.add_handler(CallbackQueryHandler(callbacks.show_note_detail, pattern='show_note_'))
        self.dispatcher.add_handler(InlineQueryHandler(inlines.inline_query))

        self.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('add_note', commands.add_note_text),
                CallbackQueryHandler(callbacks.add_note, pattern='add_note')
            ],
            states={
                NoteState.ADD_TITLE: [
                    MessageHandler(Filters.text, commands.add_note_title),
                    CommandHandler('cancel', commands.cancel)
                ],
                NoteState.ADD_DESCRIPTION: [
                    MessageHandler(Filters.text, commands.add_note_description),
                    CommandHandler('cancel', commands.cancel)
                ],
                NoteState.ADD_TEXT: [
                    MessageHandler(Filters.text, commands.add_note_text_end),
                    CommandHandler('cancel', commands.cancel)
                ],
            },
            fallbacks=[CommandHandler('cancel', commands.cancel)]
        ))

        self.bot.set_my_commands([
            ('start', 'Start the bot'),
            ('add_note', 'Add a note to the bot'),
            ('cancel', 'Cancel the current action'),
        ])

    def start(self):
        """
        Handle the traffic of your bot with polling technique or define a webhook
        """
        self.updater.start_polling()
        self.logger.info(f"[BOT] Running at https://t.me/{self.bot.username}")
        self.updater.idle()
