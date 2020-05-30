from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Blackly

class Buy_and_Hold(bt.Strategy):
  def log(self, txt, dt=None):
    '''Buy and Hold'''
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
          self.order = self.buy(size=1000)
    
    else:
      if len(self) >= (self.bar_executed + 5):
        self.log(f'賣出信號 {self.dataclose[0]}')
        self.order = self.sell(size=1000)

target_stock = '0056.TW'

cerebro = bt.Cerebro()

cerebro.broker.setcash(1e6)
cerebro.broker.setcommission(commission=0.0025)

data = bt.feeds.GenericCSVData(
  dataname=f'./data/{target_stock}.csv',
  nullvalue=0.0,
  dtformat=('%Y-%m-%d'),
  datetime=0,
  open=1,
  high=2,
  low=3,
  close=4,
  volume=6,
  )

cerebro.adddata(data)
cerebro.addstrategy(Buy_and_Hold)

cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer') # 交易分析 (策略勝率)
cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='PeriodStats') # 交易基本統計分析
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown') # 回落統計
cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN') # 期望獲利/標準差 System Quality Number
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio') # 夏普指數 

print('投資 > 起始資產 %.2f 💲' % cerebro.broker.getvalue())
cerebro.run()
print('投資 > 結束資產 %.2f 💲' % cerebro.broker.getvalue())

investment_plot = Bokeh(style='bar', plot_mode='single', scheme=Blackly())
cerebro.plot(investment_plot)