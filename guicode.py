#gui code
from tkinter import *
from tkinter import filedialog
from tkinter import Tk, Button
from subprocess import Popen 
import tkinter
import msvcrt
import subprocess
import os

master = Tk()
root = tkinter.Tk()

root.attributes("-topmost",True)
master.withdraw()
root.lift()



    
def userpass():
    os.startfile('account.txt')

def getjsonfile():
    global jsonfileprocess
    jsonfileprocess = Popen("python getsolditemsjsonfile.pyw")

def close():
    n.pack()
    process.terminate()
    root.destroy()

def enteryourtradingcharname():
    os.startfile('tradingcharname.txt')

def entercharid():
    os.startfile('charachterid.txt')

    
def gw2source():
    global root
    global gw2location
    gw2location = filedialog.askopenfilename()
    gw2locationfile= open('gw2location.txt', 'w').close()
    gw2locationfile= open('gw2location.txt', 'w').write(gw2location)

def startgw2bot():
    global process
    process = Popen("python gw2botwserver.pyw")

x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 1.1    
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 20
root.geometry("+%d+%d" % (x, y))

        

b = Button(root, text="Enter your username,password ", command=userpass)
i = Button(root, text="Enter your charachter ID", command=entercharid)
u = Button(root, text="Enter your trading character name", command=enteryourtradingcharname)
k = Button(root, text="Get sold items json file", command=getjsonfile)
n = Button(root, text="Exit application", command = close)
c = Button(root, text="Choose Gw2 location", command=gw2source)
z = Button(root, text="Start Gw2 bot", command = startgw2bot)

c.pack()
u.pack()
b.pack()
i.pack()
k.pack()
z.pack()
n.pack()

mainloop()
