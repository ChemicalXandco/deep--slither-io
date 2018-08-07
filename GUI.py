from tkinter import *
from deeptools import deeptool
 
root = Tk()
root.title('IO Bot')
# root.iconbitmap('icon.ico')
 
# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
 
root.mainloop()
