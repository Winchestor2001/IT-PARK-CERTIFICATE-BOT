from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.connections import filter_districts
from utils.misc.make_certificate import districts


async def admin_menu_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    districts_num = await filter_districts(districts)
    btn.add(
        *[
            InlineKeyboardButton(text=f"{value} ({total})", callback_data=f"filter:{key}") for key, value, total in zip(districts.keys(), districts.values(), districts_num)]
        ,
    )
    return btn
