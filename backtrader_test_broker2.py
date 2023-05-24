import backtrader as bt
import inspect


class MyStrategy(bt.Strategy):
    params = (('period', 30),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=self.p.period)

    def notify_order(self, order):
        if order.status == bt.Order.Completed:
            if order.isbuy():
                print('买： 价格: %.2f, 交易量: %d 交易费用: %.2f, 佣金 %.2f' %
                      (order.executed.price,
                       order.executed.size,
                       order.executed.value,
                       order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:
                print('卖： 价格: %.2f, 交易量: %.2f, 佣金 %.2f' %
                      (order.executed.price,
                       order.executed.value,
                       order.executed.comm))

                gross_pnl = (order.executed.price - self.buyprice) * self.opsize

                if self.broker.getcommissioninfo(order.data).margin:
                    gross_pnl *= self.broker.getcommissioninfo(order.data).p.mult

                net_pnl = gross_pnl - self.buycomm - order.executed.comm
                print('收益： 毛利 %.2f, 净利 %.2f, 资产价值 %.2f' %
                      (gross_pnl, net_pnl, self.broker.getvalue()))

    def next(self):
        if not self.position:
            if self.sma > self.data.close:
                self.order = self.order_target_percent(target=0.3)
        else:
            if self.sma < self.data.close:
                self.close()


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
cerebro.broker.setcommission(commission=10.0, margin=10000.0, mult=10.0)

cerebro.run()