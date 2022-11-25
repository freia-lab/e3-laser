import json
import requests

class GetEPPStatus:
    debug = 1
    state = None
    baseAddress = None
    output1Open = None
    atten1 = None
    picker1Val = None
    output2Open = None
    atten2 = None
    picker2Val = None

    def __init__(self, eppURL):
        self.baseAddress = eppURL

    def setDebugLvl(self, level):
        self.debug = level

    def put(self, url, data):
        return requests.put(self.baseAddress + url, json =data)
    def post(self, url, data):
        return requests.post(self.baseAddress + url, json =data)
    def get(self, url):
        return requests.get(self.baseAddress + url, timeout=1.50)
    
    def getStatus(self):
        response = self.get('/Channel1/State')
        self.state = response.json()
        if not response.ok:
            return 0
        self.atten1 = round(self.state['AttenuatorValue'])
        if self.state['IsOutputOpen']:
            self.output1Open = 1
        else:
            self.output1Open = 0    
        self.picker1Val = self.state['PulsePickerValue']
        if self.debug > 0:
            if self.debug > 1:
                print (json.dumps(self.state, indent =3))
        response = self.get('/Channel2/State')
        self.state = response.json()
        if not response.ok:
            return 0
        self.atten2 = round(self.state['AttenuatorValue'])
        if self.state['IsOutputOpen']:
            self.output2Open = 1
        else:
            self.output2Open = 0    
        self.picker2Val = self.state['PulsePickerValue']
        if self.debug > 0:
            if self.debug > 1:
                print (json.dumps(self.state, indent =3))
        return 1

