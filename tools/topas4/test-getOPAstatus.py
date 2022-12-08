import time
import random
import requests
import sys
import json

from getOPAstatus import GetOPAStatus

def main():
    url = "http://10.1.11.11:8004/P21572/v0/PublicAPI"
    opaStatus = GetOPAStatus(url)
    opaStatus.debug = 6
    run(opaStatus)

def run(opa):
   if (opa.baseAddress is None):
       return
   opa.getUserWithAccessRights()
   opa.getCalibrationInfo()
   print("*********** Shutters ************")
   opa.getShutterState()
   opa.getWavelengthSetterStatus()
   opa.getOpticalSystemStatus()
   time.sleep(0.2)
   return

if __name__ == "__main__":
    main()



