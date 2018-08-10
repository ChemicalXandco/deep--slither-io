from tkinter import *
from tkinter import ttk
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

def sep(root, rownum):
    ttk.Separator(root,orient=HORIZONTAL).grid(row=rownum, columnspan=2, pady=10, sticky="ew")

dt = dummydt()
working = False

root = Tk()
root.title('.IO Bot')
# root.iconbitmap('icon.ico')
load = BooleanVar()

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

def loadnet(entry, loadthenet, label=None):
    global dt
    dt = deeptool(0, entry.get())
    if loadthenet:
        dt.model('y')
    else:
        dt.model('n')

    entry.config(state='readonly')
    if label != None:
        label.config(text="Model loaded ")

def unloadnet(entry, label=None):
    global dt
    entry.config(state='normal')
    if label != None:
        label.config(text="")

modnamelab = Label(root, text="Name of model: ")
modnamelab.grid(column=0,row=1,sticky=E)

modnament = Entry(root)
modnament.grid(column=1,row=1,sticky=W)

loadit = Checkbutton(root, text="Load from file? ", variable=load, onvalue=True, offvalue=False)
loadit.grid(column=1,row=2,sticky=W)

loaded = Label(root, text="")
loaded.grid(column=0,row=3,sticky=E)

modelbut = Button(root, text="Load model", command=lambda: loadnet(modnament, load.get(), loaded))
modelbut.grid(column=1,row=3,sticky=W)

unmodelbut = Button(root, text="Unload model", command=lambda: unloadnet(modnament, loaded))
unmodelbut.grid(column=1,row=4,sticky=W)

sep(root, 5)

entrycap = Entry(root)
entrycap.grid(column=0,row=6,padx=5,sticky=E)

docap = Button(root, text="Capture data", command=lambda: cap(entrycap.get(), docap, root))
docap.grid(column=1,row=6,sticky=W)

sep(root, 7)

'''

trainit = Button(root, text="Train (May take a long time)", command=lambda: dt.train(1))
trainit.grid(column=1,row=5)

run = Button(root, text="Start bot", command=start)
run.grid(column=1,row=4)

stoprun = Button(root, text="Stop bot", command=stop)
stoprun.grid(column=1,row=5)

entrycaplab = Label(root, text="Time to capture: ")
entrycaplab.grid(column=0,row=1)

'''

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
