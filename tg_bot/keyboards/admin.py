from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MAPS
from models.grenade import Grenades, Grenade


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


def update_grenade_keyboard(grenades: Grenades) -> InlineKeyboardBuilder:
    """Клавиатура для выбора гранаты в обновлении"""
    keyboard = InlineKeyboardBuilder()
    for grenade in grenades.grenades:
        keyboard.row(InlineKeyboardButton(text=f"{grenade.map.upper()} | {grenade.side.upper()} | {grenade.type.upper()} | {grenade.title}",
                                          callback_data=f"update-grenade_{grenade.id}"))
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard


def fields_to_change_keyboard() -> InlineKeyboardBuilder:
    """Клавиатура для выбора изменяемого поля"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Карта", callback_data=f"update-field_map"))
    keyboard.row(InlineKeyboardButton(text="Заголовок", callback_data="update-field_title"))
    keyboard.row(InlineKeyboardButton(text="Описание", callback_data="update-field_description"))
    keyboard.row(InlineKeyboardButton(text="Тип гранаты", callback_data="update-field_type"))
    keyboard.row(InlineKeyboardButton(text="Сторона", callback_data="update-field_side"))
    keyboard.row(InlineKeyboardButton(text="Изображения", callback_data="update-field_images"))
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard


def fields_to_change_side_type_map(data: dict) -> InlineKeyboardBuilder:
    """Клавиатура для изменения 'типа гранаты', 'карты' и 'стороны' """
    keyboard = InlineKeyboardBuilder()

    if data["field"] == "map":
        for cs_map in MAPS:
            keyboard.row(InlineKeyboardButton(
                text=f"{cs_map.upper()}", callback_data=f"map_{cs_map}")
            )

    elif data["field"] == "type":
        keyboard.row(InlineKeyboardButton(text=f"Smoke", callback_data=f"type_smoke"))
        keyboard.row(InlineKeyboardButton(text=f"HE Grenade", callback_data=f"type_he"))
        keyboard.row(InlineKeyboardButton(text=f"Flashbang", callback_data=f"type_flash"))
        keyboard.row(InlineKeyboardButton(text=f"Molotov", callback_data=f"type_molotov"))

    elif data["field"] == "side":
        keyboard.row(InlineKeyboardButton(text=f"Terrorists", callback_data=f"side_T"))
        keyboard.row(InlineKeyboardButton(text=f"Counter-terrorists", callback_data=f"side_CT"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))

    return keyboard


def delete_image_keyboard(image_id: int) -> InlineKeyboardBuilder:
    """Клавиатура с кнопкой удалить для фотографий"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Удалить", callback_data=f"delete-image_{image_id}"))
    return keyboard


def fields_to_change_title_description() -> InlineKeyboardBuilder:
    """Клавиатура для изменения 'названия' и 'описания' """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard
