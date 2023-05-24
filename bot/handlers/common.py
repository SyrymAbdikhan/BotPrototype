
from aiogram import Dispatcher, types

from bot.db.models import User
from bot.filters import IsForAIFilter
from bot.ai import GPT
from bot.utils.funcs import get_db

gpt = GPT()


async def cmd_start(message: types.Message):
    db_session = get_db(message.bot['db'])

    user_id = message.from_user.id
    user = User.find(db_session, user_id)
    if user is None:
        user = User(user_id=user_id)
        await user.save(db_session)

    await message.answer(f'Hi {message.from_user.first_name}! I am a dummy bot for tasting stuff so dont mind. '
                         'Also you automatically subscribed to this bot')


async def cmd_subscribe(message: types.Message):
    db_session = get_db(message.bot['db'])

    user_id = message.from_user.id
    user = User.find(db_session, user_id)
    if user is None:
        user = User(user_id=user_id, subscribed=True)
        await user.save(db_session)

    if user.subscribed:
        return await message.answer('You already subscribed =)')

    await message.answer('You subscribed! ^.^')


async def cmd_unsubscribe(message: types.Message):
    db_session = get_db(message.bot['db'])
    
    user_id = message.from_user.id
    user = User.find(db_session, user_id)
    if user is None:
        user = User(user_id=user_id, subscribed=False)
        await user.save(db_session)

    if not user.subscribed:
        return await message.answer('You already unsubscribed ;(')

    await message.answer('You unsubscribed ;(')


async def ai_chat_handler(message: types.Message):
    res = await gpt.query(message.text)
    await message.answer(res)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_subscribe, commands='subscribe')
    dp.register_message_handler(cmd_unsubscribe, commands='unsubscribe')
    dp.register_message_handler(ai_chat_handler, IsForAIFilter())
