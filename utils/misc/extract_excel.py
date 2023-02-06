import pandas as pd

from utils.misc.make_certificate import draw_certificate


# Load the Excel file into a Pandas DataFrame
# Шаблон-ДХ.xlsx


async def extract_excel_file(file):
    df = pd.read_excel(f'{file}')
    data = []
    for i in df.values:
        if str(i[1]) != 'nan' and str(i[0]) != 'nan':
            data.append(
                {
                    'name': i[1], 'direction': i[2],
                    'start_date': pd.to_datetime(i[3]).strftime('%Y-%m-%d'),
                    'end_date': pd.to_datetime(i[4]).strftime('%Y-%m-%d')
                }
            )

    print(data)
    await draw_certificate('images/ДХ.png', data)



