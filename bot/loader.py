
from aiogram import Bot, Dispatcher

from bot.config import Config, load_config

config: Config = load_config()
bot = Bot(config.bot.token)
dp = Dispatcher(bot)
bot["config"] = config
