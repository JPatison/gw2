import requests, json, win32api, win32gui, win32con, time, win32com.client, sys, types, string
import subprocess


shell = win32com.client.Dispatch("WScript.Shell")
char_id = "4DCA2230-9686-E211-A9A3-9C8E990DC2EE"
session_key = '8846579D-A190-4B3C-91F5-581705D47092'
xcoordfirstitem = 250
ycoordfirstitem = 151
xcoordremovefirstitem = 96
ycoordremovefirstitem = 154
xcoordremoveitem = 96
ycoordremoveitem = 154
l = 0

gold = 0
silver = 0
copper = 0
poop=0
o = 0
pages = 0
removeitempages = 0
pagecounter = 0

time.sleep(4)

toplist = []
winlist = []
toplist2 = []
winlist2 = []



def startgw2():
    global session_key
    global soup
    global hwnd
    
    try: win32api.WinExec('C:\Documents and Settings\Administrator\Desktop\Guild Wars 2\gw2.exe') # Works seamlessly
    except: pass
    time.sleep(60)
    #print("Iclicked my char to login")
    doubleclick(476,668)
    time.sleep(1)
    shell.SendKeys("{ENTER}")
    time.sleep(90)
    
    click(178,12)
    time.sleep(1)
    click(666,20)
    time.sleep(1)
    click(178,12)
    time.sleep(2)
    subprocess.call(['java', '-jar', 'getsessionkey\getsessionkey.jar'])
    time.sleep(.2)
    sessionkeyfile = open('sessionVal.txt', 'r+')
    session_key = sessionkeyfile.readline()
    print(session_key)
    



def getjson():
    global r2
    global r3
    global headers
    global GW2
    global solditems
    def enum_callback(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_callback, toplist)
    GW2 = [(hwnd, title) for hwnd, title in winlist if 'guild wars 2' in title.lower()]
    GW2 = GW2[0]
    headers = {'Cookie': 's='+session_key}
    #r1 = requests.get('https://tradingpost-live.ncplatform.net/authenticate?session_key=3B31C524-E96D-4288-A44C-BBAB85219ADF&source=/me')
    r2 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers, verify = False)
    r3 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers, verify = False)
    solditems = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=past&type=sell&offset=1&count=3000',headers = headers, verify = False)

    
def autoputupbuyordersforitemsivesold():
    global solditemsjson
    global oldsellitemsjson
    boot = 4
    getjson()
    sitems = []
    sitemsprice = []
    oldsitems = []
    json_data=open('solditems.json')
    oldsellitemsjson = json.load(json_data)
    json_data.close()
    solditemsjson = solditems.json()
    
    
    for x in range(0,len(solditemsjson['listings'])):
            sitems.append(solditemsjson['listings'][x]['data_id'])
            oldsitems.append(oldsellitemsjson['listings'][x]['data_id'])
            sitemsprice.append(solditemsjson['listings'][x]['buy_price'])
    while(boot == 4):
        cat = 0
        
        for a, b, in zip(oldsitems, sitems):
            if a == b:
                cat += 1
                print(a +"does equal" + b)
            if a != b:
                print(a +"does not equal" + b)
                print(b)
                print(sitemsprice[cat])
                trader.buy(b,1,sitemsprice[cat])
                print(sitems[cat])
                del sitems[cat]
                del sitemsprice[cat]
                break
        if cat >= 70:
            with open('solditems.json', 'w') as f:
                json.dump(solditemsjson, f)
                boot = 5
        print(cat)
                
        
    
    #i have a file named sold items on my computer
    #it does a get json and compares my newly sold items list to my old one
    #if they are different it takes those new items and sets up a buy order for them if the spread is a minimum of 20 copper
    #when it is done it overwrites this new sold items list with the old one

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def rightclick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def doubleclick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

var = 1


getjson()
solditemsjson = solditems.json()
with open('solditems.json', 'w') as f:
    json.dump(solditemsjson, f)

