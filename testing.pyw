import requests, json, win32api, win32gui, win32con, time, win32com.client, sys, math, logging, types, string, os
from ctypes import *
import xmlrpc.client
import msvcrt
import subprocess
from PIL import *
from PIL import ImageGrab
account = open('account.txt', 'r+')
accountline = account.readline()
accountlinesplit = accountline.split(",")
user = str(accountlinesplit[0])
password = str(accountlinesplit[1])
gw2locationfile = open('gw2location.txt','r+')
gw2location = gw2locationfile.readline()
charidfile = open('charachterid.txt')
char_id = charidfile.readline()
tradingcharname = open('tradingcharname.txt').readline()



logging.basicConfig(
  filename='gw2.log',
  format='%(asctime)s %(levelname)s %(message)s',
  level=logging.DEBUG,)

logging.error("Starting Guild wars 2 Trading Bot")
logging.error("my username and password are")
logging.error(user)
logging.error(password)
logging.error("gw2 is located at")
logging.error(gw2location)
logging.error("my char id is")
logging.error(char_id)
logging.error("my trading char name is")
logging.error(tradingcharname)

server = xmlrpc.client.Server('https://'+user+':'+password+'@108.61.63.199:8000')
logging.error("the server is")
logging.error(server)

if os.name == 'nt':
    PUL = POINTER(c_ulong)
    class KeyBdInput(Structure):
        _fields_ = [("wVk", c_ushort),
                    ("wScan", c_ushort),
                    ("dwFlags", c_ulong),
                    ("time", c_ulong),
                    ("dwExtraInfo", PUL)]

    class HardwareInput(Structure):
        _fields_ = [("uMsg", c_ulong),
                    ("wParamL", c_short),
                    ("wParamH", c_ushort)]

    class MouseInput(Structure):
        _fields_ = [("dx", c_long),
                    ("dy", c_long),
                    ("mouseData", c_ulong),
                    ("dwFlags", c_ulong),
                    ("time",c_ulong),
                    ("dwExtraInfo", PUL)]

    class Input_I(Union):
        _fields_ = [("ki", KeyBdInput),
                    ("mi", MouseInput),
                    ("hi", HardwareInput)]

    class Input(Structure):
        _fields_ = [("type", c_ulong),
                    ("ii", Input_I)]

    KEYEVENTF_KEYUP = 0x2
    KEYEVENTF_UNICODE = 0x4
    KEYEVENTF_SCANCODE = 0x8
    MAPVK_VK_TO_VSC = 0

    def SendInput(txt):
        i = Input()
        i.type = 1
        extra = c_ulong(0)
        pextra = pointer(extra)
        for c in txt:
            vk = windll.user32.VkKeyScanW(ord(c))
            sc = windll.user32.MapVirtualKeyW(vk&0xff, MAPVK_VK_TO_VSC)
            i.ii.ki.wVk = 0
            i.ii.ki.wScan = sc
            i.ii.ki.dwFlags = KEYEVENTF_SCANCODE
            i.ii.ki.time = 0
            i.ii.ki.dwExtraInfo = pextra
            windll.user32.SendInput(1, byref(i), sizeof(i))
            i.ii.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
            windll.user32.SendInput(1, byref(i), sizeof(i))

    def SendKeyPress(key):
        i = Input()
        i.type = 1
        extra = c_ulong(0)
        pextra = pointer(extra)
        vk = windll.user32.VkKeyScanW(ord(key))
        sc = windll.user32.MapVirtualKeyW(vk&0xff, MAPVK_VK_TO_VSC)
        i.ii.ki.wVk = 0
        i.ii.ki.wScan = sc
        i.ii.ki.dwFlags = KEYEVENTF_SCANCODE
        i.ii.ki.time = 0
        i.ii.ki.dwExtraInfo = pextra
        windll.user32.SendInput(1, byref(i), sizeof(i))

    def SendKeyRelease(key):
        i = Input()
        i.type = 1
        extra = c_ulong(0)
        pextra = pointer(extra)
        vk = windll.user32.VkKeyScanW(ord(key))
        sc = windll.user32.MapVirtualKeyW(vk&0xff, MAPVK_VK_TO_VSC)
        i.ii.ki.wVk = 0
        i.ii.ki.wScan = sc
        i.ii.ki.time = 0
        i.ii.ki.dwExtraInfo = pextra
        i.ii.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
        windll.user32.SendInput(1, byref(i), sizeof(i))


