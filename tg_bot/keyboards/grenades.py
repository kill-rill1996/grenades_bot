from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MAPS
from models.grenade import Grenades


def maps_keyboard() -> InlineKeyboardBuilder:
    """Стартовая клавиатура с выбором карты"""
    keyboard = InlineKeyboardBuilder()
    for cs_map in MAPS:
        keyboard.row(InlineKeyboardButton(
            text=f"{cs_map}", callback_data=f"map_{cs_map}")
        )
    keyboard.adjust(2)
    return keyboard


def side_keyboard() -> InlineKeyboardBuilder:
    """Выбор стороны"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=f"T", callback_data=f"side_t"))
    keyboard.row(InlineKeyboardButton(text=f"CT", callback_data=f"side_ct"))
    keyboard.adjust(2)
    return keyboard


def grenade_type_keyboard() -> InlineKeyboardBuilder:
    """Выбор типа гранаты"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=f"Smoke", callback_data=f"type_smoke"))
    keyboard.row(InlineKeyboardButton(text=f"HE", callback_data=f"type_he"))
    keyboard.row(InlineKeyboardButton(text=f"Flash", callback_data=f"type_flash"))
    keyboard.row(InlineKeyboardButton(text=f"Molotov", callback_data=f"type_molotov"))
    keyboard.adjust(2)
    return keyboard


def grenade_titles_keyboard(grenades: list[Grenades]) -> InlineKeyboardBuilder:
    """Вывод title гранат"""
    keyboard = InlineKeyboardBuilder()
    for g in grenades:
        keyboard.row(InlineKeyboardButton(
            text=f"{g.title}", callback_data=f"grenadeId_{g.id}")
        )
    return keyboard
