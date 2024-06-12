from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.grenade import Grenades


def grenades_keyboard(grenades: Grenades) -> InlineKeyboardBuilder:
    """Вывод списка title гранат"""
    keyboard = InlineKeyboardBuilder()
    for grenade in grenades.grenades:
        keyboard.row(InlineKeyboardButton(text=f"{grenade.type.upper()} | {grenade.title}", callback_data=f"delete_{grenade.id}"))

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back-to-maps"))
    return keyboard


def yes_no_keyboard(grenade_id: str) -> InlineKeyboardBuilder:
    """Клавиатура Да/Нет"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Да", callback_data=f"delete-confirmation-yes_{grenade_id}"),
        InlineKeyboardButton(text="Нет", callback_data=f"delete-confirmation-no_")
    )

    return keyboard
