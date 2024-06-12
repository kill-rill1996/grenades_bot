from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MAPS
from models.grenade import Grenades


def maps_keyboard() -> InlineKeyboardBuilder:
    """Стартовая клавиатура с выбором карты"""
    keyboard = InlineKeyboardBuilder()
    for cs_map in MAPS:
        keyboard.row(InlineKeyboardButton(
            text=f"{cs_map.upper()}", callback_data=f"map_{cs_map}")
        )
    keyboard.adjust(2)
    return keyboard


def side_keyboard() -> InlineKeyboardBuilder:
    """Выбор стороны"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=f"Terrorists", callback_data=f"side_T"))
    keyboard.row(InlineKeyboardButton(text=f"Counter-terrorists", callback_data=f"side_CT"))
    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back-to-maps"))
    return keyboard


def grenade_type_keyboard() -> InlineKeyboardBuilder:
    """Выбор типа гранаты"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=f"Smoke", callback_data=f"type_smoke"))
    keyboard.row(InlineKeyboardButton(text=f"HE Grenade", callback_data=f"type_he"))
    keyboard.row(InlineKeyboardButton(text=f"Flashbang", callback_data=f"type_flash"))
    keyboard.row(InlineKeyboardButton(text=f"Molotov", callback_data=f"type_molotov"))
    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back-to-sides"))
    return keyboard


def grenade_titles_keyboard(grenades: list[Grenades]) -> InlineKeyboardBuilder:
    """Вывод title гранат"""
    keyboard = InlineKeyboardBuilder()

    for g in grenades:
        keyboard.row(InlineKeyboardButton(
            text=f"{g.title}", callback_data=f"grenadeId_{g.id}")
        )

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back-to-type"))
    return keyboard
