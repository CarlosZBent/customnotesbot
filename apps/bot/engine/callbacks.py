import logging

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from apps.bot.engine import markups
from apps.bot.models import UserBot, Note

logger = logging.getLogger(__name__)


def back_to_main(update: Update, context: CallbackContext):
    """
    Return to main menu
    """
    text, keyboard = markups.main_markup(UserBot.objects.get(id=update.effective_user.id))
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return ConversationHandler.END


def show_notes(update: Update, context: CallbackContext):
    """
    Show all user notes
    """
    notes = Note.objects.filter(user_bot_id=update.effective_user.id)
    text, keyboard = markups.show_notes_markup(notes)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return ConversationHandler.END
