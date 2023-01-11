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
    epp.setDebugLvl(0)
    if epp.getStatus():
        print("\n**** EPP Status ****")
        print("Attenuation chan 1: %f" % epp.atten1)
        print("Attenuation chan 2: %010.3g" % epp.atten2)
        print("Output 1 open:", epp.output1Open)
        print("Output 2 open:", epp.output2Open)
        print("Pulse picker chan 1 value:", epp.picker1Val)
        print("Pulse picker chan 2 value:", epp.picker2Val)
        print("Laser outputs:", epp.getOutputs())
    else:
        print("Error in getStatus()")
    if epp.getOutputs():
        print("*** Outputs (1 - open, 0 - closed):")
        print("mainLaser:\t\t", epp.mainLaserOutput)
        print("uncompressed:\t\t", epp.uncompressedOutput)
        print("automatedOsc:\t\t", epp.automatedOscOutput)
        print("simultaneousOcs:\t", epp.simultaneousOcsOutput)
        print("uncompressedAfterPP:\t", epp.uncompressedAfterPPoutput)
        print("EPPoutput1:\t\t", epp.EPPoutput1)
        print("EPPoutput2:\t\t", epp.EPPoutput2)
    else:
        print("Error in getOutputs()")
    return


if __name__ == "__main__":
    main()
