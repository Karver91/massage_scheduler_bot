from database.db_init import database


async def add_client_to_db(telegram_id, client):
    await database.execute(
        query=f'INSERT INTO {database.db_name}.client (telegram_id, first_name, last_name, phone_number) '
              f'VALUES (%s, %s, %s, %s) AS v '
              f'ON DUPLICATE KEY UPDATE telegram_id = v.telegram_id',
        values=(telegram_id,
                client['client_first_name'],
                client['client_last_name'],
                client['client_phone']),
        commit=True)
    await database.close()


async def remove_client_from_db():
    """Удаляет клиента из базы при условии, что на него не ссылаются записи из таблицы schedule"""
    await database.execute(query=f"DELETE FROM {database.db_name}.client "
                                 f"WHERE NOT EXISTS ("
                                 f"SELECT 1 FROM {database.db_name}.schedule "
                                 f"WHERE {database.db_name}.schedule.client_id = {database.db_name}.client.id"
                                 f")",
                           commit=True)
    await database.close()


async def get_phone(first_name, last_name):
    await database.execute(query=f'SELECT id, phone_number FROM {database.db_name}.client '
                                 f'WHERE first_name = %s AND last_name = %s',
                           values=(first_name, last_name))
    result = await database.cursor.fetchone()
    await database.close()
    return result


async def get_client_by_phone(phone):
    await database.execute(query=f'SELECT * FROM {database.db_name}.client '
                                 f'WHERE phone_number = %s',
                           values=phone)
    result = await database.cursor.fetchone()
    await database.close()
    return result


async def get_client_by_telegram_id(telegram_id):
    await database.execute(query=f'SELECT * FROM {database.db_name}.client '
                                 f'WHERE telegram_id = %s',
                           values=telegram_id)
    result = await database.cursor.fetchone()
    await database.close()
    return result


async def get_client_list_from_db():
    await database.execute(query=f'SELECT first_name, last_name, phone_number FROM {database.db_name}.client '
                                 f'ORDER BY last_name')
    result = await database.cursor.fetchall()
    await database.close()
    return result
