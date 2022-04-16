from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from apps.bot.engine import markups
from apps.bot.engine.states import NoteState
from apps.bot.models import UserBot, Note


def start(update: Update, context: CallbackContext):
    """
    Start command.
    """

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

    text, keyboard = markups.main_markup(user)
    update.message.reply_text(text, reply_markup=keyboard)


def cancel(update: Update, context: CallbackContext):
    """
    Cancel and end the conversation.
    """
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def add_note_text(update: Update, context: CallbackContext):
    """
    Add notes command.
    """
    update.message.reply_text('Send me your note.')
    # add the text
    # Note.objects.create(
    #     user=UserBot.objects.get(id=update.message.from_user.id),
    #     title=update.message.text,
    # )
    return NoteState.ADD_TITLE


def add_note_title(update: Update, context: CallbackContext):
    """
    Add title command.
    """
    update.message.reply_text('Send me your title.')
    # add the title
    return NoteState.ADD_DESCRIPTION


def add_note_description(update: Update, context: CallbackContext):
    """
    Add text command.
    """
    update.message.reply_text('Send me your text.')
    # add the description
    return ConversationHandler.END
