from typing import Callable, Dict, Any, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class CheckIsAdminMiddleware(BaseMiddleware):
    """Проверка является ли пользователь админом"""
    def __init__(self, admins: List[int]):
        self.admins = admins

    def is_admin(self, user_id) -> bool:
        return user_id in self.admins

    async def __call__(self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        # проверяем является ли пользователь админом
        if self.is_admin(data["event_from_user"].id):
            return await handler(event, data)

        # ответ для обычных пользователей
        await event.answer(
            "Эта функция доступна только для администраторов"
        )
        return


