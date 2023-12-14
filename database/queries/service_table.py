from database.db_init import database


# -------------------- Функции работы с базой услуг ----------------------------------

async def add_service_to_db(service):
    """Добавляет новую услугу в базу услуг"""
    await database.execute(
        query=f"INSERT INTO {database.db_name}.service (service_name, description, duration, price) "
              f"VALUES (%s, %s, %s, %s) AS v "
              f"ON DUPLICATE KEY UPDATE service_name = v.service_name, "
              f"description = v.description, "
              f"duration = v.duration, "
              f"price = v.price, "
              f"is_deleted = 0",
        values=(service['name'], service['description'], service['duration'], service['price']),
        commit=True)
    await database.close()


async def service_is_deleted_true(service_id):
    """Присваивает полю is_deleted значение True"""
    await database.execute(query=f"UPDATE {database.db_name}.service "
                                 f"SET is_deleted = 1 "
                                 f"WHERE id = %s",
                           values=service_id,
                           commit=True)
    await database.close()


async def remove_service_from_db():
    """Удаляет услугу из базы услуг при условии, что на нее не ссылаются записи из таблицы schedule"""
    await database.execute(query=f"DELETE FROM {database.db_name}.service "
                                 f"WHERE is_deleted = 1 "
                                 f"AND NOT EXISTS ("
                                 f"SELECT 1 FROM {database.db_name}.schedule "
                                 f"WHERE {database.db_name}.schedule.service_id = {database.db_name}.service.id"
                                 f")",
                           commit=True)
    await database.close()


async def get_services_from_db():
    """Получает все услуги из базы услуг"""
    await database.execute(query=f"SELECT * FROM {database.db_name}.service "
                                 f"WHERE is_deleted = 0 "
                                 f"ORDER BY service_name")
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def get_service_description_from_db(service_id):
    """Получает услугу из базы и ее описание"""
    await database.execute(query=f"SELECT * FROM {database.db_name}.service WHERE id = %s",
                           values=service_id)
    result = await database.cursor.fetchone()
    await database.close()
    return result
