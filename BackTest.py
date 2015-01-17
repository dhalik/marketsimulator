__author__ = 'kam'

from datetime import date, timedelta
import Portfolio
import BBGRequest

BUY = "BUY"
SELL = "SELL"

class BackTester:

    def __init__(self, startDate, endDate, actions):
        self.startDate = startDate
        self.endDate = endDate
        self.portfolio = Portfolio.Portfolio()
        self.actions = actions

    def run(self):
        for act in self.actions:
            print(act)
            bbg = BBGRequest.BBGRequest(act.ticker, act.date, act.date + timedelta(days=1)).run()
            print(bbg)
            #self.portfolio.addStock(act.date, act.execute(), )

class Action:

    def __init__(self, type, ticker, quantity, date):
        self.type = type
        self.ticker = ticker
        self.quantity = quantity
        self.date = date

    def __repr__(self):
        return self.type + " " +self.ticker + " " + str(self.quantity) + " on " + self.date.strftime("%Y-%m-%d")

    def execute(self):
        mult = 1
        if (self.type == SELL):
            mult *= -1
        return Portfolio.Position(self.ticker, mult * self.quantity)

def main():
    actList = [Action(BUY, "IBM", 100, date(2014, 1, 1)),
               Action(SELL, "SPY", 100, date(2014, 1, 1)),
               Action(BUY, "HYG", 100, date(2014, 1, 1))]
    test = BackTester(date(2014, 1, 1), date(2014, 12, 31), actList)
    test.run()
    print(test.portfolio)

if (__name__ == "__main__"):
    main()