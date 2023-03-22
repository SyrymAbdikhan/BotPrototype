
import logging

from aiogram import Dispatcher, types
from sqlalchemy import select

from bot.db.models import User


async def cmd_report(message: types.Message):
    db_session = message.bot.get('db')
    
    sql = select(User).order_by(User.reg_time.desc()).limit(10)
    async with db_session() as session:
        users = (await session.execute(sql)).scalars()

    info = [f'ID: "{user.user_id}"\nReg. Datetime: "{user.reg_time}"\nIs Subscribed: "{str(user.subscribed)}"' for user in users[::-1]]
    text = "\n\n".join(info)
    
    await message.answer(text)


def register_commands(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_report, lambda m: m.from_user.id == admin_id, commands='report')
