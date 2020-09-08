import requests, json

apikey = "mhfC3OFs8r"
url = "https://fgmlogin.cf/qrv2/getlink.php?header={}&apikey="+apikey

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

class FGMQR(object):

    def __init__(self):
        self.arg = "HELLO"

    def login(header):
        self.authToken = None
        self.appName = None
        result = getJSONRequests(url.format(header))
        if result["status"] == "success":
            try:
                print("LOGIN ON YOUR LINE PHONE. TIME: 2 MINUTES\n"+result["get_link"])
                result = getJSONRequests(result["get_pin"])
                print("\nENTER PIN: "+result["pincode"])
                result = getJSONRequests(result["get_token"])
                self.authToken = result["authToken"]
                self.appName = result["appName"]
                print("CONNECTING SELFBOT...")
            except:
                print("LOGIN FAILED. Please Try Again\nNeed Help?\nJoin Our Community\nHansenGianto.gq/square.html")
        else:
            print("INVALID REQUEST\nNeed Help?\nJoin Our Community\nHansenGianto.gq/square.html")