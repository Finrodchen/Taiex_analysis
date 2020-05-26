import pandas
import mplfinance as mpf
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

stock_sid = '0050'

history = pandas.read_csv(
    f'./data/{stock_sid}.csv', parse_dates=True, index_col=1)

mpf.plot(
    history,
    type="candle",
    mav=(5, 10),
    style='charles',
    title=stock_sid,
    ylabel="OHLC",
)
