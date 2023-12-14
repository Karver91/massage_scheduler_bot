from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.config import MONTH_LIMIT
from database.queries import schedule_table
from lexicon.other_lexicon import MONTHS, DAYS_OF_THE_WEEK
from services import keyboards_utils


class CalendarCallback(CallbackData, prefix='date_button'):
    """Фабрика коллбэков для дат календаря"""
    year: str
    month: str
    day: str


# -------------------------------- Клавиатура календаря -------------------------------------

async def get_calendar_keyboard(date_id) -> InlineKeyboardMarkup:
    """Принимает id страницы календаря.
    Возвращает инлайн клавиатуру календаря"""
    date: tuple = await keyboards_utils.get_date(date_id)
    month_calendar: list[list] = await keyboards_utils.get_working_days_for_month(date_id, date)
    pagination = await _get_pagination(date, date_id)
    keyboard: list = list()
    date: tuple = (str(date[0]), str(date[1]))
    for i in range(len(month_calendar)):
        keyboard.append([])
        for j in range(7):
            day_num = str(month_calendar[i][j])
            if day_num == '0':
                text = ' '
            else:
                text = day_num
            keyboard[i].append(InlineKeyboardButton(text=text,
                                                    callback_data=CalendarCallback(year=date[0],
                                                                                   month=date[1],
                                                                                   day=day_num).pack()))

    days_of_the_week = _get_days_of_the_week()
    keyboard.insert(0, days_of_the_week)
    keyboard.append(pagination)
    keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def _get_days_of_the_week() -> list:
    """Возвращает список из кнопок с днями недели"""
    days_of_the_week_buttons = list()
    for text in DAYS_OF_THE_WEEK:
        days_of_the_week_buttons.append(InlineKeyboardButton(text=text,
                                                             callback_data='0'))
    return days_of_the_week_buttons


async def _get_pagination(date, date_id) -> list:
    """Возвращает список кнопок пагинации"""
    date_btn = InlineKeyboardButton(text=f'{MONTHS[date[1]]} {date[0]}',
                                    callback_data='0')
    if date_id == 0:
        pagination = [pagination_buttons['empty'], date_btn, pagination_buttons['>>']]
    elif date_id == MONTH_LIMIT:
        pagination = [pagination_buttons['<<'], date_btn, pagination_buttons['empty']]
    else:
        pagination = [pagination_buttons['<<'], date_btn, pagination_buttons['>>']]

    return pagination


# ------------------------------------ Клавиатуры времени ----------------------------------
async def get_time_to_record(date: str, service_id: str):
    """Возвращает клавиатуру со свободным временем для записи"""
    time_to_record_list: list = await keyboards_utils.get_free_time_on_date(date, service_id)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for time in time_to_record_list:
        buttons.append(InlineKeyboardButton(
            text=str(time)[:-3],
            callback_data=str(time)
        ))

    keyboard: InlineKeyboardMarkup = kb_builder.row(*buttons, width=3).as_markup()
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    return keyboard


async def get_records_keyboard(date):
    """Возвращает клавиатуру с записями пользователей на текущую дату"""
    records_list: list[dict] = await schedule_table.get_schedule_for_date_from_db(date=date)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for record in records_list:
        buttons.append(InlineKeyboardButton(
            text=f"{str(record['time'])[:-3]} - {record['last_name']} {record['first_name']}",
            callback_data=str(record['time'])
        ))
    cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
    keyboard: InlineKeyboardMarkup = kb_builder.row(*buttons, cancel, width=1).as_markup()
    return keyboard


# Кнопки пагинации
pagination_buttons = {'<<': InlineKeyboardButton(text='<<',
                                                 callback_data='backward'),
                      '>>': InlineKeyboardButton(text='>>',
                                                 callback_data='forward'),
                      'empty': InlineKeyboardButton(text=' ',
                                                    callback_data='0')}
