__author__ = 'kam'

import subprocess
import json
from datetime import date


class BBGRequest:

    def __init__(self, req, start, end):
        self.req = req
        self.start = start
        self.end = end
        self.command = './test.sh \"' + self.req + ' US EQUITY\" '+ self.start.strftime("%Y%m%d") +' '+ self.end.strftime("%Y%m%d") +' > temp'

    def getReq(self):
        subprocess.call(self.command,shell=True)
        f = open("temp", "r")
        jsonObject = json.load(f)
        pxArray = jsonObject['data'][0]['securityData']['fieldData']
        retVal = []
        for a in pxArray:




class BBGResponse:

    def __init__(self, ticker, open, close, date):
        self.ticker = ticker
        self.open = open
        self.close = close
        self.date = date



def main():
    a = BBGRequest("IBM", date(2014, 1, 1), date(2014, 1, 10))
    print(a.getReq())

if __name__ == "__main__":
    main()