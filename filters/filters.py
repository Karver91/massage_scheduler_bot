import re
import datetime


async def check_add_service_name(message):
    """Проверяет, чтобы название сервиса состояло из букв, возможны пробелы"""
    if message.text:
        return bool(re.match(r'^[а-яА-Яa-zA-Z\s]*[а-яА-Яa-zA-Z]+$', message.text))


async def check_phone_number(message):
    return bool(re.match(r'^8\d{10}$', message.text))


# async def check_user_name(message):
#     """Проверяет, чтобы имя и фамилия пользователя состояло из букв и минимум двух слов"""
#     return bool(re.match(r'([А-ЯЁ][а-яё]+[\-\s]?){2,}', message.text))


async def check_date(callback):
    """Проверяет, что клиент записывается на актуальную дату"""
    date = list(map(int, callback.data.split(':')[1:]))
    return datetime.date.today() > datetime.date(year=date[0], month=date[1], day=date[2])


async def check_session_number(message):
    if message.text.isdigit():
        return 0 < int(message.text) <= 10
    return False
