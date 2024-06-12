from aiogram.fsm.state import StatesGroup, State


class FSMGrenades(StatesGroup):
    side = State()
    type = State()


class FSMCreateGrenade(StatesGroup):
    map = State()
    side = State()
    type = State()
    title = State()
    description = State()
    image = State()
