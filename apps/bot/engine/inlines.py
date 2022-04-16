from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
import logging

from apps.bot.models import Note


def inline_query(update: Update, context: CallbackContext):
    """
    Inline query handler
    """
    query = update.inline_query.query
    logger = logging.getLogger(__name__)
    logger.info(f'Inline query: {query}')
    user = update.inline_query.from_user

    if not query:
        return

    notes = Note.objects.filter(user_bot_id=user.id).filter(title__icontains=query).order_by('-title')
    result = [
        InlineQueryResultArticle(
            id=note.id,
            title=note.title,
            input_message_content=InputTextMessageContent(note.text),
            description=note.description,
        ) for note in notes
    ]
    update.inline_query.answer(result)
    # context.bot.answer_inline_query(update.inline_query.id, result)
