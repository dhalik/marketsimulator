__author__ = 'kam'

from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import BBGRequest
import BackTest
from datetime import date
from sklearn.ensemble import RandomForestClassifier
from numpy import asarray

movingPeriod = 10
BUY = "BUY"
SELL = "SELL"
NO = "NO"

class TSPoint:
    def __init__(self, value, date):
        self.date = date
        self.value = value

class Model:

    def __init__(self):
        self.start = date(2009, 1, 1)
        self.end = date(2014, 12, 31)
        self.decisionValue = 0.1

        self.featureList = [] #training features
        self.testList = [] #testing features

        metrics = ["CONCCONF","M2","INJCJC4","VIX","NHCHATCH", "ECGDUS 14","TYX"] #TYX
        self.spy = BBGRequest.BBGRequest("SPY", self.start, self.end).run()

        for inp in metrics:
            data = self.fillMissing(self.spy, self.getValues(inp))
            self.featureList.append(self.getMovingAverage(data))
            self.testList.append(data[-250:])

        #data = self.fillMissing(self.spy,BBGRequest.BBGRequest("CLF5", self.start, self.end, type=" Comdty").run())
        #self.featureList.append(self.getMovingAverage(data))
        #self.testList.append(data[-250:])

        self.testFeatureList = self.transformVector(self.testList)

        self.featureList = self.transformVector(self.featureList)
        self.spyLabels = self.getSpyLabels()

        self.X= self.featureList[:-250]
        self.y= self.spyLabels[:-250]

        self.clf = self.learn()

    def transformVector(self, vec):
        return asarray(vec).T.tolist()

    def getSpyLabels(self):
        self.spyPercent = self.getMovingAverage(self.getPercentReturns(self.spy))
        self.spyLabels = []
        for inp in self.spyPercent:
            if (inp > self.decisionValue):
                self.spyLabels.append(BUY)
            elif (inp < -self.decisionValue/2):
                self.spyLabels.append(SELL)
            else:
                self.spyLabels.append(NO)
        return self.spyLabels

    def getMovingAverage(self, list):
        retVal = []

        for i in xrange(len(list)):
            accum = 0.0
            for j in range(movingPeriod):
                if (i + j < len(list)):
                    accum += list[i+j].close
            retVal.append(float(accum)/float(movingPeriod))
        return retVal

    def getValues(self, name):
        request = BBGRequest.BBGRequest(name, self.start, self.end, type=" Index")
        reqVals = request.run()
        return reqVals

    def learn(self):
        clf = RandomForestClassifier()
        clf.fit(self.X, self.y)

        return clf

    def getPercentReturns(self, spyValues):
        retVal = []
        for i in xrange(len(spyValues)):
            if (i == len(spyValues) - 1):
                retVal.append(BBGRequest.BBGResponse(spyValues[i-1].ticker,0.0, spyValues[i-1].date))
            else:
                retVal.append(BBGRequest.BBGResponse(spyValues[i].ticker,
                                                     (spyValues[i + 1].close / spyValues[i].close - 1) * 100,
                                                        spyValues[i].date))
        return retVal

    def fillMissing(self, marketDays, toInterp):
        retVal = []
        savedLast = toInterp[0]
        for resp in marketDays:
            if (len(toInterp) > 0 and resp.date < toInterp[0].date):
                retVal.append(toInterp[0])
            elif(len(toInterp) > 0):
                if (len(toInterp) == 1):
                    savedLast = toInterp[0]
                retVal.append(toInterp[0])
                toInterp.remove(toInterp[0])
            else:
                retVal.append(savedLast)
        return retVal

    def run(self):
        actions = []
        self.prev = NO
        for x in self.testFeatureList:
            pred = self.clf.predict(map(lambda x: x.close, x))[0]
            if (len(actions) == 0):
                action = BackTest.Action(pred,"SPY",500,x[3].date)
            else:
                action = BackTest.Action(pred,"SPY",1000,x[3].date)
            if (action.type != NO and self.prev != action.type):
                actions.append(action)
                self.prev = pred

        for x in actions:
            print(x)
        bt = BackTest.BackTester(date(2014,1,1), date(2014,12,31), actions)
        bt.run()
        print(bt.portfolio)

def main():
    m = Model()
    #while (True):
    m.learn()
    m.run()

if (__name__ == "__main__"):
    main()
