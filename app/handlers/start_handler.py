from aiogram import Router, types
from aiogram.filters import CommandStart

from constants.texts import WELCOME_MESSAGE

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(WELCOME_MESSAGE)
