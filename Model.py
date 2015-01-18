__author__ = 'kam'

import BBGRequest
from datetime import date, datetime

class Model:

    def __init__(self):
        m2Request = BBGRequest.BBGRequest("M2", date(2014, 1, 1), date(2014, 12, 31), type=" Index")
        confRequest = BBGRequest.BBGRequest("CONCCONF", date(2014, 1, 1), date(2014, 12, 31), type=" Index")
        initClaimsRequest = BBGRequest.BBGRequest("INJCJC4", date(2014, 1, 1), date(2014, 12, 31), type=" Index")
        tyxReq = BBGRequest.BBGRequest("TYX", date(2014, 1, 1), date(2014, 12, 31), type=" Index")
        housing = BBGRequest.BBGRequest("NHCHATCH", date(2014, 1, 1), date(2014, 12, 31), type=" Index")

        m2values = m2Request.run()
        confvalues = confRequest.run()
        initValues = initClaimsRequest.run()
        tyxValues = tyxReq.run()
        housingVals = housing.run()


        print(m2values)
        print(confvalues)
        print(initValues)
        print(tyxValues)
        print(housingVals)

def main():
    Model()

if (__name__ == "__main__"):
    main()