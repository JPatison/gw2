import requests, json, webbrowser, win32api, win32gui, win32con, time, win32com.client, winsound, sys, math, logging, types, string, os
from pprint import pprint
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from lxml import etree
import lxml
from ctypes import *



logging.basicConfig(
  filename='gw2.log',
  format='%(asctime)s %(levelname)s %(message)s',
  level=logging.DEBUG,)


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

class gw2trader():
    global session_key
    def __init__(self):
        # game session id
        self.session_id = session_key
        # character id
        self.char_id = char_id
        self.opener = urllib.request.build_opener()
        self.opener.addheaders.append(('Cookie', 's='+self.session_id))

    def buy(self,item_id,amount,price):
        yolo = 'https://tradingpost-live.ncplatform.net/ws/item/'+str(item_id)+'/buy'+'?'+'count='+str(amount)+'&price='+str(price)+'&charid='+self.char_id
        print(yolo)
        headers = {'Cookie': 's='+session_key,'Referer': 'https://tradingpost-live.ncplatform.net/me'}
        print(headers)
        r6 = requests.post(yolo, headers = headers)
        print(r6)

    def search(self,offset,type,levelmin=68,levelmax=80,rarity=4,subtype=''):
        response = self.opener.open('https://tradingpost-live.ncplatform.net/ws/search.json?text=&type='+str(type)+'&subtype='+str(subtype)+'&rarity='+str(rarity)+'&levelmin='+str(levelmin)+'&levelmax='+str(levelmax)+'&removeunavailable=1&offset='+str(offset))
        return response.read()

    def item(self,item_id):
        response = self.opener.open('https://tradingpost-live.ncplatform.net/ws/listings.json?id='+str(item_id))
        return response.read()

    def cancel(self,item_id,listing_id):
        google = 'https://tradingpost-live.ncplatform.net/ws/item/'+str(item_id)+'/cancel.json'+'?'+'listing='+str(listing_id)+'&isbuy=1&charid='+self.char_id
        print(google)
        headers = {'Cookie': 's='+session_key,'Referer': 'https://tradingpost-live.ncplatform.net/me'}
        print(headers)
        r5 = requests.post(google, headers = headers)
        print(r5)

    def inventar(self,type,offset,time='now',count=10):
        response = self.opener.open('https://tradingpost-live.ncplatform.net/ws/me.json?time='+time+'&type='+type+'&charid='+self.char_id+'&offset='+str(offset)+'&count='+str(count))
        return response.read()

    def nice_money(self,amount):
        ret = '0'*(6-len(str(amount)))+str(amount)
        if amount<100:
            return ret[4:6]+'c'
        elif amount>=100 and amount<10000:
            return ret[2:4]+'s '+ret[4:6]+'c'
        elif amount>=10000:
            return ret[0:2]+'g '+ret[2:4]+'s '+ret[4:6]+'c'

trader = gw2trader()

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
    time.sleep(110)
    
    click(178,12)
    time.sleep(1)
    click(666,20)
    time.sleep(1)
    click(178,12)
    time.sleep(1)
    
    time.sleep(4)
    try: win32api.WinExec("C:\Documents and Settings\Administrator\Desktop\ZicoresTradingPostNotifier\ZicoresTradingPostNotifier.exe") # Works seamlessly
    except: pass

    time.sleep(1)
    click(25,263)
    time.sleep(1)
    click(997,529)
    time.sleep(40)
    shell.SendKeys("%{TAB}")
    time.sleep(60)
    shell.SendKeys("%{F4}")
    time.sleep(20)
    
    soup = BeautifulSoup(open('C:\Documents and Settings\Administrator\Application Data\ZicoresTradingPostNotifier\config.xml'), "xml")
    for SessionKey in soup.SessionKey:
        session_key = SessionKey


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
    '''
    win32gui.ShowWindow(GW2[0], win32con.SW_MINIMIZE)
    webbrowser.open(session_key)
    time.sleep(3)
    webbrowser.open("https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000")
    time.sleep(2)
    shell.SendKeys("^s")
    time.sleep(2)
    shell.SendKeys("m")
    time.sleep(1)
    shell.SendKeys("e")
    time.sleep(1)
    shell.SendKeys("{ENTER}")
    time.sleep(1)
    shell.SendKeys("{TAB}")
    time.sleep(1)
    shell.SendKeys("{ENTER}")
    time.sleep(1)
    shell.SendKeys("^w")
    time.sleep(2)
    shell.SendKeys("^w")
    time.sleep(4)
    win32gui.ShowWindow(GW2[0], win32con.SW_MAXIMIZE)
    '''
    headers = {'Cookie': 's='+session_key}
    #r1 = requests.get('https://tradingpost-live.ncplatform.net/authenticate?session_key=3B31C524-E96D-4288-A44C-BBAB85219ADF&source=/me')
    r2 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers)
    r3 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers)
    solditems = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=past&type=sell&offset=1&count=3000',headers = headers)
    
