

import time
import random
import requests
import sys
import json

def main():
    carbideURL = 'http://10.1.251.2:20010/v1'

    carbide = GetStatus(carbideURL)
    print("\n*** Using URL: "+carbideURL+ " ***")
    carbide.run()


class GetStatus:
    baseAddress = None
    state = dict()

    def __init__(self, carbideURL):
        self.baseAddress = carbideURL
        self.state = {'Initializing': 1, 'StandingBy': 2, 'Housekeeping': 3, 'Operational': 4, 'GoingToStandby': 5, 'InFieldUpdate': 6, 'Service': 7, 'Failure': 8}

    def run(self):
       if (self.baseAddress is None):
           return
       if self.getBasic():
           print("OK")
       else:
           print("Error")
       return
       self.getCalibrationInfo()
       self.getShutterState()
       self.getWavelengthSetterStatus()
       self.getOpticalSystemStatus()
       time.sleep(0.2)
       return
       self.changeShutter()
       availableMotors = self.get('/Motors/AllProperties').json()['Motors']
       if(len(availableMotors) > 0):
          self.tweakMotorPositions(availableMotors[0])


    def put(self, url, data):
        return requests.put(self.baseAddress + url, json =data)
    def post(self, url, data):
        return requests.post(self.baseAddress + url, json =data)
    def get(self, url):
        return requests.get(self.baseAddress + url)
    
    def getBasic(self):
        """Get Basic data"""
        try:
            basic = self.get('/Basic').json()
            print("*** Basic properties ***")
#            print (json.dumps(basic, indent =3))
        except requests.exceptions.ConnectionError as e:
            print(e)
            return False
        except:
            print("No answer")
            return False

        stnam = basic['ActualStateName']
        print("\tActual state name:\t", stnam, "(%d)" % self.state[stnam])
        print("\tActualOutputEnergy:\t", basic['ActualOutputEnergy'])
        print("\tIsOutputEnabled:\t", basic['IsOutputEnabled'] == True)
        print("\tActualShutterState:\t", basic['ActualShutterState'])
        print("\tActualHarmonic:\t\t", basic['ActualHarmonic'])
        print("\tActualOutputFrequency:\t", basic['ActualOutputFrequency'])
        print("\tActualOutputPower:\t", basic['ActualOutputPower'])
        print("\tActualAttenuatorPercentage:\t", basic['ActualAttenuatorPercentage'])
        print("\tActualPulseDuration:\t", basic['ActualPulseDuration'])
        print("\tActualBurstPulseCount:\t", basic['ActualBurstPulseCount'])
        print("\tIsPowerlockEnabled:\t", basic['IsPowerlockEnabled'])
#        print("\t:\t", basic[''])
        return True

    def getUserWithAccessRights(self):
        """Get list of users with access rights"""
        users = self.get('/Authentication/UsersWithAccessRights').json()
        print("User with access rights:")
#        print (json.dumps(users, indent =3))
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
        print("Available interactions:")
        for item in interactions:
           print("\t"+item['Type'] + " %d - %d nm" % (item['OutputRange']['From'], item['OutputRange']['To']))
        if len(interactions) <= 0:
            print("\tThere are no calibrated interactions")

    def getShutterState(self):
        """Get status of shutter and interlocks"""
        state = self.get('/ShutterInterlock/State').json()
        print("Interlock and shutter state:")
#        print (state)
        if (state['IsInterlockOpen']):
            print ("\tInterlock Open")
        else:
            print ("\tInterlock Closed")
        if (state['IsShutterOpen']):
            print ("\tShutter Open")
        else:
            print ("\tShutter Closed")
        if (state['IsShutterOpenIgnoringTemporarily']):
            print ("\tShutter Open temporarily Ignored")
        if (state['IsShutterTemporarilyClosedDueSafetyReasons']):
            print ("\tShutter temporarily Closed due to safety reasons")

        for item in state['Shutters']:
#            print (item)
            if (not item['IsHidden']):
#                print(item)
                if (state['IsShutterOpen']):
                    print ("\tShutter "+ item['Name']+" Open")
                else:
                    print ("\tShutter \""+ item['Name']+"\" Closed")

        """Get status of shutter control by laser output control (i.e. pulse picker)"""
        state = self.get('/ShutterInterlock/OutputControlWithLaserState').json()
        print("Shutter control by laser output control (pulse picker):")
#        print (state)
        if (state['IsConnectionToLaserOk']):
            print ("\tConnection to laser OK")
        else:
            print ("\tConnection to laser ERROR")
        if (state['IsControlByLaserEnabled']):
            print ("\tControl by laser ENABLED")
        else:
            print ("\tControl by laser DISABLED")
        if (state['IsLaseControlConfiguredOk']):
            print ("\tControl configuration OK")
        else:
            print ("\tControl configuration ERROR")
        if (state['IsLaserOutputSynced']):
            print ("\tLaser output SYNCED")
        else:
            print ("\tLaser output NOT SYNCED")

    def getWavelengthSetterStatus(self):
        """Get status of the smooth wavelenght setter status"""
        state = self.get('/SmoothWavelengthSetter/Status').json()
        print("Smooth wavelenght setter status:")
