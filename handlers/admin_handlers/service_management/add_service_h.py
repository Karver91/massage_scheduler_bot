from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from database.queries.service_table import add_service_to_db
from filters.filters import check_add_service_name
from keyboards.inline.control_kb import get_cancel_kb, get_next_cancel_kb
from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import admin_lexicon
from states.states import FSMAddService

router = Router()


# -------------------- Команда "Добавить услугу" ----------------------------------
@router.callback_query(F.data == 'add_service_button', StateFilter(default_state))
async def process_add_service_command(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Добавить услугу'
    Запускает машину состояний"""
    keyboard = await get_cancel_kb()
    await callback.message.answer(text=admin_lexicon.MESSAGE['add_service_name'],
                                  reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMAddService.service_name)
    await callback.answer()


# НАЗВАНИЕ
@router.message(StateFilter(FSMAddService.service_name), check_add_service_name)
async def process_add_service_name(message: Message, state: FSMContext):
    """Отлавливает ввод названия услуги.
    Переводит состояние на ввод длительности оказания услуги"""
    keyboard = await get_cancel_kb()
    await state.update_data(name=message.text)
    await message.answer(text=admin_lexicon.MESSAGE['add_service_duration'],
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода времени оказания услуги
    await state.set_state(FSMAddService.service_duration)


@router.message(StateFilter(FSMAddService.service_name))
async def warning_add_service_not_name(message: Message):
    """Срабатывает, если название услуги было введено некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['add_service_not_name'])


# ДЛИТЕЛЬНОСТЬ
@router.message(StateFilter(FSMAddService.service_duration), F.text.isdigit())
async def process_add_service_duration(message: Message, state: FSMContext):
    """Отлавливает ввод длительности оказания услуги.
    Переводит состояние на ввод стоймости услуги"""
    keyboard = await get_cancel_kb()
    await state.update_data(duration=message.text)
    await message.answer(text=admin_lexicon.MESSAGE['add_service_price'],
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода стоймости оказания услуги
    await state.set_state(FSMAddService.service_price)


@router.message(StateFilter(FSMAddService.service_duration))
async def warning_add_service_not_duration(message: Message):
    """Срабатывает, если длительность услуги была введена некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['add_service_not_duration'])


# ЦЕНА
@router.message(StateFilter(FSMAddService.service_price), F.text.isdigit())
async def process_add_service_price(message: Message, state: FSMContext):
    """Отлавливает ввод стоймости оказания услуги"""
    keyboard = await get_next_cancel_kb()
    await state.update_data(price=message.text)
    await message.answer(text=admin_lexicon.MESSAGE['add_service_description'],
                         reply_markup=keyboard)
    await state.set_state(FSMAddService.service_description)


@router.message(StateFilter(FSMAddService.service_price))
async def warning_add_service_not_price(message: Message):
    """Срабатывает, если стоймость услуги была введена некорректно"""
    await message.answer(text=admin_lexicon.MESSAGE['add_service_not_price'])


# ОПИСАНИЕ
@router.callback_query(StateFilter(FSMAddService.service_description), F.data == 'next')
@router.message(StateFilter(FSMAddService.service_description), F.text)
async def process_add_service_description(answer: Message | CallbackQuery, state: FSMContext):
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    if isinstance(answer, Message):
        answer: Message
        await state.update_data(description=answer.text)
        await answer.answer(text=admin_lexicon.MESSAGE['add_service_save_data'],
                            reply_markup=keyboard)
    else:
        answer: CallbackQuery
        await state.update_data(description=None)
        await answer.message.answer(text=admin_lexicon.MESSAGE['add_service_save_data'],
                                    reply_markup=keyboard)
        await answer.answer()

    # Сохраняет данные в бд
    data = await state.get_data()
    await add_service_to_db(data)

    # Очищаем машину состояний
    await state.clear()


@router.message(StateFilter(FSMAddService.service_description))
async def warning_add_service_incorrect_description(message: Message):
    keyboard = await get_next_cancel_kb()
    await message.answer(text=admin_lexicon.MESSAGE['add_service_incorrect_description'],
                         reply_markup=keyboard)
