import json
import requests

class GetLaserStatus:
    debug = 1
    baseAddress = None
    state = dict()
    basic = None
    shutterOpen = 0
    outputFreq = None
    outputEnergy = None
    outputPwr = None
    atten = None
    harmonic = None
    plsDur = None
    chirpPos = None
    burst = None
    ppDivider = None
    warn = None
    error = None


    def __init__(self, carbideURL):
        self.baseAddress = carbideURL
        self.state = {'Initializing': 1, 'StandingBy': 2, 'Housekeeping': 3, 'Operational': 4, 'GoingToStandby': 5, 'InFieldUpdate': 6, 'Service': 7, 'Failure': 8}

    def setDebugLvl(self, level):
        self.debug = level

    def put(self, url, data):
        return requests.put(self.baseAddress + url, json =data)
    def post(self, url, data):
        return requests.post(self.baseAddress + url, json =data)
    def get(self, url):
        return requests.get(self.baseAddress + url, timeout=1.50)
    
    def getBasic(self):
        """Get Basic data"""
        """        try:
            basic = self.get('/Basic').json()
            print("*** Basic properties ***")
#            print (json.dumps(basic, indent =3))
        except requests.exceptions.ConnectionError as e:
            print(e)
            return 0
        except:
            print("No answer")
            return 0 
        """
        response = self.get('/Basic')
        self.basic = response.json()
        if not response.ok:
            return 0
        self.outputFreq = 1000 * self.basic['ActualOutputFrequency']
        self.outputEnergy = 10 * self.basic['ActualOutputEnergy']
        self.outputPwr = 1000 * self.basic['ActualOutputPower']
        self.atten = self.basic['ActualAttenuatorPercentage']
        self.harmonic = self.basic['ActualHarmonic']
        self.plsDur = self.basic['ActualPulseDuration']
        if self.plsDur > 0:
            self.chirpPos = 1
        else:
            self.chirpPos = 0
            self.plsDur = -self.plsDur
        self.burst = self.basic['ActualBurstPulseCount']
        self.ppDivider = self.basic['ActualPpDivider']
        if  self.basic['Warnings']:
            self.warn = 1
        else:
            self.warn = 0
        if  self.basic['Errors']:
            self.error = 1
        else:
            self.error = 0
        stnam = self.basic['ActualStateName']

        if self.debug > 0:
            print("\tActual state name:\t", stnam, "(%d)" % self.state[stnam])
            print("\tActualOutputEnergy:\t", self.basic['ActualOutputEnergy'])
            print("\tIsOutputEnabled:\t", self.basic['IsOutputEnabled'] == True)
            print("\tActualShutterState:\t", self.basic['ActualShutterState'])
            print("\tActualHarmonic:\t\t", self.basic['ActualHarmonic'])
            print("\tActualOutputFrequency:\t", self.basic['ActualOutputFrequency'])
            print("\tActualOutputPower:\t", self.basic['ActualOutputPower'])
            print("\tActualAttenuatorPercentage:\t", self.basic['ActualAttenuatorPercentage'])
            print("\tActualPulseDuration:\t", self.basic['ActualPulseDuration'])
            print("\tActualBurstPulseCount:\t", self.basic['ActualBurstPulseCount'])
            print("\tIsPowerlockEnabled:\t", self.basic['IsPowerlockEnabled'])
            print("\tActualPpDivider:\t", self.basic['ActualPpDivider'])
            print("\tWarnings:\t\t", self.basic['Warnings'])
            print("\tErrors:\t\t\t", self.basic['Errors'])
            if self.debug > 1:
                print (json.dumps(self.basic, indent =3))
        return 1

    def getLaserState(self):        
        return self.state[self.basic['ActualStateName']]

    def isShutterOpen(self):
        if self.basic['ActualShutterState'] == 'Closed':
            return 0
        else:
            return 1
 
    def isOutputEnabled(self):
        if self.basic['IsOutputEnabled']:
            return 1
        else:
            return 0
 
    def isPwrLockEnabled(self):
        if self.basic['IsPowerlockEnabled']:
            return 1
        else:
            return 0
