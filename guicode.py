#gui code
from tkinter import *
from tkinter import filedialog
from tkinter import Tk, Button
from subprocess import Popen 
import tkinter
import msvcrt
import subprocess

master = Tk()
root = tkinter.Tk()

root.attributes("-topmost",True)
master.withdraw()
root.lift()
account = open('account.txt', 'r+')
accountline = account.readline()
accountlinesplit = accountline.split(",")

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
    ebutton = Entry(root)
    ebutton.pack()
    lbutton = Entry(root)
    lbutton.pack()
    f.pack()
    

def close():
    n.pack()
    process.terminate()
    root.destroy()
    
    
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

        

b = Button(root, text="enter your username and password for the trading bot", command=userpass)
f = Button(root, text="save your account details", command=saveusername)
n = Button(root, text="Exit application", command = close)
c = Button(root, text="Choose Gw2 location", command=gw2source)
z = Button(root, text="Start Gw2 bot", command = startgw2bot)

c.pack()
b.pack()
z.pack()
n.pack()

mainloop()
