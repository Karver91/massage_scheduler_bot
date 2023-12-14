import datetime

from database.queries import client_table, schedule_table


async def check_time_available(date: str, time: str) -> bool:
    """Проверяет не занято ли текущее время"""
    t = datetime.datetime.strptime(time, '%H:%M:%S')
    td = datetime.timedelta(hours=t.hour, minutes=t.minute)
    result = await schedule_table.get_record_by_date_and_time(date=date, time=td)
    return not bool(result)


async def convert_str_date_to_datetime(str_date: str):
    return datetime.datetime.strptime(str_date, '%Y%m%d')


async def get_all_records() -> str:
    """Возвращает все текущие записи"""
    records_list: list[dict] = await schedule_table.get_all_records_from_schedule()
    result: list = []

    for data in records_list:
        service_name = data['service_name']
        first_name = data['first_name']
        last_name = data['last_name']
        date = data['date']
        time = data['time']
        result.append(f"{date.day:>02}.{date.month:>02}.{date.year} в {str(time)[:-3]}:\n"
                      f"{last_name} {first_name}\n"
                      f"{service_name}\n")
    if result:
        result.insert(0, 'Все доступные записи:\n')
    else:
        result.append('Записей не найдено')

    result: str = '\n'.join(result)
    return result


async def get_client_list() -> str:
    """Возвращает список клиентов"""
    clients: list[dict] = await client_table.get_client_list_from_db()
    result: list = []

    for data in clients:
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone_number'].replace(data['phone_number'][0], '+7', 1)

        result.append(f"{last_name} {first_name}\n"
                      f"{phone}\n")
    if result:
        result.insert(0, 'Список клиентов:\n')
    else:
        result.append('Записей не найдено')

    result: str = '\n'.join(result)

    return result


async def get_appointment(user_id: int) -> str:
    """Возвращает запись клиента по его id"""
    records_list = await schedule_table.get_record_by_user_id(user_id=user_id)
    result: list = []

    for data in records_list:
        name = data['service_name']
        date = data['date']
        time = data['time']
        result.append(f"{date.day:>02}.{date.month:>02}.{date.year} в {str(time)[:-3]}:\n{name}\n")

    if result:
        result.insert(0, 'Cписок ваших процедур:\n')
    else:
        result.append('Вы еще не записались на процедуру')
    result: str = '\n'.join(result)
    return result
