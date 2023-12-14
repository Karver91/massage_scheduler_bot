from aiogram import Router

from handlers.other_handlers import other_h, service_h, calendar_h

router = Router()
router.include_router(service_h.router)
router.include_router(calendar_h.router)
router.include_router(other_h.router)
