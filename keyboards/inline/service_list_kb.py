from aiogram.types import InlineKeyboardMarkup

from database.queries.schedule_table import delete_old_records
from database.queries.service_table import get_services_from_db
from keyboards.inline.builder import create_inline_kb


async def get_service_keyboard() -> InlineKeyboardMarkup:
    """Получает список услуг и формирует из них клавиатуру на лету"""
    id_name_dict: dict = dict()
    services: list[dict] = await get_services_from_db()
    for service in services:
        id_name_dict[service['id']] = service['service_name']
    id_name_dict['cancel'] = 'Отмена'
    keyboard = await create_inline_kb(id_name_dict)
    return keyboard
