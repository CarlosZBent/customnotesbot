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


def show_note_detail_markup(note: Note) -> (str, list):
    # TODO: add edit and delete button
    base_keyboard = [
        [
            InlineKeyboardButton(text="Update Title", callback_data=f"update_title_{note.id}"),
            InlineKeyboardButton(text="Update Text", callback_data=f"update_text_{note.id}"),
            InlineKeyboardButton(text="Update description", callback_data=f"update_description_{note.id}"),
        ],
        [
            InlineKeyboardButton(text="Delete", callback_data=f"delete_note_{note.id}"),
        ],
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="show_notes"),
        ],
    ]
    text = f"title: {note.title}\n" \
           f"short description: {note.description}\n" \
           f"text: {note.text}\n"
    return text, InlineKeyboardMarkup(base_keyboard)


def add_note_markup() -> (str, list):
    keyboard = [
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main"),
        ],
    ]
    return "Write title of your note:", InlineKeyboardMarkup(keyboard)


def update_title_markup(note: Note) -> (str, list):
    text = f"Write new title for note:\n"
    keyboard = [
        [
            InlineKeyboardButton(text="Cancel", callback_data=f"show_note_{note.id}"),
        ],
    ]
    return text, InlineKeyboardMarkup(keyboard)


def update_text_markup(note: Note) -> (str, list):
    pass


def update_description_markup(note: Note) -> (str, list):
    pass


def delete_note_markup(note: Note) -> (str, list):
    pass
