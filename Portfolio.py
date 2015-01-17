__author__ = 'kam'

from datetime import date

class Portfolio:
    def __init__(self):
        self.stocks = {}
        self.transactions = 0
        self.cash = 0.0

    def addStock(self, date, pos, cost):
        if (self.stocks.__contains__(pos.ticker)):
            self.stocks[pos.ticker] = self.stocks[pos.ticker].combine(pos)
        else:
            self.stocks[pos.ticker] = pos

        if (pos.quantity > 0):
            self.cash += cost * -1
        else:
            self.cash += cost

        self.transactions += 1

    def sellStock(self, date, pos):
        self.addStock(date, Position(pos.ticker, -pos.quantity))

    def __repr__(self):
        retVal = ""
        for value in self.stocks.values():
            retVal += str(value) + "\n"
        retVal += "Total Transactions: " + str(self.transactions) + "\n"
        retVal += "Total Cash: " + str(self.cash)
        return retVal


class Position:

    def __init__(self, ticker, quantity):
        self.quantity = quantity
        self.ticker = ticker

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
