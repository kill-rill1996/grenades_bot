from models.grenade import Grenade


def update_grenade_message(grenade: Grenade) -> str:
    """Сообщение со старыми значениями в виде breadcrumbs"""
    message = f"<b>{grenade.map.upper()}</b> | <b>{grenade.side.upper()}</b> | <b>{grenade.type.upper()}</b> | "

    if len(grenade.title) > 10:
        message += f"<b>{grenade.title[:10]}</b>..."
    else:
        message += f"<b>{grenade.title}</b>"

    message += f"\n\nВыберите что хотите изменить:"
    return message


def change_field_grenade_message(data: dict) -> str:
    """Сообщения со старым значением изменяемого поля и с предложением выбора нового"""
    message = ""
    if data["field"] == "map":
        message += f"Карта: <b>{data['grenade'].map.upper()}</b>\nВыберите карту из указанных ниже"
    elif data["field"] == "title":
        message += f"Название: <b>{data['grenade'].title}</b>\nНапишите новое название в сообщении"
    elif data["field"] == "description":
        message += f"Описание: <b>{data['grenade'].description}</b>\nНапишите новое описание в сообщении"
    elif data["field"] == "type":
        message += f"Тип гранты: <b>{data['grenade'].type.upper()}</b>\nВыберите тип гранаты из указанных ниже"
    elif data["field"] == "side":
        message += f"Тип гранты: <b>{'Terrorists' if data['grenade'].side == 'T' else 'Counter-terrorists'}</b>"
        message += f"\nВыберите тип гранаты из указанных ниже"
    elif data["field"] == "images":
        pass

    return message


def successful_grenade_changes_message(data: dict) -> str:
    """data: dict {"title": "type": "side":  "map": ...}"""
    message = f"Изменения успешно внесены в гранату <b>{data['map'].upper()}</b> | <b>{data['type'].upper()}</b> | {data['title']}"
    return message
