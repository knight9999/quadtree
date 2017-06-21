import cv2
import numpy as np

COLS = 400
ROWS = 400
WIDTH = 10
HEIGHT = 10
MIN_WIDTH = 10
MIN_HEIGHT = 10
MARGIN = 4

class Square(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def message(self):
        return "(" + str(self.x) + "," + str(self.y) + ")" \
                + "  w:" + str(self.w) + " h:" + str(self.h)
    def left(self):
        return int(self.x-self.w/2)
    def top(self):
        return int(self.y-self.h/2)
    def right(self):
        return int(self.x+self.w/2)
    def bottom(self):
        return int(self.y+self.h/2)
    def collide(self,object):
        (minx,maxx) = (self.x,object.x) if self.x < object.x else (object.x,self.x)
        (miny,maxy) = (self.y,object.y) if self.y < object.y else (object.y,self.y)
        if maxx-minx < self.w/2 + object.w/2 + MARGIN :
            if maxy-miny < self.h/2 + object.h/2 + MARGIN :
                return True
        return False
    def draw(self,image,color):
        cv2.rectangle(image,(self.left(),self.top()),(self.right(),self.bottom()),color,3)


list = np.array([Square(x*COLS,y*ROWS,w*WIDTH+MIN_WIDTH,h*HEIGHT+MIN_HEIGHT) for x,y,w,h in np.random.rand(40,4) ] )

# for s in list:
#    print s.message()


image = np.zeros( (ROWS, COLS, 3) , np.uint8)
for s in list:
    s.draw(image,(0,0,255))
#    cv2.rectangle(image,(s.left(),s.top()),(s.right(),s.bottom()),(0,0,255),3)


for s in list:
    for t in list:
        if s != t and s.collide(t):
            print s.message()
            s.draw(image,(0,255,0))

cv2.imwrite('result.png',image)
