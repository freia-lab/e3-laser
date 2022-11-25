import time
import random
import requests
import sys
import json

from getEPPstatus import GetEPPStatus

def main():
    eppURL = 'http://10.1.11.11:14001/CarbideSI/ExternalPP'

    epp = GetEPPStatus(eppURL)
    print("\n*** Using URL: "+eppURL+ " ***")
    while True:
        run(epp)
        time.sleep(2)

def run(epp):
    if (epp.baseAddress is None):
        return
    epp.setDebugLvl(2)
    try:
        if epp.getStatus():
            print("Attenuation chan 1: %f" % epp.atten1)
            print("Attenuation chan 2: %010.3g" % epp.atten2)
            print("Output 1 open:", epp.output1Open)
            print("Output 2 open:", epp.output2Open)
            print("Pulse picker chan 1 value:", epp.picker1Val)
            print("Pulse picker chan 2 value:", epp.picker2Val)
        else:
            print("Error")
    except:
        print("No answer")
        return 0 
    return


if __name__ == "__main__":
    main()
