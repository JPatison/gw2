#gui code
import gw2botwserver
import subprocess

master = Tk()
root = tkinter.Tk()
root.withdraw()
root.wm_attributes("-topmost",1)

def saveusername():
    global user
    user = ebutton.get()
    accountlinesplit[0] = str(user)
    print(user)
    global password
    password = lbutton.get()
    accountlinesplit[1]= str(password)
    print(password)
    account = open('account.txt', 'r+').close()
    account = open('account.txt', 'r+').write(accountlinesplit[0]+','+accountlinesplit[1])
    


def userpass():
    global ebutton
    global lbutton
    ebutton = Entry(master)
    ebutton.pack()
    lbutton = Entry(master)
    lbutton.pack()
    f.pack()
    

def close():
    n.pack()
    root.quit()
    
def gw2source():
    global root
    global gw2location
    gw2location = filedialog.askopenfilename()
    gw2locationfile= open('gw2location.txt', 'w').close()
    gw2locationfile= open('gw2location.txt', 'w').write(gw2location)

def startgw2bot():
    subprocess.call("gw2botwserver.pyw", shell=True)
    
    
    

b = Button(master, text="enter your username and password for the trading bot", command=userpass)
f = Button(master, text="save your account details", command=saveusername)
n = Button(master, text="Exit application", command = close)
c = Button(master, text="Choose Gw2 location", command=gw2source)
z = Button(master, text="Start Gw2 bot", command = startgw2bot)




mainloop()
