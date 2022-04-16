from telegram import Update
from telegram.ext import CallbackContext

from apps.bot.models import UserBot


def start(update: Update, context: CallbackContext):
    """
    Start command.
    """
    update.message.reply_text('Hello!')

    # save the user
    user, created = UserBot.objects.get_or_create(
        id=update.message.from_user.id,
    )

    # updating user info no matter if it's created or not
    user.username = update.message.from_user.username
    user.first_name = update.message.from_user.first_name
    user.last_name = update.message.from_user.last_name
    user.chat_id = update.message.chat_id
    if created:
        user.language_code = update.message.from_user.language_code
        user.save()


def add_note(update: Update, context: CallbackContext):
    """
    Add notes command.
    """
    update.message.reply_text('Send me your note.')
