import asyncio
import json
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config.settings import TELEGRAM_BOT_TOKEN
from handlers.photo_handler import router as photo_router
from handlers.start_handler import router as start_router

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация обработчиков
dp.include_router(start_router)
dp.include_router(photo_router)


# Функция для регистрации команд бота
async def set_commands():
    await bot.set_my_commands(
        [BotCommand(command="/start", description="стартануть мисис котят")]
    )


async def handler(event: dict, context: Any):
    try:
        body = json.loads(event.get("body", None))
    except Exception:
        return {"statusCode": 400, "body": json.dumps({"status": "not ok"})}
    if "body" in event:
        await dp.feed_raw_update(bot, body)
    return {"statusCode": 200, "body": json.dumps({"status": "ok"})}


