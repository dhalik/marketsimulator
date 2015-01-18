__author__ = 'kam'

from datetime import date
import math

class Portfolio:

    def __init__(self):
        self.stocks = {}
        self.transactions = 0
        self.cash = 0.0
        self.maxCapital = 0.0

    def updateCash(self, trans):
        self.cash += trans
        print(str(trans))
        print(str(self.cash))
        if (math.fabs(self.cash) > math.fabs(self.maxCapital)):
            self.maxCapital = math.fabs(self.cash)

    def addStock(self, date, pos, cost):
        if (self.stocks.__contains__(pos.ticker)):
            self.stocks[pos.ticker] = self.stocks[pos.ticker].combine(pos)
        else:
            self.stocks[pos.ticker] = pos

        self.updateCash(cost * -1)
        self.transactions += 1

    def sellStock(self, date, pos):
        self.addStock(date, Position(pos.ticker, -pos.quantity))

    def __repr__(self):
        retVal = ""
        for value in self.stocks.values():
            retVal += str(value) + "\n"
        retVal += "Total Transactions: " + str(self.transactions) + "\n"
        retVal += "Total Cash: " + str(self.cash) + "\n"
        retVal += "Max Capital: " + str(self.maxCapital)+ "\n"
        retVal += "Return: " + str(self.cash / self.maxCapital)
        return retVal


class Position:

    def __init__(self, ticker, quantity):
        self.quantity = quantity
        self.ticker = ticker
        #add short costs to this at risk free rate
        self.costOfPosition = 10.0

    def combine(self, o):
        return Position(o.ticker, self.quantity + o.quantity)

    def __repr__(self):
        return str(self.quantity) + " X " + str(self.ticker)

def main():
    pf = Portfolio()
    pf.addStock(date(2014, 1, 1), Position("SPY", 100), 18000)
    pf.addStock(date(2014, 1, 1), Position("HYG", 20), 1600)
    print(pf)

if (__name__ == "__main__"):
    main()
