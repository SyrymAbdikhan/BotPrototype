
import logging

from aiogram import Dispatcher, types

from bot.db.models import User
from bot.filters import IsForAIFilter
from bot.ai import GPT

gpt = GPT()


async def cmd_start(message: types.Message):
    db_session = message.bot.get('db')

    async with db_session() as session:
        await session.merge(User(user_id=message.from_user.id))
        await session.commit()

    await message.answer(f'Hi {message.from_user.first_name}! I am a dummy bot for tasting stuff so dont mind. '
                          'Also you automatically subscribed to this bot')


async def cmd_subscribe(message: types.Message):
    db_session = message.bot.get('db')

    async with db_session() as session:
        user: User = await session.get(User, message.from_user.id)

    if user.subscribed:
        return await message.answer('You already subscribed')

    async with db_session() as session:
        await session.merge(User(user_id=message.from_user.id, subscribed=True))
        await session.commit()

    await message.answer('You subscribed!')


async def cmd_unsubscribe(message: types.Message):
    db_session = message.bot.get('db')

    async with db_session() as session:
        user: User = await session.get(User, message.from_user.id)

    if not user.subscribed:
        return await message.answer('You already unsubscribed')

    async with db_session() as session:
        await session.merge(User(user_id=message.from_user.id, subscribed=False))
        await session.commit()

    await message.answer('You unsubscribed ;(')


async def ai_chat_handler(message: types.Message):
    res = await gpt.query(message.text)
    await message.answer(res)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_subscribe, commands='subscribe')
    dp.register_message_handler(cmd_unsubscribe, commands='unsubscribe')
    dp.register_message_handler(ai_chat_handler, IsForAIFilter())
