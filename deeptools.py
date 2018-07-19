from iotools import *
from dummytools import *
import numpy as np
import time, keyboard, pyautogui
from alexnet import alexnet

# gather data
ff = FrameFunc()

time.sleep(5)

imgs = []
avgdirs = []
avgspaces = []
k = None
captures = int(input('How many seconds of capture? '))
modelname = input('Name of model? ')
print('\ncapturing data')
for i in range(captures*10):
    img, avgdir, avgspace = ff.getcap()
    imgs.append(img)
    avgdirs.append(avgdir)
    avgspaces.append(avgspace)
imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
avgdirz = []
for i in avgdirs:
    avgdirz.append((round((i*10)))/10)
# avgdirs = np.expand_dims(np.array(avgdirz), axis=1)#.astype('float32')
avgdirs = []
for i, j in zip(avgdirz, avgspaces):
    avgdirs.append(np.concatenate((getdummy(i), getbindummy(j))))
# print(str(avgdirs))

# quit()

print('captured data')

model = alexnet(72, 128, 0.01, 13)

if input('Load pretrained model? ') != 'y':
    # Training
    model.fit(imgs, avgdirs, n_epoch=100, batch_size=100, show_metric=True)
    model.save('%s.tfl' % modelname)
else:
    model.load('%s.tfl' % modelname)

start = True # time.time()
pause = False

while True:
    if not pause and ff.capavailable():
        imgs = []
        img, avgdir, avgspace = ff.getcap()
        ff.show(img)
        imgs.append(img)
        imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
        pred = model.predict(imgs)
        pred = pred.flatten()
        preddir = pred[:11]
        predspace = pred[11:]
        actpreddir = (getmaxpos(preddir)/10)
        actpredspace = getmaxpos(predspace)
        print(str(actpreddir), str(actpredspace))
        # if time.time()-start < 100: 
        CircleFunc.setmouse(actpreddir)
        if actpredspace:
            pyautogui.keyDown('space')
        else:
            pyautogui.keyUp('space')
    if keyboard.is_pressed('p'):#if key 'p' is pressed
        if start == True or time.time()-start > 2.5:
            start = time.time()
            pause = not pause
            if pause:
                print('paused')
        