shell = win32com.client.Dispatch("WScript.Shell")

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
apples = 0


time.sleep(4)

toplist = []
winlist = []
toplist2 = []
winlist2 = []
def ocr(image):
    process = subprocess.Popen(['tesseract.exe', image,'outputfromtesseract'])
    process.communicate()

def choosewhatcharachtertouse():
    global apples
    time.sleep(2)
    hulu = 4
    while(hulu == 4):
        time.sleep(1)
        im = ImageGrab.grab(bbox=(40,440,300,475))
        im.save('tradingcharname.bmp')
        ocr('tradingcharname.bmp')
        tcharname = open('tradingcharname.txt').readline()
        
        with open('outputfromtesseract.txt') as f_in:
            lines = filter(None, (line.rstrip() for line in f_in))
        output = open('outputfromtesseract.txt').read()
        logging.error(output)
        if tcharname not in open('outputfromtesseract.txt').read():
            apples += 100
            click(476+apples,668)
            
        else:
            logging.error("I found my trading char")
            doubleclick(476+apples,668)
            hulu = 5
            
def startgw2():
    global session_key
    global soup
    global hwnd
    
    try: win32api.WinExec('C:\Documents and Settings\Administrator\Desktop\Guild Wars 2\gw2.exe') # Works seamlessly
    except: pass
    time.sleep(60)
    choosewhatcharachtertouse()
    time.sleep(1)
    shell.SendKeys("{ENTER}")
    logging.error("i have clicked my char and am going into the game")
    time.sleep(90)
    
    click(178,12)
    time.sleep(1)
    click(666,20)
    time.sleep(1)
    click(178,12)
    time.sleep(2)
    time.sleep(1)
    click(997,529)
    time.sleep(1)
    subprocess.call(['java', '-jar', 'getsessionkey\getsessionkey.jar'])
    time.sleep(.2)
    sessionkeyfile = open('sessionVal.txt', 'r+')
    session_key = sessionkeyfile.readline()
    logging.error("this is my session key")
    logging.error(session_key)


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

    r2 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers, verify = False)
    r3 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers, verify = False)
    solditems = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=past&type=sell&offset=1&count=3000',headers = headers, verify = False)
    logging.error("i have gone through get json now")    

def checktomakesureimnotbuyingitemtwice():
    global dataids
    global var
    global data
    global s
    global mobeen
    global listingids
    global char_id
    global session_key
    global server
    mobeen = 0
    ameer = 0
    fart = 0
    getjson()
    s = []
    data = r2.json()
    dataids = []
    listingids = []
    
    
    for x in range(0,len(data['listings'])):
        dataids.append(data['listings'][x]['data_id'])
        listingids.append(data['listings'][x]['listing_id'])
    while(ameer == 0):
        for i in dataids:
            if i not in s:
                print('i is not in s')
                
                print(len(s))
                print(len(dataids))
                s.append(i)
                mobeen += 1
            else:
                print(mobeen)
                logging.error("i was buying the same of=%s",dataids[mobeen])
                print(dataids[mobeen],listingids[mobeen])
                server.cancel(dataids[mobeen],listingids[mobeen],str(char_id),str(session_key))
                break
            
        if len(s) == len(dataids):
            logging.error('len of s and and len of data ids is the same')
            ameer = 1
            break
        getjson()
        s = []
        data = r2.json()
        dataids = []
        listingids = []
        time.sleep(2)
        mobeen = 0
        for x in range(0,len(data['listings'])):
            dataids.append(data['listings'][x]['data_id'])
            listingids.append(data['listings'][x]['listing_id'])
    logging.error('gone,trhough checksameitems,I am not buying any of the same items')
    
