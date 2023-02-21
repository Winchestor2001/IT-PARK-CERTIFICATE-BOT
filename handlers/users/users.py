from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import *
from data.config import ADMINS
from database.connections import add_user, get_certificate_by_id, get_total_certificate, filter_district_category
from keyboards.default.admin_btns import menu_btn
from keyboards.inline.admin_btns import admin_menu_btn
from states.AllStates import SimpleStates
from utils.misc.context import main_statistics
from utils.misc.extract_excel import extract_excel_file
import os
from utils.misc.make_certificate import districts


async def bot_start(message: Message, state: FSMContext):
    await state.finish()
    await add_user(message.from_user.id, message.from_user.username)
    args = message.get_args()

    if args:
        certificate = await get_certificate_by_id(args)
        await message.answer_document(certificate['certificate'])
        return
    if message.from_user.id in ADMINS:
        btn = await menu_btn()
        await message.answer(f"Assalomu aleykum", reply_markup=btn)


async def admin_start(message: Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in ADMINS:
        total = await get_total_certificate()
        context = "Admin Panel:\n\n" + main_statistics.format(total)
        btn = await admin_menu_btn()
        await message.answer(context, reply_markup=btn)


async def make_certificate_handler(message: Message, state: FSMContext):
    text = message.text
    await message.answer("Excel faylni yuboring:")
    await state.update_data(name=text)
    await SimpleStates.make_certificate.set()


async def get_excel_file_handler(message: Message, state: FSMContext):
    await message.document.download(destination_file=message.document.file_name)
    data = await state.get_data()
    await extract_excel_file(message.document.file_name)
    file = InputFile("certificates/certificates.zip")
    await message.answer_document(file)
    await state.finish()
    os.unlink("certificates/certificates.zip")


async def filter_district_category_callback(c: CallbackQuery):
    await c.answer()
    cat = int(c.data.split(":")[-1])
    total = await get_total_certificate()
    category = await filter_district_category(districts[cat])
    context = "Admin Panel:\n\n" + main_statistics.format(total) + category + districts[cat]
    btn = await admin_menu_btn()
    await c.message.edit_text(context, reply_markup=btn)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'], state='*')
    dp.register_message_handler(admin_start, commands=['admin'], state='*')

    dp.register_message_handler(make_certificate_handler, content_types=['text'], text='Sertifikat tayyorlash')

    dp.register_message_handler(get_excel_file_handler, content_types=['document'], state=SimpleStates.make_certificate)

    dp.register_callback_query_handler(filter_district_category_callback, text_contains='filter:')

