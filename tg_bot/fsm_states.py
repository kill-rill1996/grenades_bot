from aiogram.fsm.state import StatesGroup, State


class FSMGrenades(StatesGroup):
    side = State()
    type = State()
