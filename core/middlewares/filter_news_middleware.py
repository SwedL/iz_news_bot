from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.news_sources.iz_news_source import IZNewsSource


class FilterNewsMiddleware(BaseMiddleware):
    """Служит для отправки ссылки на экземпляр класса IZNewsSource, в обработчик сообщений чат-бота,
    для доступа к фильтру рубрик"""

    def __init__(self, source: IZNewsSource) -> None:
        self.source = source

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        data['source'] = self.source
        return await handler(event, data)
