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
            resp = BBGRequest.BBGRequest(act.ticker, act.date, act.date + timedelta(days=1)).run()
            if (len(resp) == 0):
                raise Exception("No Data")

            self.portfolio.addStock(act.date, act.execute(), resp[0].close * act.quantity)
            print(str(act) + str(resp[0]))
        self.liquidate()

    def liquidate(self):
        for sec in self.portfolio.stocks.values():
            resp = BBGRequest.BBGRequest(sec.ticker, self.endDate, self.endDate + timedelta(days=1)).run()
            if (len(resp) == 0):
                raise Exception("No Data")
            pos = Portfolio.Position(sec.ticker, -sec.quantity)
            self.portfolio.addStock(self.endDate, pos, resp[0].close * pos.quantity)
            print(str(pos) + str(resp[0]))



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
    actList = [Action(BUY, "SPY", 100, date(2014, 1, 1)),
               Action(BUY, "HYG", 100, date(2014, 1, 1))]
    test = BackTester(date(2014, 1, 1), date(2014, 12, 31), actList)
    test.run()
    print(test.portfolio)

if (__name__ == "__main__"):
    main()