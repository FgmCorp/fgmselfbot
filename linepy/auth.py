# -*- coding: utf-8 -*-
from akad.ttypes import IdentityProvider, LoginResultType, LoginRequest, LoginType
from .server import Server
from .session import Session
from .callback import Callback

import rsa, os, requests, json

def getJSONRequests(url, header=None):
    try:
        r = ""
        if header != None:r = requests.get(url, headers=header).text
        else:r = requests.get(url).text
        try:
            return json.loads(r)
        except Exception as e:
            print(e)
            return "REQUESTS FAILED"
    except Exception as e:
        print(e)

class Auth(object):
    isLogin     = False
    authToken   = ""
    certificate = ""

    def __init__(self):
        self.server = Server(self.appType)
        self.callback = Callback(self.__defaultCallback)
        self.server.setHeadersWithDict({
            'User-Agent': self.server.USER_AGENT,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-Carrier': self.server.CARRIER,
            'x-lal': "in_ID"
        })

    def __loadSession(self):
        self.talk       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR, self.customThrift).Talk()
        self.poll       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_POLL_QUERY_PATH_FIR, self.customThrift).Talk()
        self.channel    = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CHAN_QUERY_PATH, self.customThrift).Channel()
        self.liff       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LIFF_QUERY_PATH, self.customThrift).Liff()
        
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True

    def __loginRequest(self, type, data):
        lReq = LoginRequest()
        if type == '0':
            lReq.type = LoginType.ID_CREDENTIAL
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = LoginType.QRCODE
            lReq.keepLoggedIn = data['keepLoggedIn']
            if 'identityProvider' in data:
                lReq.identityProvider = data['identityProvider']
            if 'accessLocation' in data:
                lReq.accessLocation = data['accessLocation']
            if 'systemName' in data:
                lReq.systemName = data['systemName']
            lReq.verifier = data['verifier']
            lReq.e2eeVersion = data['e2eeVersion']
        else:
            lReq=False
        return lReq

    def loginWithCredential(self, _id, passwd):
        if self.systemName is None:
            self.systemName=self.server.SYSTEM_NAME
        if self.server.EMAIL_REGEX.match(_id):
            self.provider = IdentityProvider.LINE       # LINE
        else:
            self.provider = IdentityProvider.NAVER_KR   # NAVER
        
        if self.appName is None:
            self.appName=self.server.APP_NAME
        self.server.setHeaders('X-Line-Application', self.appName)
        self.tauth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)

        rsaKey = self.tauth.getRSAKeyInfo(self.provider)
        
        message = (chr(len(rsaKey.sessionKey)) + rsaKey.sessionKey +
                   chr(len(_id)) + _id +
                   chr(len(passwd)) + passwd).encode('utf-8')
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16), int(rsaKey.evalue, 16))
        crypto = rsa.encrypt(message, pub_key).hex()

        try:
            with open(_id + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if self.certificate is not None:
                if os.path.exists(self.certificate):
                    with open(self.certificate, 'r') as f:
                        self.certificate = f.read()

        self.auth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

        lReq = self.__loginRequest('0', {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': self.keepLoggedIn,
            'accessLocation': self.server.IP_ADDR,
            'systemName': self.systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })

        result = self.auth.loginZ(lReq)
        
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            self.callback.PinVerified(result.pinCode)

            self.server.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)

            self.auth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

            try:
                lReq = self.__loginRequest('1', {
                    'keepLoggedIn': self.keepLoggedIn,
                    'verifier': getAccessKey['result']['verifier'],
                    'e2eeVersion': 0
                })
                result = self.auth.loginZ(lReq)
            except:
                raise Exception('Login failed')
            
            if result.type == LoginResultType.SUCCESS:
                if result.certificate is not None:
                    with open(_id + '.crt', 'w') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate
                if result.authToken is not None:
                    self.loginWithAuthToken(result.authToken)
                else:
                    return False
            else:
                raise Exception('Login failed')

        elif result.type == LoginResultType.REQUIRE_QRCODE:
            self.loginWithQrCode()
            pass

        elif result.type == LoginResultType.SUCCESS:
            self.certificate = result.certificate
            self.loginWithAuthToken(result.authToken)

    def setHeaderLogin(self):
        if "CHROMEOS" in self.appName:
            return "chrome"
        else:return False

    def loginWithQrCode(self):
        # SECONDARY LOGIN SERVICE BY FGM CORP: Hansen & UNYPASS
        # Special Thanks: HelloWorld & BE-TEAM
        # PLEASE DON'T REMOVE CREATOR NAME :)
        print("[FGM SERVICE] STARTING LOGIN...")
        authToken = None
        if "token.json" not in os.listdir():
            header = self.setHeaderLogin()
            if header != None:
                apikey = "VkYXuF9NIm"
                url = "https://fgmlogin.cf/qrv2/getlink.php?header={}&apikey="+apikey
                result = getJSONRequests(url.format(header))
                if result["status"] == "success":
                    try:
                        print("[FGM SERVICE] LOGIN ON YOUR LINE PHONE. TIME: 2 MINUTES\n"+result["get_link"])
                        get_token = result["get_token"]
                        result = getJSONRequests(result["get_pin"])
                        print("\n[FGM SERVICE] ENTER PIN: "+result["pincode"])
                        result = getJSONRequests(get_token)
                        savetoken = {"authToken":result["authToken"], "appName":result["appName"]}
                        open("token.json","w").write(json.dumps(savetoken, indent=2))
                        authToken = result["authToken"]
                        print("[FGM SERVICE] PIN VERIFICATION SUCCESS")
                        print("[FGM SERVICE] CONNECTING SELFBOT...")
                    except Exception as e:
                        #print(e)
                        print("[FGM SERVICE] LOGIN FAILED. TRY AGAIN")
                else:
                    print("[FGM SERVICE] INVALID REQUESTS")
            else:
                print("[FGM SERVICE] HEADER NOT FOUND")
        else:
            print("[FGM SERVICE] TOKEN FILE FOUND !!!!")
            opentoken = open("token.json","r").read()
            result = json.loads(opentoken)
            authToken = result["authToken"]
            print("[FGM SERVICE] CONNECTING SELFBOT...")

        if authToken is not None:
            self.loginWithAuthToken(authToken)
        else:
            return False

    def loginWithAuthToken(self, authToken=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        if self.appName is None:
            self.appName=self.server.APP_NAME
        self.server.setHeadersWithDict({
            'X-Line-Application': self.appName,
            'X-Line-Access': authToken
        })
        self.authToken = authToken
        self.__loadSession()

    def __defaultCallback(self, str):
        print(str)

    def logout(self):
        self.auth.logoutZ()
