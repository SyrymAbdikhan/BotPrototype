
from os import getenv
from dataclasses import dataclass


@dataclass
class Bot:
    token: str
    admin_id: int


@dataclass
class Webhook:
    host: str
    path: str
    url: str

    app_host: str
    app_port: int

    def __post_init__(self):
        self.url = self.host + self.path


@dataclass
class DB:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass
class Config:
    bot: Bot
    webhook: Webhook
    db: DB


def load_config():
    return Config(
        bot=Bot(
            token=getenv('BOT_TOKEN'),
            admin_id=getenv('ADMIN_ID')
        ),
        webhook=Webhook(
            host=getenv('WEBHOOK_HOST'),
            path=f"/bot/{getenv('BOT_TOKEN')}",
            url='',
            app_host=getenv('APP_HOST'),
            app_port=getenv('APP_PORT')
        ),
        db=DB(
            host=getenv('DB_HOST'),
            port=int(getenv('DB_PORT')),
            name=getenv('DB_NAME'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASS')
        )
    )
