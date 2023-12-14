from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний FSM
class FSMAddService(StatesGroup):
    """Класс машины состояний для добавления новой услуги в базу услуг"""
    service_name = State()
    service_duration = State()
    service_price = State()
    service_description = State()


class FSMRemoveService(StatesGroup):
    """Класс машины состояний для удаления услуги из базы услуг"""
    state_remove = State()


class FSMRecords(StatesGroup):
    """Класс машины состояний для работы с записью клиентов"""
    client_first_name = State()
    client_last_name = State()
    client_phone = State()
    choice_service = State()
    sessions_number = State()
    choice_date = State()
    choice_date_remove = State()
    choice_time = State()
    choice_record = State()

