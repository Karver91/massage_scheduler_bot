from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import admin_lexicon
from services.services import get_client_list

router = Router()


# ------------------ Команда "Получить список клиентов" --------------------
@router.callback_query(F.data == 'client_list', StateFilter(default_state))
async def process_get_client_list_command(callback: CallbackQuery):
    """Срабатывает на нажатие кнопки 'Получить список клиентов'"""
    clients: str = await get_client_list()
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    await callback.message.answer(text=clients,
                                  reply_markup=keyboard)
    await callback.answer()
