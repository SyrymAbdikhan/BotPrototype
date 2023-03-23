
import logging

from aiogram import Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.loader import bot, dp
from bot.config import Config, Webhook
from bot.db.base import Base


def register_all_middlewares(dispatcher: Dispatcher) -> None:
    logging.info("Registering middlewares")
    dispatcher.setup_middleware(LoggingMiddleware())


def register_all_filters(dispatcher: Dispatcher) -> None:
    logging.info("Registering filters")


def register_all_handlers(dispatcher: Dispatcher) -> None:
    from bot.handlers import admin, common
    logging.info("Registering handlers")

    admin.register_commands(dispatcher)
    common.register_commands(dispatcher)


async def register_all_commands(dispatcher: Dispatcher) -> None:
    commands = [
        BotCommand(command='/subscribe', description='subscribe for bot'),
        BotCommand(command='/unsubscribe', description='unsubscribe for bot'),
    ]
    await dispatcher.bot.set_my_commands(commands)


async def get_async_sessionmaker(config: Config):
    db = config.db
    engine = create_async_engine(
        f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}',
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )


async def on_startup(dispatcher: Dispatcher, webhook_url: str = None) -> None:
    register_all_middlewares(dispatcher)
    register_all_filters(dispatcher)
    register_all_handlers(dispatcher)
    await register_all_commands(dispatcher)
    
    bot = dispatcher.bot
    webhook_url = bot.config.webhook.url

    webhook = await bot.get_webhook_info()
    if webhook_url:
        await dispatcher.bot.set_webhook(webhook_url)
        logging.info('Webhook was set')
    elif webhook.url:
        await dispatcher.bot.delete_webhook()
        logging.info('Webhook was deleted')

    dispatcher.bot.db = await get_async_sessionmaker(dispatcher.bot.config)
    logging.info('Bot started!')


async def on_shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logging.info("Bot shutdown!")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    logging.info("Initializing bot")

    webhook: Webhook = bot.config.webhook
    '''
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
    '''
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        webhook_path=webhook.path,
        skip_updates=True,
        host=webhook.app_host,
        port=webhook.app_port
    )


if __name__ == "__main__":
    main()
