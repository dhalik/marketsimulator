__author__ = 'kam'

import BBGRequest
from datetime import date

class Model:

    def __init__(self):
        metrics = ["M2","CONCCONF","INJCJC4","TYX","NHCHATCH"]
        for inp in metrics:
            self.getValues(inp)

    def getValues(self, type):
        request = BBGRequest.BBGRequest(type, date(2014, 1, 1), date(2014, 12, 31), type=" Index")
        reqVals = request.run()
        print(reqVals)

def main():
    Model()

if (__name__ == "__main__"):
    main()