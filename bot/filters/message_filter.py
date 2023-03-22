
import os
import logging

from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter

from bot.loader import bot


class IsForAIFilter(BoundFilter):
    keyword=tuple(eval(os.getenv('KEYWORD', ['dummy', 'дамеке'])))

    async def check(self, message: Message) -> bool:
        if len(message.text) == 0:
            return False

        if message.chat.type == ChatType.PRIVATE:
            return True

        if message.text.startswith(self.keyword):
            return True

        if message.reply_to_message:
            if message.reply_to_message.from_user.id == bot.id:
                return True

        return False
