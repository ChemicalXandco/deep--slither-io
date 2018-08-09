from tkinter import *
from PIL import Image
from PIL import ImageTk
from deeptools import deeptool

root = Tk()
root.title('.IO Bot')
# root.iconbitmap('icon.ico')

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)

res = (root.winfo_screenwidth(), root.winfo_screenheight())

panel = None

dt = deeptool(0, 'slither')

dt.model('y')

while True:
    dt.control()

    screen = Image.fromarray(dt.ff.getopencvformat(dt.img, True, int(res[0]/4), int(res[1]/4)))
    tkscreen = ImageTk.PhotoImage(screen)

    if panel is None:
        panel = Label(image=tkscreen)
        panel.image = tkscreen
        panel.grid(column=0,row=0)
    else:
        panel.configure(image=tkscreen)
        panel.image = tkscreen

    root.update_idletasks()
    root.update()
