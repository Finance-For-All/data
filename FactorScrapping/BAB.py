from requests import get
import os
from datetime import datetime
import pandas as pd

FREQUENCIES = ['daily', 'monthly']
COUNTRIES = ['AUS', 'AUT', 'BEL', 'CAN', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 
    'FRA', 'GBR', 'HKG', 'IRL', 'ISR', 'ITA', 'JPN', 'NLD', 'NOR', 
    'NZL', 'PRT', 'SWE', 'USA', 'Global', 'Global Ex USA', 'Europe', 'North America', 'Pacific']

def BAB(frequency='daily', securities=['USA'], start_date='19260701', end_date=None):
    if frequency not in FREQUENCIES:
        raise ValueError('Invalid value for frequency.')

    if type(securities) is not list:
        raise TypeError('Invalid type for securities')
    for country in securities:
        if country not in COUNTRIES:
            raise ValueError('Invalid value for security')

    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    else:
        try:
            datetime.strptime(end_date, "%Y%m%d")
        except:
            raise ValueError('Invalid format for start_date')

    try:
        start_date = datetime.strptime(start_date, '%Y%m%d')
    except:
        raise ValueError('Invalid format for start_date')
    
    frequency = frequency.capitalize()
    url = f'https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Betting-Against-Beta-Equity-Factors-{frequency}.xlsx'
    r = get(url)

    with open('temp.xlsx', 'wb') as file:
        file.write(r.content)

    df = pd.read_excel('temp.xlsx', header=18)
    os.remove('temp.xlsx')

    df.DATE = df.DATE.apply(_convert_index)
    df = df.set_index('DATE')

    df = df.query(f'index<\'{end_date}\' & index>\'{start_date}\'')
    df = df[securities]
    return df

def _convert_index(date):
    date = date.split('/')
    return f'{date[2]}{date[0]}{date[1]}'
