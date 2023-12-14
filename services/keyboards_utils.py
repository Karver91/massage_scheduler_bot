import calendar
import datetime

from config.config import WEEKEND, MONTH_LIMIT, WORKING_TIME
from database.queries import schedule_table, service_table


# -------------------------------------- Функции календаря -----------------------------------------
async def get_date(date_id: int) -> tuple:
    """Принимает id даты для страницы календаря
    Возвращает дату в соотвествии с id"""
    date = datetime.date.today()
    year, month, day = date.year, date.month, date.day
    for i in range(date_id):
        month += 1
        if month > 12:
            month = 1
            year += 1

    return year, month, day


async def get_working_days_for_month(date_id: int, date: tuple, months_limith: int = MONTH_LIMIT):
    """Проверяет рабочие дни месяца"""
    month_calendar = calendar.monthcalendar(year=date[0], month=date[1])
    today = date[2]
    for week in month_calendar:
        for indx in range(7):
            __check_weekend(week, indx)
            if date_id == 0:
                __less_than(week, indx, today)
            elif date_id == months_limith:
                __greater_than(week, indx, today)
    return month_calendar


def __check_weekend(week, indx):
    if indx in WEEKEND:
        week[indx] = 0


def __greater_than(week, indx, today):
    if week[indx] > today:
        week[indx] = 0


def __less_than(week, indx, today):
    if week[indx] < today:
        week[indx] = 0


# -------------------------------------- Функции времени -----------------------------------------

async def get_free_time_on_date(date: str, service_id: str) -> list[datetime.timedelta]:
    """Получает свободное время для записи на переданную дату"""
    occupied_time_list: list[dict] = await schedule_table.get_time_and_duration_for_date_from_schedule(date)
    service_description: dict = await service_table.get_service_description_from_db(service_id)
    user_service_duration: int = service_description['duration']
    working_hours_list_copy: list = list(WORKING_TIME[:])
    index = 0

    for service_time in occupied_time_list:
        # Вычисляю время окончания услуги: время ее начала + ее длительность
        service_end_time = service_time['time'] + datetime.timedelta(minutes=service_time['duration'])
        service_time = service_time['time']

        for working_time in WORKING_TIME[index:]:
            # Вычисляю время окончания процедуры, на которую записывается клиент, от текущего времени
            user_service_end_time = working_time + datetime.timedelta(minutes=user_service_duration)

            if working_time < service_end_time <= user_service_end_time or \
                    service_time < user_service_end_time <= service_end_time:
                working_hours_list_copy.remove(working_time)

            if working_time >= service_end_time:
                index = WORKING_TIME.index(working_time)
                break

    return working_hours_list_copy
