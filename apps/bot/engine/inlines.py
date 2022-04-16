from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
import logging


def inline_query(update: Update, context: CallbackContext):
    """
    Inline query handler
    """
    query = update.inline_query.query
    logger = logging.getLogger(__name__)
    logger.info(f'Inline query: {query}')
    if not query:
        return
    result = [
        InlineQueryResultArticle(
            id=f"id: {query}",
            title=f"title: {query}",
            input_message_content=InputTextMessageContent(f"message: {query}"),
            description=f"description: {query}",
        )
    ]
    context.bot.answer_inline_query(update.inline_query.id, result)
