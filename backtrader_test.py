from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

class SmaCross(bt.SignalStrategy):
    def __init(self):
        sma1,sma2 = bt.ind.SMA(period=10),bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1,sma2)
        self.singl_add(bt.SINGAL_LONG,crossover)


class TestStrategy(bt.SignalStrategy):
    def __init__(self):
        pass

    def next(self):
        print("已经处理了%d个数据, 总共有%d个数据" % (len(self), self.data.buflen()))

cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)

data = btfeeds.GenericCSVData(
    dataname = "history_k_data.csv",
    fromdate = datetime(2017,6,1),
    todate = datetime(2017,12,29),
    nullvalue=0.0,
    dtformat = ('%Y-%m-%d'),
    datetime =0,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    openinterest=-1
)

cerebro.adddata(data)
cerebro.run()
#cerebro.plot(iplot=False)