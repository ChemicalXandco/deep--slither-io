from iotools import *
from dummytools import *
import numpy as np
import time, keyboard, pyautogui
from alexnet import alexnet

class deeptool:
    def __init__(self, captures, modelname):
        self.ff = FrameFunc()
        self.np = np
        self.notfake = True
        # time.sleep(5)
        self.start = True # time.time()
        self.pause = False

        self.modelname = modelname

        self.imgs, self.avgdirs = [], []

        if captures > 0:
            self.capdata(captures)

    def capdata(self, captures, printit=True, gui=None, root=None):
        imgs = []
        avgdirs = []
        avgspaces = []
        timer = captures+1
        for i in range(5):
            timer = 5-i
            if printit:
                print("Starting capture in %d" % timer)
            if gui != None:
                gui.config(text="Starting capture in %d" % timer)
                root.update_idletasks()
            time.sleep(1)
        timer = captures+1
        if printit:
            print('\ncapturing data')
        for i in range(captures*10):
            self.img, avgdir, avgspace = self.ff.getcap()
            imgs.append(self.img)
            avgdirs.append(avgdir)
            avgspaces.append(avgspace)
            if timer != round(captures-(i/10)):
                timer = round(captures-(i/10))
                if printit:
                    print(str(timer))
                if gui != None:
                    gui.config(text=str(timer))
                    root.update_idletasks()
                    root.update()
        self.imgs = np.expand_dims(np.array(imgs), axis=3)
        avgdirz = []
        for i in avgdirs:
            avgdirz.append((round((i*10)))/10)
        self.avgdirs = []
        for i, j in zip(avgdirz, avgspaces):
            self.avgdirs.append(np.concatenate((getdummy(i), getbindummy(j))))
        if printit:
            print('captured data')

    def model(self, load, n_epoch=0):
        self.model = alexnet(72, 128, 0.01, 13)

        if load != 'y':
            if n_epoch >= 1:
                self.train(n_epoch)
            else:
                self.savemodel()
        else:
            self.model.load('%s.tfl' % self.modelname)

    def train(self, n_epoch):
        try:
            a = int(n_epoch)
        except ValueError as e:
            print(e)
        if self.imgs == [] and self.avgdirs == []:
            print("Can't train on nothing!")
        elif a != n_epoch:
            print("Number of epochs is not int!")
        else:
            self.model.fit(self.imgs, self.avgdirs, n_epoch, batch_size=100, show_metric=True)
            self.savemodel()

    def savemodel(self):
        self.model.save('%s.tfl' % self.modelname)

    def control(self, showcv=False):
        if not self.pause and self.ff.capavailable():
            imgs = []
            self.img, avgdir, avgspace = self.ff.getcap()
            if showcv:
                self.ff.show(self.img)
            imgs.append(self.img)
            imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
            pred = self.model.predict(imgs)
            pred = pred.flatten()
            preddir = pred[:11]
            predspace = pred[11:]
            actpreddir = (getmaxpos(preddir)/10)
            actpredspace = getmaxpos(predspace)
            # print(str(actpreddir), str(actpredspace))
            # if time.time()-start < 100: 
            CircleFunc.setmouse(actpreddir)
            if actpredspace:
                pyautogui.keyDown('space')
            else:
                pyautogui.keyUp('space')
        if keyboard.is_pressed('p'):#if key 'p' is pressed
            if self.start == True or time.time()-self.start > 2.5:
                self.start = time.time()
                self.pause = not self.pause
                if self.pause:
                    print('paused')

if __name__ == '__main__':
    captures = int(input('How many seconds of capture? '))
    modelname = input('Name of model? ')
    dt = deeptool(captures, modelname)
    dt.model('y', 100)
    while True:
        dt.control(True)






