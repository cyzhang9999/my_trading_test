import backtrader as bt
import inspect


class MyStrategy(bt.Strategy):
    params = (('period', 30),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=self.p.period)

    def notify_order(self, order):

        if order.status == bt.Order.Completed:
            print("\033[31mbar序：{}，{}, 手数：{}, 价格:{}\033[0m"
                  .format(len(self), ' 买 ' * order.isbuy() or ' 卖', order.executed.size, order.executed.price))

    def next(self):
        print("bar序：{}，开盘价：{},收盘价：{},最高价：{},最低价：{}".format(len(self), self.data.open[0], self.data.close[0],
                                                           self.data.high[0], self.data.low[0]))
        if self.sma > self.data.close:
            self.buy()

        elif self.sma < self.data.close:
            self.sell()


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
cerebro.addstrategy(MyStrategy, period=30)

cerebro.broker.set_slippage_perc(0.01)

cerebro.run()
