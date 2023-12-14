from keyboards.inline.builder import create_inline_kb


async def get_cancel_kb():
    """Возвращает кнопку 'Отмена'"""
    keyboard = await create_inline_kb({'cancel': 'Отмена'})
    return keyboard


async def get_next_cancel_kb():
    """Возвращает клавиатуру 'Далее/Отмена'"""
    keyboard = await create_inline_kb({'next': 'Далее', 'cancel': 'Отмена'})
    return keyboard


async def get_next_back_kb():
    """Возвращает клавиатуру 'Далее/Назад'"""
    keyboard = await create_inline_kb({'next': 'Далее', 'back': 'Назад'})
    return keyboard
