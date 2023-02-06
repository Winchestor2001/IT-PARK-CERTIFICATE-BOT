from aiogram import Dispatcher
from aiogram.types import *
from data.config import ADMINS
from loader import dp
from utils.misc.extract_excel import extract_excel_file


async def bot_start(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer(f"Assalomu aleykum")


async def get_excel_file_handler(message: Message):
    await message.document.download(destination_file=message.document.file_name)
    await extract_excel_file(message.document.file_name)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
    dp.register_message_handler(get_excel_file_handler, content_types=['document'])

