import time
import random
import requests
import sys
import json

from getLaserStatus import GetLaserStatus

def main():
    carbideURL = 'http://10.1.251.2:20010/v1'

    carbide = GetLaserStatus(carbideURL)
    print("\n*** Using URL: "+carbideURL+ " ***")
    while True:
        run(carbide)
        time.sleep(2)

def run(laser):
    if (laser.baseAddress is None):
        return
    laser.setDebugLvl(7)
    if laser.getBasic():
        print("OK")
    else:
        print("Error")
    laser.setDebugLvl(7)
    print("Actual laser state:",laser.getLaserState())
    return


if __name__ == "__main__":
    main()
