from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Blackly

class BuyBuyBuy(bt.Strategy):
  def log(self, txt, dt=None):
    ''' 買買買 策略 '''
    dt = dt or self.datas[0].datetime.date(0)
    print(f'{dt.isoformat()}, {txt}')

  def __init__(self):
    # 鎖定"收盤價"在 datas[0] 的收盤價
    self.dataclose = self.datas[0].close
    self.order = None

  def notify_order(self, order):
    if order.status in [order.Submitted, order.Accepted]:
      return 
    if order.status in [order.Completed]:
      if order.isbuy():
        self.log(f'已購買於 {order.executed.price}')
      elif order.issell():
        self.log(f'已賣出於 {order.executed.price}')

      self.bar_executed = len(self)

    self.order = None

  def next(self):
    self.log(f'收盤價, {self.dataclose[0]}')
    
    # 假設沒有倉位(股票資產)
    if not self.position:
      # 今日收盤價 < 昨日收盤價
      if self.dataclose[0] < self.dataclose[-1]:
        
        # 昨日收盤價 < 前日收盤價
        if self.dataclose[-1] < self.dataclose[-2]:
          self.log(f'購買信號, {self.dataclose[0]}')
          self.order = self.buy()
    
    else:
      if len(self) >= (self.bar_executed + 5):
        self.log(f'賣出信號 {self.dataclose[0]}')
        self.order = self.sell()

target_stock = '4142'

cerebro = bt.Cerebro()

cerebro.broker.setcash(1e5)
cerebro.broker.setcommission(commission=0.001)

data = bt.feeds.GenericCSVData(
  dataname=f'./data/{target_stock}.csv',
  fromedate=datetime(2020, 1, 1),
  todate=datetime(2020, 5, 1),
  nullvalue=0.0,
  dtformat=('%Y-%m-%d'),
  datetime=1,
  high=5,
  low=6,
  open=4,
  close=7,
  volume=3,
  )

cerebro.adddata(data)
cerebro.addstrategy(BuyBuyBuy)
# cerebro.addstrategy(BuyBuyBuy)

cerebro.addanalyzer(btanalyzers.PositionsValue, _name='PositionsValue')

print('投資 > 起始資產 %.2f 💲' % cerebro.broker.getvalue())
cerebro.run()
print('投資 > 結束資產 %.2f 💲' % cerebro.broker.getvalue())

investment_plot = Bokeh(style='bar', plot_mode='single', scheme=Blackly())
cerebro.plot(investment_plot)