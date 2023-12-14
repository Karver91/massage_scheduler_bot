from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import admin_lexicon
from services.services import get_all_records


router = Router()


# ------------------ Команда "Посмотреть все доступные записи" --------------------
@router.callback_query(F.data == 'view_all_records', StateFilter(default_state))
async def process_view_appointment_command(callback: CallbackQuery):
    """Срабатывает на нажатие кнопки 'Посмотреть все доступные записи'"""
    all_records: str = await get_all_records()
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    await callback.message.answer(text=all_records,
                                  reply_markup=keyboard)
    await callback.answer()
