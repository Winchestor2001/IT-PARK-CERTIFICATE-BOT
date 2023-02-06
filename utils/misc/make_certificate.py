from PIL import Image, ImageDraw, ImageFont


async def draw_certificate(image, data):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 100)
    draw.text((1500, 1000), str(data[0]['name']).upper(), fill='black', font=font)
    img.save("certificates/text_on_image.jpg")
