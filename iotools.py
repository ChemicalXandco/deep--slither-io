import screenfunctions, cv2, time, math, pyautogui
# import turtletest as tt

sf = screenfunctions.ScreenFunc()

class CircleFunc:
    def getdir(x1, y1, x2, y2):
        raw = math.atan2(y2-y1,x2-x1)
        # print(str(raw))
        raw += math.pi
        alt = (raw/math.pi)/2
        alt += 0.25
        if alt > 1:
            alt = alt-1
        # print(str(alt))
        return alt

    def getcoords(bindir, rad):
        actdir = ((2*(((bindir*-1)+1)*math.pi))-math.pi)#+(math.pi/4)
        # print(str(actdir))
        return ((rad*math.sin(actdir)), (rad*math.cos(actdir)))

    def setmouse(direction, radius=100):
        retco = CircleFunc.getcoords(direction, radius)
        pyautogui.moveTo((retco[0]+960), (retco[1]+540))
    
class FrameFunc:
    def __init__(self):
        sf = screenfunctions.ScreenFunc()

    def waituntil(self, start, length, capact=True):
        rec = []
        while time.time()-start < length:
            # k = cv2.waitKey(10) & 0xff
            if capact:
                x, y = pyautogui.position()
                rec.append(CircleFunc.getdir(x, y, 960, 540))
            else:
                pass
            '''
            if k == 27:
                raise KeyError('quit key has been pressed')
                break
            '''
        if capact:
            recavg = sum(rec)/len(rec)
            return recavg
        else:
            return None

    def getcap(self, framelen=0.1, capact=True):
        start = time.time()

        cap = cv2.resize(sf.get_screen(sf.resRight),(128, 72), interpolation = cv2.INTER_LINEAR)
        img = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)/255
        # cap = cv2.resize(cap,(1280, 720), interpolation = cv2.INTER_LINEAR)

        # print(str(time.time()-start))

        avgdir = self.waituntil(start, framelen, capact)

        # print(str(time.time()-start))
        # print(sorted(img.flatten()))

        return (img, avgdir)

if __name__ == '__main__':
    '''
    for i in range(100):
        print(str(i/100))
        retco = CircleFunc.getcoords(i/100, 100)
        pyautogui.moveTo((retco[0]+960), (retco[1]+540))
        x, y = pyautogui.position()
        diry = CircleFunc.getdir(x, y, 960, 540)
        print(str(diry))
    '''

    '''
    while True:
        x, y = pyautogui.position()

        diry = CircleFunc.getdir(x, y, 960, 540)
        retco = CircleFunc.getcoords(diry, 50)

        # tt.point(retco)
        
        print(str(diry),str(retco))
    '''
    # ff = FrameFunc()
    # cv2.imshow('cap',ff.getcap())
    # cv2.waitKey(1)

    start = time.time()

    rec = []
    while time.time()-start < 10:
        starty = time.time()
        x, y = pyautogui.position()
        rec.append(CircleFunc.getdir(x, y, 960, 540))
        while time.time()-starty < 0.1:
            pass

    if len(rec) < 102:
        for item in rec:
            retco = CircleFunc.getcoords(item, 100)
            pyautogui.moveTo((retco[0]+960), (retco[1]+540))
    else:
        print('rec too long: '+str(len(rec)))
    

    


