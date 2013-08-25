from PIL import Image
from PIL import ImageGrab
import subprocess
import time
import win32api
import win32gui, win32con, win32com.client
apples = 0
peaches = 0

def ocr(image):
    process = subprocess.Popen(['tesseract.exe', image,'outputfromtesseract'])
    process.communicate()

def choosewhatcharachtertouse():
    global apples
    global peaches
    time.sleep(2)
    hulu = 4
    while(hulu == 4):
      time.sleep(1)
      im = ImageGrab.grab(bbox=(40,440,300,475))
      im.save('tradingcharname.bmp')
      ocr('tradingcharname.bmp')
      tcharname = open('tradingcharname.txt').readline()
      print(tcharname)
      with open('outputfromtesseract.txt') as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))
      output = open('outputfromtesseract.txt').read()
      print(output)
          
      if tcharname in open('outputfromtesseract.txt').read():
        print("true")
        hulu = 5
      else:
        click(476+apples,668+peaches)
        apples += 100


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

choosewhatcharachtertouse()
