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
    images = State()


class FSMUpdateGrenade(StatesGroup):
    grenade = State()
    field = State()
    updating = State()


class FSMAddImages(StatesGroup):
    map = State()
    grenade = State()
    getImages = State()

