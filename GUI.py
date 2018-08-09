from tkinter import *
from PIL import Image
from PIL import ImageTk
from deeptools import deeptool
import numpy as np

class dummydt:
    def __init__(self):
        self.notfake = False
    class ff:
        def getopencvformat():
            print("None of this!")

dt = dummydt()
working = False

root = Tk()
root.title('.IO Bot')
# root.iconbitmap('icon.ico')

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)

def start():
    global working
    working = True
    dt.pause = False

def stop():
    global working
    working = False

def cap(captime, button, root):
    try:
        timetocap = int(captime)
    except Exception as e:
        print(e)
        return
    dt.capdata(timetocap, False, button, root)
    button.config(text="Capture data")
    root.update_idletasks()

def loadnet():
    global dt
    dt = deeptool(0, 'test')
    dt.model('y')

trainit = Button(root, text="Train (May take a long time)", command=lambda: dt.train(1))
trainit.grid(column=1,row=5)

run = Button(root, text="Start bot", command=start)
run.grid(column=1,row=4)

stoprun = Button(root, text="Stop bot", command=stop)
stoprun.grid(column=1,row=5)

docap = Button(root, text="Capture data", command=lambda: cap(entrycap.get(), docap, root))
docap.grid(column=1,row=2)

entrycap = Entry(root)
entrycap.grid(column=1,row=1)

entrycaplab = Label(root, text="Time to capture: ")
entrycaplab.grid(column=0,row=1)

pauselab = Label(root, text="Press 'P' to pause bot when running \npress again to unpause")
pauselab.grid(column=1,row=0)

res = (root.winfo_screenwidth(), root.winfo_screenheight())

black = np.zeros((int(res[1]/4), int(res[0]/4), 3))

screen = Image.fromarray(black.astype(np.uint8))
tkscreen = ImageTk.PhotoImage(screen)
panel = Label(image=tkscreen)
panel.image = tkscreen
panel.grid(column=0,row=0)

while True:
    if working and dt.notfake:
        dt.control()

        screen = Image.fromarray(dt.ff.getopencvformat(dt.img, True, int(res[0]/4), int(res[1]/4)))
        tkscreen = ImageTk.PhotoImage(screen)
        panel.configure(image=tkscreen)
        panel.image = tkscreen

    root.update_idletasks()
    root.update()