def checktomakesureimnotbuyingitemtwice():
    global dataids
    global var
    global data
    global s
    global mobeen
    global listingids   
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
                trader.cancel(dataids[mobeen],listingids[mobeen])
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
    boot = 4
    getjson()
    sitems = []
    sitemsprice = []
    oldsitems = []
    json_data=open('C:\Documents and Settings\Administrator\My Documents\GitHub\gw2\solditems.json')
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
            if cat == 90:
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
    time.sleep(2)
    shell.SendKeys(gold)
    time.sleep(2)
    doubleclick(176,314)
    time.sleep(2)
    shell.SendKeys(silver)
    time.sleep(2)
    doubleclick(241,317)
    time.sleep(2)
    shell.SendKeys(copper)
    time.sleep(2)

def increase_coord():
    global l
    global ycoordfirstitem
    global ycoordremoveitem
    global xcoordfirstitem
    global ycoordfirstitem
    global xcoordremoveitem
    global removeitempages
    global pages
    global pagecounter
    if l <= 7:
        ycoordfirstitem += 48
        ycoordremoveitem += 48 
        l += 1
    elif l == 8:
        removeitempages = 1
        ycoordfirstitem += 48
        ycoordremoveitem += 48 
        l += 1
    else:
        xcoordfirstitem = 250
        ycoordfirstitem = 151
        xcoordremoveitem = 96
        ycoordremoveitem = 154
        time.sleep(1)
        pages += 1
        pagecounter +=1
        #ichanged l = 1 to 0 
        l = 0

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
    
        
def gothroughbuyitems():
    global pagecounter
    global r3
    global r2
    global newdata
    global poop
    global removeitempages
    global headers
    global buyprice
    global gold
    global silver
    global copper
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


    #json_data=open('C:\Documents and Settings\Administrator\My Documents\Downloads\me.json')
    data = r2.json()

    #pprint(data)
    #json_data.close()


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
        #i SHOULD PUT IN A FUCNTION THAT GETS A NEW JSON COMPARES IT TO Len of DATA IDS and IF ITS DIFFIFERENT START OVER
        time.sleep(2)
        for _ in range(pagecounter):
            click(864,626)
            pagecounter -= 1
        if a > b:
            logging.error('buyprice is greater than a unitprice of %s', b)
            time.sleep(4)
            click(xcoordfirstitem,ycoordfirstitem)
            time.sleep(4)
            #click again	
            click(118,195)
            time.sleep(4)
            #click again
            click(201,320)
            time.sleep(4)
            convertbuypricenumbertogsc(poop)
            logging.error("gold = %s", gold)
            logging.error("silver = %s", silver)
            logging.error("copper = %s", copper)
            inputprice(gold,silver,copper)
            time.sleep(4)
            #click place order
            logging.error("I clicked place order")
            click(139,390)
            time.sleep(4)
            getmoney()
            #click on sell orders
            click(28,219)
            time.sleep(4)
            #click(gobacktomytransactions)
            click(24,261)
            time.sleep(4)
            click(431,73)
            time.sleep(4)
            click(415,119)
            time.sleep(4)
            #click removeitem 
            logging.error("I am getting ready to remove item")
            for g in range(pages):
                click(864,626)
                time.sleep(4)
            for r in range(removeitempages):
                click(864,626)
                time.sleep(4)
            if removeitempages == 1:
                click(xcoordremovefirstitem,ycoordremovefirstitem)
                logging.info("i tehoritailcally clicked on remove item for teh 10th item =ycoord %s", ycoordremoveitem)
                time.sleep(1)
                pagecounter -= 1
            else:
                logging.info("i removed the item at ycoordremoveitem(add 48 to this) %s =", ycoordremoveitem) 
                click(xcoordremoveitem,(ycoordremoveitem + 48))
                time.sleep(4)
        if a <= b:
            logging.error("buyprice is less than or equal to a unitprice of %s", b)
        poop += 1
        moveforwardandback()
        removeitempages = 0
        increase_coord()
        r3 = requests.get('https://tradingpost-live.ncplatform.net/ws/me.json?time=now&type=buy&offset=1&count=3000',headers = headers)
        
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

startgw2()
logging.error("my char id is = %s",char_id)
logging.error("my session key is %s",session_key)
checktomakesureimnotbuyingitemtwice()
autoputupbuyordersforitemsivesold()
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


