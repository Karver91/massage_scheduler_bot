from aiogram import Router

from config.config import ADMIN_IDS
from handlers.admin_handlers import command_h
from handlers.admin_handlers.client_managment import add_client_h, get_client_list_h
from handlers.admin_handlers.schedule_managment import get_schedule_h, get_schedule_for_date_h
from handlers.admin_handlers.service_management import add_service_h, remove_service_h

router = Router()

# Регистрирует в роутер фильтры по id администраторов бота.
router.message.filter(lambda message: message.from_user.id in ADMIN_IDS)
router.callback_query.filter(lambda message: message.from_user.id in ADMIN_IDS)

router.include_router(command_h.router)
router.include_router(add_client_h.router)
router.include_router(get_client_list_h.router)
router.include_router(get_schedule_h.router)
router.include_router(get_schedule_for_date_h.router)
router.include_router(add_service_h.router)
router.include_router(remove_service_h.router)
