from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from apps.bot.models import UserBot


def main_markup(user: UserBot) -> (str, list):
    text = f"Hi {user.first_name},\n" \
           f"I'm a bot that can help you to manage your notes.\n"
    keyboard = [
        [
            InlineKeyboardButton(text="Add note", callback_data="add_note"),
            InlineKeyboardButton(text="Show notes", callback_data="show_notes"),
        ],
    ]
    return text, InlineKeyboardMarkup(keyboard)
