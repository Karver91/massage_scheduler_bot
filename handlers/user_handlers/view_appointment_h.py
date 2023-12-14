from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import user_lexicon
from services.services import get_appointment

router = Router()


# -------------------- Команда "Посмотреть мою запись" ----------------------------------

@router.callback_query(F.data == 'view_appointment', StateFilter(default_state))
async def process_view_appointment_command(callback: CallbackQuery):
    my_appointment: str = await get_appointment(callback.from_user.id)
    keyboard = await get_start_keyboard(user_lexicon.COMMANDS['start_buttons'])
    await callback.message.answer(text=my_appointment,
                                  reply_markup=keyboard)
    await callback.answer()
