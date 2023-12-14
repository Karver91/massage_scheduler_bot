from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_inline_kb(lexicon: dict | list) -> InlineKeyboardMarkup:
    """Функция для формирования инлайн-клавиатуры на лету"""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if isinstance(lexicon, list):
        for text in lexicon:
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=str(text)))

    elif isinstance(lexicon, dict):
        for callback, text in lexicon.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=str(callback)))

    keyboard: InlineKeyboardMarkup = kb_builder.row(*buttons, width=1).as_markup()
    return keyboard
