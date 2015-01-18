__author__ = 'kam'

import subprocess
import json
from datetime import datetime, date


class BBGRequest:

    def __init__(self, ticker, start, end, type=" US EQUITY"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.type = type

        self.script = './makeReq.sh'
        if (self.type == " US EQUITY"):
            self.script = './getEquity.sh'

        self.command = self.script + ' \"' + self.ticker + self.type + '\" '+ self.start.strftime("%Y%m%d") \
                       +' '+ self.end.strftime("%Y%m%d") +' > temp'
        print(self.command)
    def run(self):
        subprocess.call(self.command,shell=True)
        f = open("temp", "r")
        jsonObject = json.load(f)
        pxArray = jsonObject['data'][0]['securityData']['fieldData']
        retVal = []
        for a in pxArray:
            sampleTime = datetime.strptime(a['date'], "%Y-%m-%dT00:00:00.000Z")
            retVal.append(BBGResponse(self.ticker, a['PX_LAST'], sampleTime))
        return retVal



class BBGResponse:

    def __init__(self, ticker, close, date):
        self.ticker = ticker
        self.close = close
        self.date = date

    def __repr__(self):
        return "BBGResponse[" + self.date.strftime("%Y-%m-%d") + ": " \
               + self.ticker + ": Close=" + str(self.close) + "]"


def main():
    #unitTest
    for r in BBGRequest("SPY", date(2014, 1, 1), date(2014, 12, 31)).run():
        print(r.date.strftime("%Y-%m-%d ") + str(r.close))

if (__name__ == "__main__"):
    main()