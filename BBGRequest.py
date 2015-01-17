__author__ = 'kam'

import subprocess
import json
from datetime import datetime, date


class BBGRequest:

    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.command = './makeReq.sh \"' + self.ticker + ' US EQUITY\" '+ self.start.strftime("%Y%m%d") \
                       +' '+ self.end.strftime("%Y%m%d") +' > temp'

    def getReq(self):
        subprocess.call(self.command,shell=True)
        f = open("temp", "r")
        jsonObject = json.load(f)
        pxArray = jsonObject['data'][0]['securityData']['fieldData']
        retVal = []
        for a in pxArray:
            sampleTime = datetime.strptime(a['date'], "%Y-%m-%dT00:00:00.000Z")
            retVal.append(BBGResponse(self.ticker, a['OPEN'], a['PX_LAST'], sampleTime))
        return retVal



class BBGResponse:

    def __init__(self, ticker, open, close, date):
        self.ticker = ticker
        self.open = open
        self.close = close
        self.date = date

    def __repr__(self):
        return "BBGResponse[" + self.date.strftime("%Y-%m-%d") + ": " \
               + self.ticker + ": Open=" + str(self.open) + ": Close=" + str(self.close) + "]"


def main():
    #unitTest
    print(BBGRequest("SPY", date(2014, 1, 1), date(2014, 1, 15)).getReq())

if (__name__ == "__main__"):
    main()