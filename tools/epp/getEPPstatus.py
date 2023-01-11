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

    mainLaserOutput = None
    simultaneousOcsOutput = None
    automatedOscOutput = None
    uncompressedAfterPPoutput = None
    uncompressedOutput = None
    EPPoutput1 = None
    EPPoutput2 = None
    outputs = [None]*7
    logicDict = dict()
    
    def __init__(self, eppURL):
        self.baseAddress = eppURL
        self.logicDict = {False: 0, True: 1}

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

    def getOutputs(self):
        response = self.get('/../Outputs/Status')
        data = response.json()
        if not response.ok:
            return 0
        if self.debug > 1:
            print (json.dumps(data, indent =3))
        for item in data:
            self.outputs[item['OutputIndex']] = self.logicDict[item['IsOutputOpen']]
            if self.debug > 0:
                print("AttenuatorValue: %f" % item['AttenuatorValue'])
                print("IsOutputOpen:", item['IsOutputOpen'])
                print("OutputIndex:", item['OutputIndex'])
                print("Title:", item['Title'])
        self.mainLaserOutput = self.outputs[0]
        self.uncompressedOutput = self.outputs[1]
        self.automatedOscOutput = self.outputs[2]
        self.simultaneousOcsOutput = self.outputs[3]
        self.uncompressedAfterPPoutput = self.outputs[4]
        self.EPPoutput1 = self.outputs[5]
        self.EPPoutput2 = self.outputs[6]
        if self.debug > 0:
            print("Outputs:", self.outputs)
        return 1

