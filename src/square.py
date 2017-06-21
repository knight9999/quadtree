import cv2
import numpy as np

class Square(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def message(self):
        return "(" + str(self.x) + "," + str(self.y) + ")" \
                + "  w:" + str(self.w) + " h:" + str(self.h)

list = np.array([Square(x*400,y*400,w*10+10,h*10+10) for x,y,w,h in np.random.rand(40,4) ] )

for s in list:
    print s.message()

cols = 400
rows = 400

image = np.zeros( (rows, cols, 3) , np.uint8)
for s in list:
    cv2.rectangle(image,(int(s.x-s.w/2),int(s.y-s.h/2)),\
    (int(s.x+s.w/2),int(s.y+s.h/2)),(0,0,255),3)

cv2.imwrite('result.png',image)
