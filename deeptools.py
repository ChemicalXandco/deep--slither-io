from iotools import *
from dummytools import *
import numpy as np
import time, keyboard, pyautogui
from alexnet import alexnet

class deeptool:
    def __init__(self, captures, modelname):
        self.ff = FrameFunc()
        # time.sleep(5)
        self.start = True # time.time()
        self.pause = False

        self.modelname = modelname
        imgs = []
        avgdirs = []
        avgspaces = []
        k = None
        print('\ncapturing data')
        for i in range(captures*10):
            img, avgdir, avgspace = self.ff.getcap()
            imgs.append(img)
            avgdirs.append(avgdir)
            avgspaces.append(avgspace)
        self.imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
        avgdirz = []
        for i in avgdirs:
            avgdirz.append((round((i*10)))/10)
        # avgdirs = np.expand_dims(np.array(avgdirz), axis=1)#.astype('float32')
        self.avgdirs = []
        for i, j in zip(avgdirz, avgspaces):
            self.avgdirs.append(np.concatenate((getdummy(i), getbindummy(j))))
        # print(str(avgdirs))
        # quit()

        print('captured data')

    def model(self, load, n_epoch=100):
        self.model = alexnet(72, 128, 0.01, 13)

        if load != 'y':
            # Training
            self.model.fit(self.imgs, self.avgdirs, n_epoch, batch_size=100, show_metric=True)
            self.model.save('%s.tfl' % self.modelname)
        else:
            self.model.load('%s.tfl' % self.modelname)

    def control(self):
        if not self.pause and self.ff.capavailable():
            imgs = []
            img, avgdir, avgspace = self.ff.getcap()
            self.ff.show(img)
            imgs.append(img)
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
    load = input('Load pretrained model? ')
    dt.model(load)
    while True:
        dt.control()