def autoputupbuyordersforitemsivesold():
    global solditemsjson
    global oldsellitemsjson
    global server
    global session_key
    global char_id
    boot = 4
    getjson()
    sitems = []
    sitemsprice = []
    oldsitems = []
    json_data=open('solditems.json')
    oldsellitemsjson = json.load(json_data)
    json_data.close()
    solditemsjson = solditems.json()
    
    
    for x in range(0,len(solditemsjson['listings'])-1):
        print(x)
        sitems.append(solditemsjson['listings'][x]['data_id'])
        oldsitems.append(oldsellitemsjson['listings'][x]['data_id'])
        try:
            sitemsprice.append(solditemsjson['listings'][x]['buy_price'])
        except KeyError:
            sitemsprice.append('0')
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
                server.buy(b,1,sitemsprice[cat],str(char_id),str(session_key))
                print(sitems[cat])
                del sitems[cat]
                del sitemsprice[cat]
                break
        if cat >= 45:
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

def moveforwardandback():
    time.sleep(1)
    SendKeyPress('d')
    time.sleep(1)
    SendKeyRelease('d')
    time.sleep(1)
    SendKeyPress('a')
    time.sleep(1)
    SendKeyRelease('a')
    time.sleep(1)
    logging.error("i have gone through moveforwardandbackfunction")

def inputprice(gold,silver,copper):
    doubleclick(105,317)
    time.sleep(0.5)
    shell.SendKeys(gold)
    time.sleep(0.5)
    doubleclick(176,314)
    time.sleep(0.5)
    shell.SendKeys(silver)
    time.sleep(0.5)
    doubleclick(241,317)
    time.sleep(0.5)
    shell.SendKeys(copper)
    time.sleep(0.5)

def convertbuypricenumbertogsc(y):
    global o
    global copper
    global silver
    global gold
    global buyprice
    o = int(buyprice[y])
    copper = math.floor(o % 100)
    silver = math.floor((o % 10000) / 100)
    gold = math.floor((o % 1000000) / 10000)
    if(copper == 99):
        copper = 0
        silver += 1
    else:
        copper += 1



def getmoney():
    time.sleep(2)
    click(25,307)
    time.sleep(2)
    click(94,53)

def resell_items():
    time.sleep(2)
    #clickonsellyourstuff
    click(25,216)
    time.sleep(2)
    #clickfirstitem
    click(140,163)
    time.sleep(2)
    #clickonmatchlowestseller
    click(554,448)
    time.sleep(2)
    #clicksell
    click(877,265)
    time.sleep(2)
    #clickseconditem
    click(138,206)
    time.sleep(2)
    #clickonmatchlowestseller
    click(554,448)
    time.sleep(2)
    #clicksell
    click(877,265)
    time.sleep(2)
    
        
