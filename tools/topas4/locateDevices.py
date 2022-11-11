import time
import requests
import sys
import json

from Topas4Locator import Topas4Locator



def main():
#    serialNumber = "00666" #enter serial number or your own device here
#    serialNumber = "P21572" #enter serial number or your own device here
    serialNumber = "EPP21004" #enter serial number or your own device here
    example = GetStatus(serialNumber)
    example.run()


class GetStatus:
    baseAddress = None
    publicREST_API_urls = []
    availableDevices = None

    def __init__(self, serialNumber):
        locator = Topas4Locator()
        self.availableDevices = locator.locate()
        print ('Available devices: ')

    def run(self):
       self.getInfo(self.availableDevices)
       return


    def getInfo(self, devices):
        for item in self.availableDevices:
            print("##### Serial number:\t\t" + item['SerialNumber'])
            print("      WebPageAddress:\t\t" + item['WebPageAddress'])
            print("      PublicApiRestUrl_Version0:\t" + item['PublicApiRestUrl_Version0'])
            self.publicREST_API_urls.append(item['PublicApiRestUrl_Version0'])
            if (item['CallerHasAccessRights']):
                print("      Caller Has Access Rights")
            else:
                print("      Caller Has No Access Rights")
            self.getUserWithAccessRights(item['PublicApiRestUrl_Version0'])


    def getUserWithAccessRights(self, url):
        """Get list of users with access rights"""
        users = requests.get(url + '/Authentication/UsersWithAccessRights').json()
        print("      User with access rights:")
#        print (json.dumps(users, indent =3))
        for item in users:
            ip = item['IPAddress']
            if isinstance(ip, str):
                if isinstance(item['PCName'], str):
                    print("\t\tIP addr: %s\tHostname: %s" %  ip,item['PCName'])
                else:
                    print("\t\tIP addr: %s\tHostname: null" %  ip)
            else:
                print("\t\tIP addr: null\t\tHostname: %s" %  item['PCName'])


if __name__ == "__main__":
    main()



