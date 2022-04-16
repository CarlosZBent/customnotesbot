from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    """
    Start command.
    """
    update.message.reply_text('Hello!')
