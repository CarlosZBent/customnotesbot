import logging

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from apps.bot.engine import markups
from apps.bot.engine.states import NoteState
from apps.bot.models import UserBot, Note

logger = logging.getLogger(__name__)


def back_to_main(update: Update, context: CallbackContext):
    """
    Return to main menu
    """
    text, keyboard = markups.main_markup(UserBot.objects.get(id=update.effective_user.id))
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return ConversationHandler.END


def add_note(update: Update, context: CallbackContext):
    """
    Add new note
    """
    text, keyboard = markups.add_note_markup()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return NoteState.ADD_TITLE


def show_notes(update: Update, context: CallbackContext):
    """
    Show all user notes
    """
    notes = Note.objects.filter(user_bot_id=update.effective_user.id)
    text, keyboard = markups.show_notes_markup(notes)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return ConversationHandler.END


def show_note_detail(update: Update, context: CallbackContext):
    """
    Show note's details
    """
    note_id = int(update.callback_query.data.split('_')[-1])
    note = Note.objects.get(id=note_id)
    text, keyboard = markups.show_note_detail_markup(note)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return ConversationHandler.END


def update_title(update: Update, context: CallbackContext):
    note_id = int(update.callback_query.data.split('_')[-1])
    note = Note.objects.get(id=note_id)
    context.user_data['note_id'] = note_id
    text, keyboard = markups.update_title_markup(note)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return NoteState.UPDATE_TITLE


def update_text(update: Update, context: CallbackContext):
    note_id = int(update.callback_query.data.split('_')[-1])
    note = Note.objects.get(id=note_id)
    text, keyboard = markups.update_text_markup(note)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # return NoteState.UPDATE_TEXT


def update_description(update: Update, context: CallbackContext):
    note_id = int(update.callback_query.data.split('_')[-1])
    note = Note.objects.get(id=note_id)
    text, keyboard = markups.update_description_markup(note)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # return NoteState.UPDATE_DESCRIPTION


def delete_note(update: Update, context: CallbackContext):
    note_id = int(update.callback_query.data.split('_')[-1])
    note = Note.objects.get(id=note_id)
    text, keyboard = markups.delete_note_markup(note)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # return NoteState.DELETE_NOTE