def gothroughbuyitems():
    global pagecounter
    global r3
    global r2
    global newdata
    global poop
    global removeitempages
    global pages
    global headers
    global xcoordfirstitem
    global ycoordfirstitem
    global xcoordremoveitem
    global ycoordremoveitem
    global l
    global buyprice
    global gold
    global silver
    global copper
    global server
    #click on sell orders
    click(28,219)
    time.sleep(4)
    #click(gobacktomytransactions)
    click(24,261)
    time.sleep(4)
    click(431,73)
    time.sleep(4)
    click(415,119)

    getjson()


    
    data = r2.json()

    dataids = []
    buyprice = []
    unitprice = []
    newdataids = []


    for x in range(0,len(data['listings'])):
        dataids.append(data['listings'][x]['data_id'])
        buyprice.append(data['listings'][x]['buy_price'])
        unitprice.append(data['listings'][x]['unit_price'])
    
    
    

    for a, b, in zip(buyprice, unitprice):
        logging.error('poop = %s',poop)
        logging.error('pages = %s',pages)
        logging.error("xclicked %s", xcoordfirstitem)
        logging.error("yclicked %s", ycoordfirstitem)
        logging.error("xremoved %s", xcoordremoveitem)
        logging.error("yremoved %s", ycoordremoveitem)
        logging.error("l = %s", l)
        logging.error("len of data listings = %s", len(data['listings']))
        logging.error("removeitempages = %s", removeitempages)
        time.sleep(2)
        for _ in range(pagecounter):
            click(864,626)
            pagecounter -= 1
        if a > b:
            logging.error('buyprice is greater than a unitprice of %s', b)
            time.sleep(1)
            click(xcoordfirstitem,ycoordfirstitem)
            time.sleep(3)
            #click again	
            click(118,195)
            time.sleep(1)
            #click again
            click(201,320)
            time.sleep(1)
            convertbuypricenumbertogsc(poop)
            logging.error("gold = %s", gold)
            logging.error("silver = %s", silver)
            logging.error("copper = %s", copper)
            inputprice(gold,silver,copper)
            time.sleep(0.5)
            #click place order
            logging.error("I clicked place order")
            click(139,390)
            time.sleep(0.5)
            getmoney()
            #click on sell orders
            click(28,219)
            time.sleep(4)
            #click(gobacktomytransactions)
            click(24,261)
            time.sleep(3)
            click(431,73)
            time.sleep(1)
            click(415,119)
            time.sleep(1)
            #click removeitem 
            logging.error("I am getting ready to remove item")
            for g in range(pages):
                click(864,626)
                time.sleep(2)
            for r in range(removeitempages):
                click(864,626)
                time.sleep(2)
            if removeitempages == 1:
                click(xcoordremovefirstitem,ycoordremovefirstitem)
                logging.info("i tehoritailcally clicked on remove item for teh 10th item =ycoord %s", ycoordremoveitem)
                time.sleep(1)
                pagecounter -= 1
            else:
                logging.info("i removed the item at ycoordremoveitem(add 48 to this) %s =", ycoordremoveitem) 
                click(xcoordremoveitem,(ycoordremoveitem + 48))
                time.sleep(2)
        if a <= b:
            logging.error("buyprice is less than or equal to a unitprice of %s", b)
        poop += 1
        moveforwardandback()
        removeitempages = 0
        response = []
        response = server.increase_coord(l,ycoordfirstitem,ycoordremoveitem,xcoordfirstitem,xcoordremoveitem,removeitempages,pages,pagecounter)
        l = response[0]
        ycoordfirstitem = response[1]
        ycoordremoveitem = response[2]
        xcoordfirstitem = response[3]
        xcoordremoveitem = response[4]
        removeitempages = response[5]
        pages = response[6]
        pagecounter = response[7]
        r3 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers, verify = False)
        
        newdata = r3.json()
        for x in range(0,len(newdata['listings'])):
            newdataids.append(newdata['listings'][x]['data_id'])
        logging.error("len of newdatalistings = %s", len(newdata['listings']))
        if len(data['listings']) != len(newdata['listings']):
            logging.error("item sizes are different,something must have been sold or something messed up")
            break
        else:
            newdataids = []
            
var = 1
server.senduserinfo(user,password)
startgw2()
logging.error("my char id is = %s",char_id)
logging.error("my session key is %s",session_key)
#autoputupbuyordersforitemsivesold()
#checktomakesureimnotbuyingitemtwice()
'''
while(var == 1):
    gothroughbuyitems()
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
    dataids = []
    buyprice = []
    unitprice = []
    newdataids = []
    moveforwardandback()
    time.sleep(100)
    logging.error("I have made it through all the buy items, or im guessing that item sizes are different thus my break works")
    checktomakesureimnotbuyingitemtwice()
    resell_items()


'''
