import backtrader as bt

class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi =bt.indicators.RSI(self.data,period = 14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        if self.rsi > 90 and self.position:
            self.close()

cerebro = bt.Cerebro()

#data = bt.feeds.GenericCSVData(dataname='daily.csv' , dtformat=2)
data = bt.feeds.GenericCSVData(dataname='coin_Bitcoin.csv', dtformat=('%d-%m-%Y %H:%M'))

cerebro.adddata(data)
cerebro.addstrategy(RSIStrategy)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('=============================================================================================')
print('=============================================================================================')
cerebro.run()
print('=============================================================================================')
print('=============================================================================================')
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#cerebro.plot()


