import urllib,time
import xml.parsers.expat


captivePortalIP = "192.168.0.1" # The address of the Captial Portal
captivePortalPort = "8090" #Set to "" if not using.

KeepTryingConnection=True


captivePortalAddress = captivePortalIP
if captivePortalPort != "":
 captivePortalAddress = captivePortalAddress+":"+captivePortalPort

    
#Handelers------------------------------------------------
i=0
finalData={}
temp=""

def start_element(name, attrs):
    #print 'Start element:', name, attrs
    global i,temp,finalData
    if i!=0:
      temp=name
      finalData[name]="None"
    i+=1

def end_element(name):
    pass
    #print 'End element:', name
def char_data(data):
    ss=repr(data)
    #print 'Character data:', ss
    global i,temp,finalData
    if i!=0:
      finalData[temp]=ss
#--------------------------------------------------------
    

def checkmsg(message):

    if message=="You have successfully logged in":
        print ":: CONNECTED"
        a=1
    elif message == u'The system could not log you on. Make sure your password is correct':
        print ":: INCORRECT UID/PASS"
        a=2

    elif message == "DataTransfer limit has been exceeded" or message =="You are not allowed to login at this time":
        print ":: NO DATA or NO TIME"
        a=2
    elif message == "You have reached Maximum Login Limit.":
        print ":: LOGIN LIMIT"
        a=2
    
    return a

"""
login mode = 191
logout mode = 193

"""
def processRequest(uid="",pas="",mode="191"):
    
    if pas=="":pas=uid
    if uid=="" and pas=="":mode="193"
        
    if mode=="191" :print "Username in use: "+uid
    try:
        while True:
            try:
                #print 1
                f = urllib.urlopen("http://"+captivePortalAddress+"/httpclient.html","mode="+mode+"&isAccessDenied=null&url=null&message=&username="+uid+"&password="+pas+"&saveinfo=saveinfo&login=Login")
            except IOError:
                print "No Network Connection!",
                if KeepTryingConnection:
                    print "Trying again in 5 seconds!"
                    time.sleep(5)
                else:
                    break
            except:
                print "Unkown Error!"
            else:
                break
    except KeyboardInterrupt:
        print "Keyboard Interpect"


    s = f.read() #raw Data
    
    #Data Parsing
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    p.Parse(s,1)
    
    global finalData
    message=""
    message=finalData['message']
    message=message[2:len(message)-1]
    

    checkmsg(message)


def main():
     #login
     processRequest("username","password")

     #logoff
     processRequest()








        





