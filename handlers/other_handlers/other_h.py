from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import other_lexicon

router: Router = Router()


# Кнопка Отмена
@router.callback_query(F.data == 'cancel')
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=other_lexicon.COMMANDS['cancel'])
    await callback.answer()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(StateFilter(default_state))
async def send_answer(message: Message):
    await message.answer(text=other_lexicon.MESSAGE['other_answer'])


@router.callback_query()
async def use_old_callback(callback: CallbackQuery):
    await callback.message.answer(text=other_lexicon.MESSAGE['use_old_callback'])
    await callback.answer()
