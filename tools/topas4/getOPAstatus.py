import time
import random
import requests
import sys
import json

def main():
    url = "http://10.1.11.11:8004/P21572/v0/PublicAPI"
    opaStatus = GetOPAStatus(url)
    opaStatus.run()


class GetOPAStatus:
    baseAddress = None
    debug = 1

    """ Shutter and interlocks """
    shutterOpen = 0
    shutterOpenIgnored = 0
    shutterForceClosed = 0
    interlockOpen = 0
    conn2laserOK = 0
    ctrlByLaser = 0
    ctrlConfiguration = 0
    laserOutputSynched = 0

    """ Optical system """
    wavelength = 0.0

    def __init__(self, baseAddress):
        if self.debug > 0:
            print("Connecting to", baseAddress)
        self.baseAddress = baseAddress

    def run(self):
       if (self.baseAddress is None):
           return
       self.getUserWithAccessRights()
       self.getCalibrationInfo()
       self.getShutterState()
       self.getWavelengthSetterStatus()
       self.getOpticalSystemStatus()
       time.sleep(0.2)
       return


    def put(self, url, data):
        return requests.put(self.baseAddress + url, json =data)
    def post(self, url, data):
        return requests.post(self.baseAddress + url, json =data)
    def get(self, url):
        return requests.get(self.baseAddress + url, timeout=1.50)
    

    def getUserWithAccessRights(self):
        """Get list of users with access rights"""
        users = self.get('/Authentication/UsersWithAccessRights').json()
        if self.debug > 3:
            print("User with access rights:")
            if self.debug > 5:
                print (json.dumps(users, indent =3))
            for item in users:
                ip = item['IPAddress']
                if isinstance(ip, str):
                    if isinstance(item['PCName'], str):
                        print("IP addr: %s\tHostname: %s" %  ip,item['PCName'])
                    else:
                        print("IP addr: %s\tHostname: null" %  ip)
                else:
                    print("IP addr: null\t\tHostname: %s" %  item['PCName'])


    def getCalibrationInfo(self):
        """Get basic calibration info and set random wavelength using random interaction"""
        interactions = self.get('/Optical/WavelengthControl/ExpandedInteractions').json()
        if self.debug > 3:
            print("Available interactions:")
            for item in interactions:
               print("\t"+item['Type'] + " %d - %d nm" % (item['OutputRange']['From'], item['OutputRange']['To']))
            if len(interactions) <= 0:
                print("\tThere are no calibrated interactions")

    def getShutterState(self):
        """Get status of shutter and interlocks"""
        state = self.get('/ShutterInterlock/State').json()
        if self.debug > 1:
            print("Interlock and shutter state:")
        if self.debug > 5:
            print (state)
        if (state['IsInterlockOpen']):
            self.interlockOpen = 1
            print ("\tInterlock Open")
        else:
            self.interlockOpen = 0
            print ("\tInterlock Closed")
        if (state['IsShutterOpen']):
            self.shutterOpen = 1
            print ("\tShutter Open")
        else:
            self.shutterOpen = 0
            print ("\tShutter Closed")
        if (state['IsShutterOpenIgnoringTemporarily']):
            self.shutterOpenIgnored = 1
            print ("\tShutter Open temporarily Ignored")
        else:
            self.shutterOpenIgnored = 0
        if (state['IsShutterTemporarilyClosedDueSafetyReasons']):
            self.shutterForceClosed = 1
            print ("\tShutter temporarily Closed due to safety reasons")
        else:
            self.shutterForceClosed = 0

        for item in state['Shutters']:
            if self.debug > 5:
                print (item)
            if (not item['IsHidden']):
                if self.debug > 2:
                    if (state['IsShutterOpen']):
                        print ("\tShutter "+ item['Name']+" Open")
                    else:
                        print ("\tShutter \""+ item['Name']+"\" Closed")

        """Get status of shutter control by laser output control (i.e. pulse picker)"""
        state = self.get('/ShutterInterlock/OutputControlWithLaserState').json()
        if self.debug > 1:
            print("Shutter control by laser output control (pulse picker):")
        if self.debug > 5:
            print (state)
        if (state['IsConnectionToLaserOk']):
            self.conn2laserOK = 1
            print ("\tConnection to laser OK")
        else:
            self.conn2laserOK = 0
            print ("\tConnection to laser ERROR")
        if (state['IsControlByLaserEnabled']):
            self.ctrlByLaser = 1
            print ("\tControl by laser ENABLED")
        else:
            self.ctrlByLaser = 0
            print ("\tControl by laser DISABLED")
        if (state['IsLaseControlConfiguredOk']):
            self.ctrlConfiguration = 1
            print ("\tControl configuration OK")
        else:
            self.ctrlConfiguration = 0
            print ("\tControl configuration ERROR")
        if (state['IsLaserOutputSynced']):
            self.laserOutputSynched = 1
            print ("\tLaser output SYNCED")
        else:
            self.laserOutputSynched = 0
            print ("\tLaser output NOT SYNCED")
        return 1

    def getWavelengthSetterStatus(self):
        """Get status of the smooth wavelenght setter status"""
        state = self.get('/SmoothWavelengthSetter/Status').json()
        if self.debug > 1:
            print("Smooth wavelenght setter status:")
        if self.debug > 5:
            print (state)
        if (state['IsRunning']):
            print ("\tRunning")
        else:
            print ("\tIdle")
        if (state['IsStopScheduled']):
            print ("\tStop scheduled")
        print("\tRate: %d [nm/s]" % state['NanometersPerSecondIncludingStartStop'])
        print("\tRepeats left: %d" % state['RepeatsLeft'])
        return 1

    def getOpticalSystemStatus(self):
        """Get status of the optical system"""
        state = self.get('/Optical/WavelengthControl/Output/Wavelength').json()
        if self.debug > 1:
            print("Optical system status:")
        if self.debug > 5:
            print (state)
        print("\tWavelength: %f nm" % state)
        state = self.get('/Optical/WavelengthControl/Output/Interaction').json()
        print("\tIntercation: "+state)
        state = self.get('/Optical/WavelengthControl/Output').json()
        if self.debug > 5:
            print("*** Wavelength control ***")
            print (json.dumps(state, indent =3))
        state = self.get('/Optical/WavelengthControl/ExpandedInteractions').json()
        if self.debug > 5:
            print("*** Expanded interactions ***")
            print (json.dumps(state, indent =3))
        state = self.get('/Optical/WavelengthControl/OpticalSystemData').json()
        if self.debug > 5:
            print("*** Optical system data ***")
            print (json.dumps(state, indent =3))
        return 1



if __name__ == "__main__":
    main()



