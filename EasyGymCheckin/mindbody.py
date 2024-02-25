import http.client
import json
import traceback
from django.utils.timezone import make_aware
from pprint import pprint
from .models import gymClient, gymClass

class MindBody:
    def __init__(self):
        self.conn = None
        self.staffUserName = None
        self.staffPassword = None
        self.siteId = None
        self.apiKey = None
        self.HEADERS = None
        self.authenticated = False

    def authenticate(self, Username, Password, apiKey, siteId):
        # https://developers.mindbodyonl sine.com/ui/documentation/public-api#/python/mindbody-public-api-v6-0/authentication/user-tokens
        self.staffUserName = Username
        self.staffUserName = Password
        self.ApiKey = apiKey
        payload = {
            'Username': Username,
            'Password': Password,
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Api-Key': f'{apiKey}',
            'SiteId': f'{siteId}',
        }

        self.conn = http.client.HTTPSConnection("api.mindbodyonline.com")
        self.conn.request("POST", "/public/v6/usertoken/issue", json.dumps(payload), self.headers)
        res = self.conn.getresponse()

        data = json.loads(res.read())
        token = data.get("AccessToken")

        self.headers['Authorization'] = token
        self.authenticated = True

    def getClients(self):
        self.conn.request("GET", "/public/v6/client/clients", headers=self.headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        return data['Clients']

    def getClasses(self):
        self.conn.request("GET", "/public/v6/class/classes", headers=self.headers)
        res = self.conn.getresponse()
        classes = json.loads(res.read())['Classes']
        return classes

    def addClientToClass(self, clientid, classid):
        # https://developers.mindbodyonline.com/ui/documentation/public-api#/python/tutorials/book-a-client-into-a-class
        payload = {
            'ClientId': f'{clientid}',
            'ClassId': int(classid),
        }

        self.conn.request("POST", "/public/v6/class/addclienttoclass", json.dumps(payload), headers=self.headers)
        res = self.conn.getresponse()
        pprint(res.read())
        return res


def loadClasses(mbapi):
    for c in mbapi.getClasses():
        try:
            if c['Active'] is True:
                start = c['StartDateTime']
                end = c['EndDateTime']
                id = c['Id']
                name = c['ClassDescription']['Name']
                active = c['Active']
                print(f"id={id}, name={name}, start={start}, end={end}")
                gymClass.objects.update_or_create(id=id, startTime=start, endTime=end, name=name, active=active)
        except Exception as e:
            print(traceback.format_exc())


def loadClients(mbapi):
    for client in mbapi.getClients():
        try:
            active = client.get('Active')
            email = client.get('Email')
            first_name = client.get('FirstName')
            last_name = client.get('LastName')
            id = client.get('Id')
            uniq_id = client.get('UniqueId')
            mobile = client.get('MobilePhone')
            home = client.get('HomePhone')
            gender = client.get('Gender')
            photo = client.get('PhotoURL')

            gymClient.objects.update_or_create(
                id=id, first_name=first_name, last_name=last_name,
                active=active, email=email, homePhone=home, mobile=mobile,
                photoURL=photo, gender=gender
            )
        except Exception as e:
            print(traceback.format_exc())
