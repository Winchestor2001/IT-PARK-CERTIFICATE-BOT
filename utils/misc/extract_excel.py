import os

import pandas as pd

from utils.misc.make_certificate import draw_certificate, pdf_to_zip_file, draw_certificate2


# Load the Excel file into a Pandas DataFrame
# Шаблон-ДХ.xlsx


async def extract_excel_file(file):
    excel_file = pd.ExcelFile(f'{file}')
    df = pd.read_excel(excel_file)
    for n, i in enumerate(df.values, start=1):
        if str(i[1]) != 'nan' and str(i[0]) != 'nan':
            if i[2] in ['Kampyuter s.', 'Android', 'Backend', 'Frontend', 'Graphic design', 'Robotics']:
                data = {
                    'name': i[1], 'direction': i[2],
                    'end_date': pd.to_datetime(i[3]).strftime('%d.%m.%Y'),
                    'district': i[5],
                }
            else:
                data = {
                    'name': i[1], 'direction': i[2],
                    'start_date': pd.to_datetime(i[3]).strftime('%d.%m.%Y'),
                    'end_date': pd.to_datetime(i[4]).strftime('%d.%m.%Y'),
                    'total_hour': i[5], 'district': i[7],
                }

            if i[2] == 'Davlat xodimi':
                await draw_certificate(f'images/ДХ.png', data)
            elif i[2] == 'SSV':
                await draw_certificate(f'images/ССВ.png', data)
            elif i[2] == 'Kampyuter s.':
                await draw_certificate2(f'images/Оддий - KS.png', data)
            elif i[2] == 'Android':
                await draw_certificate2(f'images/Оддий - Android.png', data)
            elif i[2] == 'Backend':
                await draw_certificate2(f'images/Оддий - Back.png', data)
            elif i[2] == 'Frontend':
                await draw_certificate2(f'images/Оддий - Front.png', data)
            elif i[2] == 'Graphic design':
                await draw_certificate2(f'images/Оддий - Graphic.png', data)
            elif i[2] == 'Robotics':
                await draw_certificate2(f'images/Оддий - Robot.png', data)
    excel_file.close()
    os.unlink(file)
    await pdf_to_zip_file()
