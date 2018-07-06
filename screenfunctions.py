import numpy as np 
import cv2
import platform
if platform.system() == 'Linux':
    import pyscreenshot as ImageGrab
else:
    from PIL import ImageGrab

class ScreenFunc:
    def __init__(self):
        self.np = np
        global resRight
        img = ImageGrab.grab()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        # frame = cv2.resize(frame,(1280, 720), interpolation = cv2.INTER_LINEAR)
        if frame.shape != (1080, 1920, 3):
            from fractions import gcd
            from functools import reduce
            ratios = [(frame.shape)[1], (frame.shape)[0]]
            if list(map(reduce(gcd, ratios).__rfloordiv__, ratios)) == [16, 9]:
                self.resRight = False
                print('screen resolution is not 1080p but is 16:9 so it might work')
            else:
                print('screen resolution is not 1080p or 16:9 so it will not work')
        else:
            self.resRight = True
        # resRight = False
        self.screenavailable = True

    def imcrop(self, img, bbox): 
        x1,y1,x2,y2 = bbox
        if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
            img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
        return img[y1:y2, x1:x2, :]

    def pad_img_to_fit_bbox(self, img, x1, x2, y1, y2):
        img = np.pad(img, ((np.abs(np.minimum(0, y1)), np.maximum(y2 - img.shape[0], 0)),
                        (np.abs(np.minimum(0, x1)), np.maximum(x2 - img.shape[1], 0)), (0,0)), mode="constant")
        y1 += np.abs(np.minimum(0, y1))
        y2 += np.abs(np.minimum(0, y1))
        x1 += np.abs(np.minimum(0, x1))
        x2 += np.abs(np.minimum(0, x1))
        return img, x1, x2, y1, y2

    def get_screen(self, resRight):
        try:
            img = ImageGrab.grab()
            img_np = np.array(img)
            if resRight == True:
                return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB) 
            else:
                return cv2.resize((cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)),(1920, 1080), interpolation = cv2.INTER_LINEAR)
            if self.screenavailable == False:
                self.screenavailable = True
                print('screen capture regained')
        except OSError as e:
            if self.screenavailable == True:
                self.screenavailable = False
                print('could not get screenshot - %s' % e)
            return None

# if __name__ == "__main__":
    # start()

# cv2.destroyAllWindows()
