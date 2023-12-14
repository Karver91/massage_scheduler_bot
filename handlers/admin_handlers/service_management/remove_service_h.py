from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from database.queries.service_table import service_is_deleted_true, remove_service_from_db
from keyboards.inline.service_list_kb import get_service_keyboard
from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import admin_lexicon
from states.states import FSMRemoveService

router = Router()


# --------------------- Команда "Удалить услугу" ----------------------------------
@router.callback_query(F.data == 'remove_service_button', StateFilter(default_state))
async def process_remove_service_command(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Удалить услугу'
    Выводит клавиатуру со списком услуг пользователю"""
    keyboard = await get_service_keyboard()
    await state.set_state(FSMRemoveService.state_remove)
    await callback.message.answer(text=admin_lexicon.MESSAGE['remove_service_message'],
                                  reply_markup=keyboard)
    await callback.answer()


@router.message(StateFilter(FSMRemoveService.state_remove))
async def warning_remove_service(message: Message):
    """Срабатывает, если вместо события нажатия кнопки, было совершено нечто другое"""
    await message.answer(text=admin_lexicon.MESSAGE['remove_not_service'])


@router.callback_query(F.data != 'cancel', StateFilter(FSMRemoveService.state_remove))
async def process_remove_service(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки с услугой, которую нужно удалить"""
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    await service_is_deleted_true(callback.data)
    await remove_service_from_db()
    await state.clear()
    await callback.message.answer(text=admin_lexicon.MESSAGE['remove_service_success'],
                                  reply_markup=keyboard)
    await callback.answer()
