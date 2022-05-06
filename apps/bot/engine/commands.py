import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from apps.bot.engine import markups
from apps.bot.engine.states import NoteState
from apps.bot.models import UserBot, Note

logger = logging.getLogger(__name__)


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
    return ConversationHandler.END


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
    update.message.reply_text('Write title of your note:')
    return NoteState.ADD_TITLE


def add_note_title(update: Update, context: CallbackContext):
    """
    Add title command.
    """
    title = update.message.text
    context.user_data['title'] = title
    update.message.reply_text('Send me a short description:')
    return NoteState.ADD_DESCRIPTION


def add_note_description(update: Update, context: CallbackContext):
    """
    Add text command.
    """
    description = update.message.text
    context.user_data['description'] = description
    update.message.reply_text('Send the text you want to save:')
    return NoteState.ADD_TEXT


def add_note_text_end(update: Update, context: CallbackContext):
    """
    Add text end command.
    """
    text = update.message.text
    title = context.user_data['title']
    description = context.user_data['description']

    del context.user_data['title']
    del context.user_data['description']

    user = UserBot.objects.get(id=update.message.from_user.id)
    note = Note.objects.create(
        user_bot=user,
        title=title,
        description=description,
        text=text,
    )
    _, keyboard = markups.main_markup(user)
    update.message.reply_text(
        f'Note "{note.title}" was added successfully!',
        reply_markup=keyboard
    )
    return ConversationHandler.END


def update_title(update: Update, context: CallbackContext):
    """
    Update note title
    """
    note = Note.objects.get(id=context.user_data['note_id'])
    note.title = update.message.text
    note.save()
    text, keyboard = markups.show_note_detail_markup(note)

    text = f'Note "{note.title}" was updated successfully!\n\n' + text
    update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return ConversationHandler.END


def update_text(update: Update, context: CallbackContext):
    """
    Update note text
    """
    note = Note.objects.get(id=context.user_data['note_id'])
    note.text = update.message.text
    note.save()
    text, keyboard = markups.show_note_detail_markup(note)

    text = f'Note "{note.title}" was updated successfully!\n\n' + text
    update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return ConversationHandler.END


def update_description(update: Update, context: CallbackContext):
    """
    Update note description
    """
    note = Note.objects.get(id=context.user_data['note_id'])
    note.description = update.message.text
    note.save()
    text, keyboard = markups.show_note_detail_markup(note)

    text = f'Note "{note.title}" was updated successfully!\n\n' + text
    update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return ConversationHandler.END


def delete_note(update: Update, context: CallbackContext):
    """
    Delete note command.
    """
    note = Note.objects.get(id=context.user_data['note_id'])
    note.delete()
    update.message.reply_text(
        'Note was deleted successfully!'
    )
    return ConversationHandler.END
