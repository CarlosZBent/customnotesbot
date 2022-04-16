from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from apps.bot.models import UserBot, Note


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


def show_notes_markup(notes: Note) -> (str, list):
    base_keyboard = [
        [
            InlineKeyboardButton(text="Add note", callback_data="add_note"),
            InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main"),
        ],
    ]
    if notes:
        text = f"Here are your notes:\n"
        keyboard = [
            [
                InlineKeyboardButton(text=note.title, callback_data=f"show_note_{note.id}")
            ] for note in notes
        ]
        return text, InlineKeyboardMarkup(keyboard + base_keyboard)

    text = "You don't have any notes yet.\n"

    return text, InlineKeyboardMarkup(base_keyboard)
