from zipfile import ZipFile
from requests import get
from io import BytesIO, StringIO
from datetime import datetime
import pandas as pd

FREQUENCIES = ['daily', 'weekly', 'monthly']

def MKT_RF(frequency='weekly', start_date='19260701', end_date=None):
    
    if frequency not in FREQUENCIES:
        raise ValueError('Invalid value for frequency.')

    if not end_date:
        end_date = datetime.now().strftime('%Y%m%d')
    else:
        try:
            datetime.strptime(end_date, "%Y%m%d")
        except:
            raise ValueError('Invalid format for start_date')
        else:
            end_date = datetime.strptime(end_date, "%Y%m%d")

    try:
        start_date = datetime.strptime(start_date, '%Y%m%d')
    except:
        raise ValueError('Invalid format for start_date')

    url = f'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_{frequency}_CSV.zip'
    r = get(url, stream=True)
    with ZipFile(BytesIO(r.content), 'r') as zip:
        data = zip.read(zip.namelist()[0])

    data = data.decode('utf-8')
    df = pd.read_csv(pd.compat.StringIO(data), header=3, index_col=0)
    df = df.query(f'index<\'{end_date}\' & index>\'{start_date}\'')
    MKT_RF = df['Mkt-RF']
    return MKT_RF