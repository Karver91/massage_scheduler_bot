from aiogram.types import CallbackQuery

from config.config import ADMIN_IDS
from keyboards.inline.builder import create_inline_kb
from lexicon import admin_lexicon, user_lexicon


async def get_start_keyboard(lexicon):
    """Возвращает стартовую клавиатуру-меню по нажатию кнопки /start"""
    keyboard = await create_inline_kb(lexicon)
    return keyboard


async def get_start_menu_kb(callback: CallbackQuery):
    """Возвращает стартовую клавиатуру-меню по запросу"""
    if callback.from_user.id in ADMIN_IDS:
        lexicon = admin_lexicon.COMMANDS['start_buttons']
    else:
        lexicon = user_lexicon.COMMANDS['start_buttons']
    keyboard = await create_inline_kb(lexicon)
    return keyboard
