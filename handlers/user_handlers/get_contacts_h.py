from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from config.config import SALON_ADDRESS, SALON_PHONE

router: Router = Router()


# -------------------- Команда "Наши контактные данные" ----------------------------------

@router.callback_query(F.data == 'get_contact', StateFilter(default_state))
async def process_get_contact_command(callback: CallbackQuery):
    await callback.message.answer(text=f'Наш адрес: {SALON_ADDRESS}\n\nНомер телефона для связи: {SALON_PHONE}')
    await callback.answer()
