from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MAPS
from models.grenade import Grenades


def maps_keyboard() -> InlineKeyboardBuilder:
    """Клавиатура с выбором карты для удаления"""
    keyboard = InlineKeyboardBuilder()
    for cs_map in MAPS:
        keyboard.row(InlineKeyboardButton(
            text=f"{cs_map.upper()}", callback_data=f"delete-map_{cs_map}")
        )
    keyboard.adjust(2)

    return keyboard


def grenades_keyboard(grenades: Grenades) -> InlineKeyboardBuilder:
    """Вывод списка title гранат"""
    keyboard = InlineKeyboardBuilder()
    for grenade in grenades.grenades:
        keyboard.row(InlineKeyboardButton(text=f"{grenade.type.upper()} | {grenade.title}", callback_data=f"delete_{grenade.id}"))

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back-to-map-list"))
    return keyboard


def yes_no_keyboard(grenade_id: str) -> InlineKeyboardBuilder:
    """Клавиатура Да/Нет"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Да", callback_data=f"delete-confirmation-yes_{grenade_id}"),
        InlineKeyboardButton(text="Нет", callback_data=f"delete-confirmation-no_")
    )

    return keyboard


def maps_keyboard_with_cancel() -> InlineKeyboardBuilder:
    """Список карт с кнопкой отмены"""
    keyboard = InlineKeyboardBuilder()
    for cs_map in MAPS:
        keyboard.row(InlineKeyboardButton(text=f"{cs_map.upper()}", callback_data=f"map_{cs_map}"))
    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def sides_keyboard_with_cancel() -> InlineKeyboardBuilder:
    """Выбор стороны с кнопкой отмены"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Counter-terrorists", callback_data=f"side_CT"),
        InlineKeyboardButton(text="Terrorists", callback_data=f"side_T"))

    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def types_keyboard_with_cancel() -> InlineKeyboardBuilder:
    """Выбор типа гранаты с кнопкой отмены"""
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text=f"Smoke", callback_data=f"type_smoke"))
    keyboard.row(InlineKeyboardButton(text=f"HE Grenade", callback_data=f"type_he"))
    keyboard.row(InlineKeyboardButton(text=f"Flashbang", callback_data=f"type_flash"))
    keyboard.row(InlineKeyboardButton(text=f"Molotov", callback_data=f"type_molotov"))
    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def cancel_keyboard() -> InlineKeyboardBuilder:
    """Клавиатура с одной кнопкой отмены"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard
