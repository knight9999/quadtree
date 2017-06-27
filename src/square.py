# -*- coding: utf-8 -*-

import cv2
import time
import numpy as np
import itertools as it

COLS = 500
ROWS = 500
WIDTH = 10
HEIGHT = 10
MIN_WIDTH = 10
MIN_HEIGHT = 10
OBJ_NUM = 200

class Square(object):
    def __init__(self, x, y, w, h):
        self.x = min( max( x , w / 2 ) , COLS - 1 - w/2 )
        self.y = min( max( y , h / 2 ) , ROWS - 1 - w/2 )
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
        if maxx-minx < self.w/2 + object.w/2 :
            if maxy-miny < self.h/2 + object.h/2 :
                return True
        return False
    def draw(self,image,color):
        cv2.rectangle(image,(self.left(),self.top()),(self.right(),self.bottom()),color,3)

def getPairs(width,height,list):

    pairs = []
    for (s,t) in it.combinations( list , 2 ):
        if (s.collide(t)):
            pairs.append( (s,t) )

    return pairs


##############################################################
# For Debug
##############################################################

if __name__ == '__main__':

    def test2():
        list = np.array([Square(x*COLS,y*ROWS,w*WIDTH+MIN_WIDTH,h*HEIGHT+MIN_HEIGHT) for x,y,w,h in np.random.rand(OBJ_NUM,4) ] )

        # for s in list:
        #    print s.message()


        image = np.zeros( (ROWS, COLS, 3) , np.uint8)
        for s in list:
            s.draw(image,(0,0,255))
        #    cv2.rectangle(image,(s.left(),s.top()),(s.right(),s.bottom()),(0,0,255),3)


        # for s in list:
        #     for t in list:
        #         if s != t and s.collide(t):
        #             print s.message()
        #             s.draw(image,(0,255,0))

        for (s,t) in it.combinations( list , 2 ):
            if (s.collide(t)):
                s.draw(image,(0,255,0))
                t.draw(image,(0,255,0))

        cv2.imwrite('result1.png',image)

    start = time.time()
    test2()
    interval = time.time() - start
    print "time:{0}[sec]".format(interval)
