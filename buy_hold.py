from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Blackly
from strategies.SIP import SIP
# from strategies.BuyBuyBuy import BuyBuyBuy

cerebro = bt.Cerebro()

cerebro.broker.setcash(1e5)
cerebro.broker.setcommission(commission=0.001)

data = bt.feeds.YahooFinanceData(
  dataname='./data/TSLA.csv',
  fromdate=datetime(2010, 7, 1),
  todate=datetime(2020, 1, 1)
)
cerebro.adddata(data)
cerebro.addstrategy(SIP)
# cerebro.addstrategy(BuyBuyBuy)

cerebro.addanalyzer(btanalyzers.PositionsValue, _name='PositionsValue')

print('投資 > 起始資產 %.2f 💲' % cerebro.broker.getvalue())
cerebro.run()
print('投資 > 結束資產 %.2f 💲' % cerebro.broker.getvalue())

b = Bokeh(style='bar', plot_mode='single', scheme=Blackly())
cerebro.plot(b)