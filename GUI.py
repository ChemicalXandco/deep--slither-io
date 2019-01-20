from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from deeptools import deeptool, picklewrite, pickleread, time
import numpy as np

class dummydt:
    def __init__(self):
        self.notfake = False
        self.pause = False
        self.message = "Model not loaded!"
    class ff:
        def getopencvformat():
            print("None of this!")
    def capdata(self, captures, printit=True, gui=None, root=None):
        print(self.message)
    def train(self, n_epochs):
        print(self.message)

def sep(root, rownum):
    ttk.Separator(root,orient=HORIZONTAL).grid(row=rownum, columnspan=2, pady=10, sticky="ew")

dt = dummydt()
working = False
playing = False

root = Tk()
root.title('.IO Bot')
res = (root.winfo_screenwidth(), root.winfo_screenheight())
# root.iconbitmap('icon.ico')
load = BooleanVar()
timelinepos = IntVar()

def start():
    if dt.notfake:
        global working
        working = True
        dt.pause = False
    else:
        print(dt.message)

def stop():
    if dt.notfake:
        global working
        global playing
        working = False
        playing = False
        
    else:
        print(dt.message)

def play():
    if dt.notfake:
        global playing
        playing = True
    else:
        print(dt.message)

def cap(captime, button, scale, root):
    try:
        timetocap = int(captime)
    except Exception as e:
        print(e)
        return
    dt.capdata(timetocap, False, button, root)
    scale.config(to=timetocap*10)
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
    dt = dummydt()
    entry.config(state='normal')
    if label != None:
        label.config(text="")

def savecap():
    picklewrite(entrycapname.get()+'.dat', [dt.imgs, dt.avgdirs])

def opencap():
    out = pickleread(entrycapname.get()+'.dat')
    dt.imgs, dt.avgdirs = out[0], out[1]
    timeline.config(to=dt.imgs.shape[0])

modnamelab = Label(root, text="Name of model: ")
modnamelab.grid(column=0,row=1,sticky=E)

modnameframe = Frame(root)
modnameframe.grid(column=1,row=1,sticky=W)

modnament = Entry(modnameframe)
modnament.grid(column=0,row=0,sticky=E)

modnamelabext = Label(modnameframe, text=".tfl")
modnamelabext.grid(column=1,row=0,sticky=W)

loadit = Checkbutton(root, text="Load from file? ", variable=load, onvalue=True, offvalue=False)
loadit.grid(column=1,row=2,sticky=W)

loaded = Label(root, text="")
loaded.grid(column=0,row=3,sticky=E)

modelbut = Button(root, text="Load model", command=lambda: loadnet(modnament, load.get(), loaded))
modelbut.grid(column=1,row=3,sticky=W)

unmodelbut = Button(root, text="Unload model", command=lambda: unloadnet(modnament, loaded))
unmodelbut.grid(column=1,row=4,sticky=W)

sep(root, 5)

entrycaplab = Label(root, text="Time to capture: ")
entrycaplab.grid(column=0,row=6,sticky=E)

entrycap = Entry(root)
entrycap.grid(column=1,row=6,sticky=W)

docap = Button(root, text="Capture data", command=lambda: cap(entrycap.get(), docap, timeline, root))
docap.grid(column=1,row=7,sticky=W)

entrycapnamelab = Label(root, text="Name of capture file: ")
entrycapnamelab.grid(column=0,row=8,sticky=E)

capnameframe = Frame(root)
capnameframe.grid(column=1,row=8,sticky=W)

entrycapname = Entry(capnameframe)
entrycapname.grid(column=0,row=0,sticky=E)

entrycapnamelabext = Label(capnameframe, text=".dat")
entrycapnamelabext.grid(column=1,row=0,sticky=W)

capbut = Button(root, text="Save captured data", command=savecap)
capbut.grid(column=1,row=9,sticky=W)

uncapbut = Button(root, text="Open captured data", command=opencap)
uncapbut.grid(column=1,row=10,sticky=W)

timelineframe = Frame(root)
timelineframe.grid(column=0,row=11,columnspan=2)

timeline = Scale(timelineframe, variable=timelinepos, from_=1, to=1, length=(res[0]/4)+100, orient=HORIZONTAL)
timeline.grid(column=1,row=0)

playicon = PhotoImage(file="assets/play.png")
pauseicon = PhotoImage(file="assets/pause.png")

playbut = Button(timelineframe, image=playicon, width="25", height="25", command=play)
pausebut = Button(timelineframe, image=pauseicon, width="25", height="25", command=stop)

playbut.grid(column=2,row=0)
pausebut.grid(column=3,row=0)

sep(root, 12)

entrainlab = Label(root, text="How many epochs? (100+ recommended): ")
entrainlab.grid(column=0,row=13,sticky=E)

entrytrain = Entry(root)
entrytrain.grid(column=1,row=13,sticky=W)

trainit = Button(root, text="Train (May take a long time)", command=lambda: dt.train(entrytrain.get()))
trainit.grid(column=1,row=14,sticky=W)

sep(root, 15)

run = Button(root, text="Start bot", command=start)
run.grid(column=1,row=16,sticky=W)

stoprun = Button(root, text="Stop bot", command=stop)
stoprun.grid(column=1,row=17,sticky=W)

pauselab = Label(root, text="")
pauselab.grid(column=0,row=16,sticky=E)

pauseguide = Label(root, text="Press 'P' to pause bot when running press again to unpause")
pauseguide.grid(column=0,row=17,sticky=E)

black = np.zeros((int(res[1]/4), int(res[0]/4), 3))

screen = Image.fromarray(black.astype(np.uint8))
tkscreen = ImageTk.PhotoImage(screen)
panel = Label(image=tkscreen)
panel.image = tkscreen
panel.grid(column=0,row=0)

def setpreview(img, panel):
    screen = Image.fromarray(dt.ff.getopencvformat(img, True, int(res[0]/4), int(res[1]/4)))
    tkscreen = ImageTk.PhotoImage(screen)
    panel.configure(image=tkscreen)
    panel.image = tkscreen

while True:
    if working and dt.notfake:
        dt.control()
        setpreview(dt.img, panel)

    if playing:
        currentframe = timelinepos.get()
        setpreview(dt.imgs[currentframe-1], panel)
        time.sleep(0.1)
        if currentframe != timeline.cget('to'):
            timelinepos.set(currentframe+1)
        else:
            playing = False
        working = False

    if dt.pause:
        pauselab.config(text="Bot paused ")
    else:
        pauselab.config(text="")

    root.update_idletasks()
    root.update()
