from aiogram import Router

from handlers.user_handlers import command_h, get_contacts_h, make_appointment_h, view_appointment_h

router = Router()
router.include_router(command_h.router)
router.include_router(get_contacts_h.router)
router.include_router(make_appointment_h.router)
router.include_router(view_appointment_h.router)
