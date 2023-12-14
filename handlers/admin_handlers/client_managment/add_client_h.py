from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from database.queries import client_table
from filters.filters import check_phone_number
from handlers.other_handlers.service_h import get_service_list
from keyboards.inline.control_kb import get_cancel_kb
from lexicon import admin_lexicon
from states.states import FSMRecords

router = Router()


@router.callback_query(F.data == 'add_record', StateFilter(default_state))
async def add_client_record(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Записать клиента'"""
    keyboard = await get_cancel_kb()
    await state.set_state(FSMRecords.client_first_name)
    await callback.message.answer(text=admin_lexicon.MESSAGE['enter_client_first_name'],
                                  reply_markup=keyboard)
    await callback.answer()


@router.message(StateFilter(FSMRecords.client_first_name), F.text.isalpha())
async def process_enter_client_first_name(message: Message, state: FSMContext):
    """Срабатывает на ввод имени клиента"""
    keyboard = await get_cancel_kb()
    await state.set_state(FSMRecords.client_last_name)
    await state.update_data(client_first_name=message.text)
    await message.answer(text=admin_lexicon.MESSAGE['enter_client_last_name'],
                         reply_markup=keyboard)


@router.message(StateFilter(FSMRecords.client_first_name))
async def warning_client_not_first_name(message: Message):
    """Срабатывает, если имя или было введено некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['warning_client_not_first_name'])


@router.message(StateFilter(FSMRecords.client_last_name),  F.text.isalpha())
async def process_enter_client_last_name(message: Message, state: FSMContext):
    """Срабатывает на корректный ввод фамилии пользователя"""
    await state.update_data(client_last_name=message.text)
    data = await state.get_data()
    phone = await client_table.get_phone(data['client_first_name'], data['client_last_name'])
    if phone:
        client_id = phone['id']
        await state.clear()
        await state.update_data(client_id=client_id)
        await get_service_list(message=message, state=state)
    else:
        keyboard = await get_cancel_kb()
        await state.set_state(FSMRecords.client_phone)
        await message.answer(text=admin_lexicon.MESSAGE['enter_client_phone'],
                             reply_markup=keyboard)


@router.message(StateFilter(FSMRecords.client_last_name))
async def warning_client_not_last_name(message: Message):
    """Срабатывает, если фамилия была введена некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['warning_client_not_last_name'])


@router.message(StateFilter(FSMRecords.client_phone), check_phone_number)
async def process_enter_client_phone(message: Message, state: FSMContext):
    """Срабатывает на корректный ввод телефона пользователя"""
    await state.update_data(client_phone=message.text)
    client = await client_table.get_client_by_phone(phone=message.text)
    if client:
        first_name, last_name = client['first_name'], client['last_name']
        await message.answer(
            text=admin_lexicon.MESSAGE['name_does_not_match'].format(first_name=first_name, last_name=last_name))
    else:
        data = await state.get_data()
        telegram_id = None
        await client_table.add_client_to_db(telegram_id, data)
        client = await client_table.get_client_by_phone(phone=message.text)

    client_id = client['id']
    await state.clear()
    await state.update_data(client_id=client_id)
    await get_service_list(message=message, state=state)


@router.message(StateFilter(FSMRecords.client_phone))
async def warning_user_not_name(message: Message):
    """Срабатывает, если телефон клиента был введен некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['warning_client_not_phone'])
