from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import admin_lexicon, other_lexicon

router = Router()


# Команда Старт
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """Отлавливает команду /start и возвращает клавиатуру стартового меню"""
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    await message.answer(text=other_lexicon.COMMANDS['start'],
                         reply_markup=keyboard)
