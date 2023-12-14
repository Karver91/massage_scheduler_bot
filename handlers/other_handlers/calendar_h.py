from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.queries.schedule_table import add_record_to_schedule
from filters.filters import check_date, check_session_number
from keyboards.inline import calendar_kb
from keyboards.inline.start_menu_kb import get_start_menu_kb
from lexicon import other_lexicon
from services.services import check_time_available, convert_str_date_to_datetime
from states.states import FSMRecords

router = Router()


@router.message(StateFilter(FSMRecords.sessions_number), check_session_number)
async def process_choice_date(message: CallbackQuery | Message, state: FSMContext):
    """Срабатывает на ввод количества услуг под запись"""
    text = other_lexicon.MESSAGE['choice_date']
    await state.update_data(date_id=0)
    await state.update_data(sessions_counter=int(message.text))
    await state.set_state(FSMRecords.choice_date)
    await calendar_date_dispatcher(message=message, state=state, text=text)


async def calendar_date_dispatcher(message: CallbackQuery | Message, state: FSMContext, text: str):
    data = await state.get_data()
    keyboard = await calendar_kb.get_calendar_keyboard(date_id=data['date_id'])
    if isinstance(message, Message):
        await message.answer(text=text,
                             reply_markup=keyboard)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text=text,
                                     reply_markup=keyboard)


@router.message(StateFilter(FSMRecords.sessions_number))
async def warning_not_sessions_number(message: Message):
    await message.answer(text='Введено неверное число')


@router.callback_query(StateFilter(FSMRecords.choice_date, FSMRecords.choice_date_remove), F.data.in_({'forward', 'backward'}))
async def process_pagination_press(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопок пагинации для перелистывания страницы календаря"""
    data = await state.get_data()
    if callback.data == 'forward':
        date_id = data['date_id'] + 1
    else:
        date_id = data['date_id'] - 1
    await state.update_data(date_id=date_id)

    keyboard = await calendar_kb.get_calendar_keyboard(date_id=date_id)
    await callback.message.edit_reply_markup(text=other_lexicon.MESSAGE['choice_date'],
                                             reply_markup=keyboard)
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_date, FSMRecords.choice_date_remove), F.data == '0')
@router.callback_query(StateFilter(FSMRecords.choice_date, FSMRecords.choice_date_remove),
                       calendar_kb.CalendarCallback.filter(F.day == '0'))
async def process_empty_press(callback: CallbackQuery):
    """Отлавливает нажатия на пустые кнопки"""
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_date, FSMRecords.choice_date_remove),
                       F.data[:11] == 'date_button', check_date)
async def check_date(callback: CallbackQuery):
    """Отлавливает нажатия на неактуальную дату"""
    await callback.message.answer(text='Эта дата неактуальна, выберете другую')
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_date), calendar_kb.CalendarCallback.filter(F.day != '0'))
async def process_date_press(callback: CallbackQuery, callback_data: calendar_kb.CalendarCallback, state: FSMContext):
    """Отлавливает нажатие на кнопку даты в календаре"""
    await state.set_state(FSMRecords.choice_time)
    await state.update_data(date=f'{callback_data.year}{callback_data.month:>02}{callback_data.day:>02}')
    states = await state.get_data()
    keyboard = await calendar_kb.get_time_to_record(date=states['date'], service_id=states['service_id'])
    if len(keyboard.inline_keyboard) > 1:
        await callback.message.answer(text=other_lexicon.MESSAGE['choice_time_message'],
                                      reply_markup=keyboard)
    else:
        await state.set_state(FSMRecords.choice_date)
        keyboard = await calendar_kb.get_calendar_keyboard(date_id=states['date_id'])
        await callback.message.answer(text=other_lexicon.MESSAGE['no_time_message'],
                                      reply_markup=keyboard)

    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_time), F.data == 'back')
async def process_choice_time_back(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Назад' при выборе времени для записи"""
    await state.set_state(FSMRecords.choice_date)
    states = await state.get_data()
    keyboard = await calendar_kb.get_calendar_keyboard(date_id=states['date_id'])
    await callback.message.answer(text=other_lexicon.MESSAGE['choice_date'],
                                  reply_markup=keyboard)
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_time), F.data != 'cancel')
async def process_time_press(callback: CallbackQuery, state: FSMContext):
    """Отлавливает нажатие на кнопку выбора времени для записи"""
    try:
        await state.update_data(time=callback.data)
        states = await state.get_data()
        if await check_time_available(date=states['date'], time=callback.data):
            await add_record_to_schedule(client_id=states['client_id'],
                                         service_id=states['service_id'],
                                         date=states['date'],
                                         time=states['time'])
            await session_counter_dispatcher(callback=callback, state=state)
        else:
            await callback.message.answer(text=other_lexicon.MESSAGE['recording_failed'])
            await process_choice_date(callback, state)
        await callback.answer()
    except ValueError:
        await callback.answer()


async def session_counter_dispatcher(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sessions_counter = data['sessions_counter']
    sessions_counter -= 1
    if sessions_counter > 0:
        datetime_date = await convert_str_date_to_datetime(data['date'])
        date = f'{datetime_date.day}.{datetime_date.month}.{datetime_date.year}'
        time = data['time']
        await state.update_data(sessions_counter=sessions_counter)
        text = other_lexicon.MESSAGE['recording_notice'].format(date=date, time=time[:-3],
                                                                sessions_counter=sessions_counter)
        await state.set_state(FSMRecords.choice_date)
        await calendar_date_dispatcher(message=callback, state=state, text=text)
    else:
        keyboard = await get_start_menu_kb(callback=callback)
        await callback.message.answer(text=other_lexicon.MESSAGE['recording_successful'],
                                      reply_markup=keyboard)
        await state.clear()
