import asyncio

from aiocron import crontab
from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN
from database.backup.backup import csv_email_sender
from database.db_init import database
from database.queries.client_table import remove_client_from_db
from database.queries.schedule_table import delete_old_records
from database.queries.service_table import remove_service_from_db
from routers import admin_router, user_router, other_router


async def main():
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=BOT_TOKEN)
    dp: Dispatcher = Dispatcher()

    # Инициализируем Базу Данных
    await database.create_tables()

    # Запуск планированных задач
    crontab('59 23 * * *', func=delete_old_records)
    crontab('0 5 * * *', func=remove_client_from_db)
    crontab('0 5 * * 0', func=remove_service_from_db)
    crontab('0 0 * * *', func=csv_email_sender)

    # Регистрируем роутеры в диспетчере
    dp.include_router(router=admin_router.router)
    dp.include_router(router=user_router.router)
    dp.include_router(router=other_router.router)

    # Пропускаем апдейты и запускаем пулинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
