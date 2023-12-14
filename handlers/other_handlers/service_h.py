from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.queries.service_table import get_service_description_from_db
from keyboards.inline.control_kb import get_next_back_kb
from keyboards.inline.service_list_kb import get_service_keyboard
from lexicon import other_lexicon
from states.states import FSMRecords

router = Router()


async def get_service_list(message: Message | CallbackQuery, state: FSMContext):
    """Возвращает клавиатуру с услугами пользователю"""
    keyboard = await get_service_keyboard()
    text = other_lexicon.MESSAGE['choose_service']
    await state.set_state(FSMRecords.choice_service)
    if isinstance(message, Message):
        await message.answer(text=text,
                             reply_markup=keyboard)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text=text,
                                     reply_markup=keyboard)
        await message.answer()


@router.callback_query(StateFilter(FSMRecords.choice_service), ~F.data.in_({'next', 'back', 'cancel'}))
async def process_choice_service(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на выбор услуги для админа и клиента"""
    try:
        keyboard = await get_next_back_kb()
        service_description = await get_service_description_from_db(callback.data)
        await callback.message.answer(text=f"{service_description['service_name']}\n"
                                           f"{service_description['description'] if service_description['description'] else ''}\n"
                                           f"Продолжительность: {service_description['duration']} мин\n"
                                           f"Цена: {service_description['price']} руб",
                                      reply_markup=keyboard)
        await state.update_data(service_id=callback.data)
        await callback.answer()
    except (ValueError, KeyError, TypeError):
        await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_service), F.data == 'back')
async def process_choice_service_back(callback: CallbackQuery):
    """Срабатывает на нажатие кнопки 'Назад' при выборе услуги"""
    keyboard = await get_service_keyboard()
    await callback.message.answer(text=other_lexicon.MESSAGE['choose_service'],
                                  reply_markup=keyboard)
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_service), F.data == 'next')
async def process_enter_number_sessions(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Далее' при выборе услуги.
    Переводит в состояние выбора количества посещений"""
    await state.set_state(FSMRecords.sessions_number)
    await callback.message.answer(text=other_lexicon.MESSAGE['enter_number_sessions'])
    await callback.answer()


@router.message(StateFilter(FSMRecords.choice_service))
async def warning_not_choice_service(message: Message):
    """Срабатывает, если вместо события нажатия кнопки, было совершено нечто другое"""
    await message.answer(text=other_lexicon.MESSAGE['not_choice_service'])
