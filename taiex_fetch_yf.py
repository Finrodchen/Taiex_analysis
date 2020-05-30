import yfinance as yf
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime

yf.pdr_override()

target_stock = '2884.TW'  #股票代號變數

start_date = datetime(2010, 1, 1)
end_date = datetime(2019, 12, 31)

df = web.get_data_yahoo([target_stock], start_date, end_date)

filename = f'./data/{target_stock}.csv'

df.to_csv(filename)