from database.db_init import database


async def delete_old_records():
    """Удаляет старые записи"""
    await database.execute(query=f"DELETE FROM {database.db_name}.schedule WHERE date < NOW() - INTERVAL 1 DAY",
                           commit=True)
    await database.close()


async def delete_record(date, time):
    await database.execute(query=f"DELETE FROM {database.db_name}.schedule WHERE date = %s AND time = %s",
                           values=(date, time),
                           commit=True)


async def add_record_to_schedule(client_id, service_id, date, time):
    """Добавляем новую запись в расписание"""
    await database.execute(query=f"INSERT INTO {database.db_name}.schedule (client_id, service_id, date, time) "
                                 f"VALUES (%s, %s, %s, %s)",
                           values=(client_id, service_id, date, time),
                           commit=True)
    await database.close()


async def get_time_and_duration_for_date_from_schedule(date):
    """Возвращает время начала процедур и их продолжительность на текущий день"""
    await database.execute(
        query=f"SELECT time, duration FROM {database.db_name}.schedule, {database.db_name}.service WHERE "
              f"{database.db_name}.schedule.service_id = {database.db_name}.service.id AND "
              f"{database.db_name}.schedule.date = %s "
              f"ORDER BY time",
        values=date)
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def get_record_by_date_and_time(date, time):
    """Получает записи из расписания по дате и времени"""
    await database.execute(query=f"SELECT * FROM {database.db_name}.schedule WHERE date = %s AND time = %s",
                           values=(date, time))
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def get_record_by_user_id(user_id):
    """Получает запись клиента на услугу по его id"""
    await database.execute(query=f"SELECT service_name, date, time FROM {database.db_name}.schedule "
                                 f"JOIN {database.db_name}.service "
                                 f"ON {database.db_name}.schedule.service_id = {database.db_name}.service.id "
                                 f"JOIN {database.db_name}.client "
                                 f"ON {database.db_name}.schedule.client_id = {database.db_name}.client.id "
                                 f"WHERE telegram_id = %s "
                                 f"ORDER BY date, time",
                           values=user_id)
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def get_all_records_from_schedule():
    """Получает все записи из schedule"""
    await database.execute(query=f"SELECT service_name, first_name, last_name, date, time "
                                 f"FROM {database.db_name}.schedule "
                                 f"JOIN {database.db_name}.service "
                                 f"ON {database.db_name}.schedule.service_id = {database.db_name}.service.id "
                                 f"JOIN {database.db_name}.client "
                                 f"ON {database.db_name}.schedule.client_id = {database.db_name}.client.id "
                                 f"ORDER BY date, time")
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def get_schedule_for_date_from_db(date):
    """Получаем расписание из базы"""
    await database.execute(query=f"SELECT first_name, last_name, time "
                                 f"FROM {database.db_name}.schedule "
                                 f"JOIN {database.db_name}.client "
                                 f"ON {database.db_name}.schedule.client_id = {database.db_name}.client.id "
                                 f"WHERE date = %s "
                                 f"ORDER BY time",
                           values=date)
    result = await database.cursor.fetchall()
    await database.close()
    return result
