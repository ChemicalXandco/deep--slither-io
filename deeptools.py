from iotools import *
from dummytools import *
import numpy as np
import pandas as pd
import time
from alexnet import alexnet

dummy = np.array(pd.get_dummies([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]))

# gather data
ff = FrameFunc()

time.sleep(5)

imgs = []
avgdirs = []
k = None
captures = int(input('How many seconds of capture? '))
print('\ncapturing data')
for i in range(captures*10):
    img, avgdir = ff.getcap()
    imgs.append(img)
    avgdirs.append(avgdir)
imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
avgdirz = []
for i in avgdirs:
    avgdirz.append((round((i*10)))/10)
# avgdirs = np.expand_dims(np.array(avgdirz), axis=1)#.astype('float32')
avgdirs = []
for i in avgdirz:
    avgdirs.append(getdummy(i))
# print(str(avgdirs))

print('captured data')

model = alexnet(72, 128, 0.01, 11)

# Training
model.fit(imgs, avgdirs, n_epoch=100, batch_size=100, show_metric=True)

start = time.time()

while True:
    imgs = []
    img, avgdir = ff.getcap()
    imgs.append(img)
    imgs = np.expand_dims(np.array(imgs), axis=3)#.astype('float32')
    pred = model.predict(imgs)
    actpred = (getmaxpos(pred)/10)
    print(str(actpred))
    # if time.time()-start < 100:
    CircleFunc.setmouse(actpred)