#        print (state)
        if (state['IsRunning']):
            print ("\tRunning")
        else:
            print ("\tIdle")
        if (state['IsStopScheduled']):
            print ("\tStop scheduled")
        print("\tRate: %d [nm/s]" % state['NanometersPerSecondIncludingStartStop'])
        print("\tRepeats left: %d" % state['RepeatsLeft'])

    def getOpticalSystemStatus(self):
        """Get status of the optical system"""
        state = self.get('/Optical/WavelengthControl/Output/Wavelength').json()
        print("Optical system status:")
#        print (state)
        print("\tWavelength: %f nm" % state)
        state = self.get('/Optical/WavelengthControl/Output/Interaction').json()
        print("\tIntercation: "+state)
        state = self.get('/Optical/WavelengthControl/Output').json()
        print("*** Wavelength control ***")
        print (json.dumps(state, indent =3))
        state = self.get('/Optical/WavelengthControl/ExpandedInteractions').json()
        print("*** Expanded interactions ***")
        print (json.dumps(state, indent =3))
        state = self.get('/Optical/WavelengthControl/OpticalSystemData').json()
        print("*** Optical system data ***")
        print (json.dumps(state, indent =3))


    def getCalibrationInfoAndSetWavelength(self):
        """Get basic calibration info and set random wavelength using random interaction"""
        interactions = self.get('/Optical/WavelengthControl/ExpandedInteractions').json()
        print("Available interactions:")
        for item in interactions:
           print(item['Type'] + " %d - %d nm" % (item['OutputRange']['From'], item['OutputRange']['To']))
        if len(interactions) > 0:
          interaction = interactions[random.randint(0,len(interactions) - 1)] #set wavelength using random interaction
          #wavelength is selected randomly too, to be in valid range for that
                                                                                       #interaction
          wavelengthToSet = interaction['OutputRange']['From'] + (interaction['OutputRange']['To'] - interaction['OutputRange']['From']) * random.uniform(0,1)
          print("setting wavelength %.4f nm using interaction %s" % (wavelengthToSet, interaction['Type']))
          response = self.put('/Optical/WavelengthControl/SetWavelength', { 'Interaction':interaction['Type'], 'Wavelength':wavelengthToSet })
          #if I don't care about interaction used:
          #response =self.put('/Optical/WavelengthControl/SetWavelengthUsingAnyInteraction',wavelengthToSet)
          self.waitTillWavelengthIsSet()
        else:
            print("There are no calibrated interactions")

    def changeShutter(self):
        isShutterOpen = self.get('/ShutterInterlock/IsShutterOpen').json()
        line = input(r"Do you want to " + ("close" if isShutterOpen  else "open") + r" shutter? (Y\N)").upper()
        if line == "Y" or line == "YES":
           self.put('/ShutterInterlock/OpenCloseShutter', not isShutterOpen)
 

   
    def waitTillWavelengthIsSet(self):
       """
       Waits till wavelength setting is finished.  If user needs to do any manual
       operations (e.g.  change wavelength separator), inform him/her and wait for confirmation.
       """
       while(True):
        s = self.get('/Optical/WavelengthControl/Output').json()
        sys.stdout.write("\r %d %% done" % (s['WavelengthSettingCompletionPart'] * 100.0))
        if s['IsWavelengthSettingInProgress'] == False or s['IsWaitingForUserAction']:
            break
       state = self.get('/Optical/WavelengthControl/Output').json()
       if state['IsWaitingForUserAction']:
          print("\nUser actions required. Press enter key to confirm.")
          #inform user what needs to be done
          for item in state['Messages']:
             print(item['Text'] + ' ' + ('' if item['Image'] is None else ', image name: ' + item['Image']))
          sys.stdin.read(1)#wait for user confirmation
          # tell the device that required actions have been performed.  If shutter was open before setting wavelength it will be opened again
          self.put('/Optical/WavelengthControl/FinishWavelengthSettingAfterUserActions', {'RestoreShutter':True})
       print("Done setting wavelength")


    def tweakMotorPositions(self, motor):
        """Shows how to move single motor to desired position and read current position"""
        print(r"Press Up/Down arrow keys to move motor " + motor['Title'] + ". Press Escape to finish motor position tweaking.")
        motorIndex = motor['Index']
        while (True):
             key = ord(msvcrt.getch())
             if key == 27: #ESC
                return
             elif key == 224: #Special keys
                key = ord(msvcrt.getch())
                if key == 72: #Up arrow
                    current = self.get('/Motors/TargetPosition?id=%i' % motorIndex).json()
                    self.put('/Motors/TargetPosition?id=%i' % motorIndex, current + 8)
                    #steps, if you want to use units use TargetPositionInUnits
                elif key == 80: #Down arrow
                    self.put('/Motors/TargetPositionRelative?id=%i' % motorIndex, -8)
                    #equivalent functionality to UpArrow
                else:
                    print("Invalid key. Use Escape to stop motor position adjustment, Up and Down arrows to move motor.")
             else:
                print("Invalid key. Use Escape to stop motor position adjustment, Up and Down arrows to move motor.")





if __name__ == "__main__":
    main()
