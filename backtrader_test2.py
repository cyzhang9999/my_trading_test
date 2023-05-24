import backtrader as bt
class SMACloseSignal(bt.Indicator):
    lines = ('signa',)
    params = (('period', 30),)
    def __init__(self):
        self.lines.signa = self.data - bt.indicators.SMA(period=self.p.period)

class SMAExitSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)
    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2

cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(
    dataname='CU1811.csv',
    nullvalue=0.0,
    dtformat=('%Y%m%d'),
    datetime=1,
    open=4,
    high=5,
    low=6,
    close=7,
    volume=11,
    openinterest=-1
)
cerebro.adddata(data)
cerebro.broker.set_cash(1000000)
cerebro.add_signal(bt.SIGNAL_LONG, SMACloseSignal, period=30)
cerebro.add_signal(bt.SIGNAL_LONGEXIT, SMAExitSignal,p1=5,p2=30)
cerebro.run()
cerebro.plot(style='bar',iplot=False)
