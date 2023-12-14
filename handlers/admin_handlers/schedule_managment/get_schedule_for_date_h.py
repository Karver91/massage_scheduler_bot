from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from database.queries import schedule_table
from handlers.other_handlers.calendar_h import calendar_date_dispatcher
from keyboards.inline import calendar_kb
from keyboards.inline.start_menu_kb import get_start_keyboard
from lexicon import other_lexicon, admin_lexicon
from states.states import FSMRecords

router = Router()


@router.callback_query(F.data == 'remove_records', StateFilter(default_state))
async def process_choice_date(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки 'Посмотреть/Удалить запись на конкретную дату' для админа"""
    text = other_lexicon.MESSAGE['choice_date']
    await state.update_data(date_id=0)
    await state.set_state(FSMRecords.choice_date_remove)
    await calendar_date_dispatcher(message=callback, state=state, text=text)
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_date_remove), calendar_kb.CalendarCallback.filter(F.day != '0'))
async def process_date_press(callback: CallbackQuery, callback_data: calendar_kb.CalendarCallback, state: FSMContext):
    """Срабатывает на нажатие кнопки с выбором даты"""
    await state.update_data(date=f'{callback_data.year}{callback_data.month:>02}{callback_data.day:>02}')
    states = await state.get_data()
    keyboard = await calendar_kb.get_records_keyboard(date=states['date'])
    if len(keyboard.inline_keyboard) > 1:
        await state.set_state(FSMRecords.choice_record)
        await callback.message.answer(text=admin_lexicon.MESSAGE['choice_record_message'],
                                      reply_markup=keyboard)
    else:
        keyboard = await calendar_kb.get_calendar_keyboard(date_id=states['date_id'])
        await callback.message.answer(text=admin_lexicon.MESSAGE['no_record_message'],
                                      reply_markup=keyboard)
    await callback.answer()


@router.callback_query(StateFilter(FSMRecords.choice_record), calendar_kb.CalendarCallback.filter(F.day != '0'))
async def process_date_press_again(callback: CallbackQuery, callback_data: calendar_kb.CalendarCallback,
                                   state: FSMContext):
    await process_date_press(callback, callback_data, state)


@router.callback_query(F.data != 'cancel', StateFilter(FSMRecords.choice_record))
async def process_remove_record(callback: CallbackQuery, state: FSMContext):
    """Срабатывает на нажатие кнопки с записью, которую нужно удалить"""
    keyboard = await get_start_keyboard(admin_lexicon.COMMANDS['start_buttons'])
    states = await state.get_data()
    await schedule_table.delete_record(date=states['date'], time=callback.data)
    await callback.message.answer(text=admin_lexicon.MESSAGE['record_deleted'],
                                  reply_markup=keyboard)
    await state.clear()
    await callback.answer()
