from PIL import Image, ImageDraw, ImageFont
import os
from zipfile import ZipFile, ZIP_DEFLATED
import qrcode

import database.connections as dc
from loader import bot
from aiogram.types import InputFile


districts = {
    1: 'Chortoq', 2: 'Chust', 3: 'Kosonsoy', 4: 'Mingbuloq', 5: 'Namangan tuman', 6: 'Namangan shahar',
    7: 'Norin', 8: 'Pop', 9: 'To`raqo`rg`on', 10: 'Uchqo`rg`on', 11: 'Uychi', 12: 'Yangiqo`rgon'
}


async def get_img_sizes(draw, img, text, font):
    w, h = draw.textsize(text, font)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return x, y


async def make_qrcode_img(unique_id):
    url = f"https://t.me/it_park_namangan_certificate_bot?start={unique_id}"
    qr = qrcode.make(url)
    qr.save(f"certificates/qr_{unique_id}.png")
    return f"certificates/qr_{unique_id}.png"


async def draw_certificate(image, data):
    images_name = []
    certificates = await dc.get_all_certificates()
    last_unique_id = len(certificates) if certificates else 0
    unique_id = "{:05d}".format(int(last_unique_id) + 1)

    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 120)
    font2 = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 65)

    qr_img = Image.open(await make_qrcode_img(unique_id))
    img.paste(qr_img, (3100, 0))

    x, y = await get_img_sizes(draw, img, str(data['name']).upper(), font)
    draw.text((x, (y - 130)), str(data['name']).upper(), fill='black', font=font)

    x, y = await get_img_sizes(draw, img, str(data['total_hour']), font2)
    draw.text(((x - 420), (y + 200)), str(data['total_hour']), fill='black', font=font2)

    x, y = await get_img_sizes(draw, img, str(data['start_date']), font2)
    draw.text(((x - 200), (y + 370)), f"{data['start_date']} - {data['end_date']}", fill='black', font=font2)

    x, y = await get_img_sizes(draw, img, f"ID:{unique_id}", font2)
    draw.text(((x + 500), (y + 840)), f"ID:{unique_id}", fill='black', font=font2)
    img.save(f"certificates/user_{unique_id}.jpg")
    images_name.append(f"certificates/user_{unique_id}.jpg")
    os.unlink(await make_qrcode_img(unique_id))
    await img_to_pdf_file(images_name, str(data['direction']), str(data['district']))


async def draw_certificate2(image, data):
    # print(data)
    images_name = []
    certificates = await dc.get_all_certificates()
    last_unique_id = len(certificates) if certificates else 0
    unique_id = "{:05d}".format(int(last_unique_id) + 1)

    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 140)
    font2 = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 70)

    qr_img = Image.open(await make_qrcode_img(unique_id))
    img.paste(qr_img, (1600, 1900))

    draw.text((200, 1200), str(data['name']).upper(), fill='black', font=font)

    x, y = await get_img_sizes(draw, img, str(data['end_date']), font2)
    draw.text(((x + 1000), (y + 850)), str(data['end_date']), fill='black', font=font2)

    x, y = await get_img_sizes(draw, img, f"ID:{unique_id}", font2)
    draw.text(((x + 1000), (y + 660)), f"ID:{unique_id}", fill='black', font=font2)

    img.save(f"certificates/user_{unique_id}.jpg")
    images_name.append(f"certificates/user_{unique_id}.jpg")
    os.unlink(await make_qrcode_img(unique_id))
    await img_to_pdf_file(images_name, str(data['direction']), str(data['district']))


async def img_to_pdf_file(images, category, district):
    for img in images:
        pdf_name = img.split("/")[-1].split(".")[0] + ".pdf"
        image = Image.open(img)
        image.save(f"certificates/{pdf_name}", "PDF", resolution=100.0)
        os.unlink(img)
        image.close()
        pdf = InputFile(f"certificates/{pdf_name}")
        file = await bot.send_document(591250245, pdf)
        file_id = file.document.file_id
        unique_id = img.split("/")[-1].split(".")[0].split("_")[-1]
        await dc.insert_user_certificate(unique_id, file_id, category, district)
        await bot.delete_message(591250245, file.message_id)


async def pdf_to_zip_file():
    files = os.scandir('certificates/')
    zip_name = "certificates/certificates.zip"
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zip_file:
        for file in files:
            file = f"certificates/{file.name}"
            zip_file.write(file, os.path.basename(file))
            os.unlink(file)




