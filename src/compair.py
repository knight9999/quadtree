import numpy as np
import math
import itertools as it
import cv2
import time
import morton
import square
import quadtree


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
SQUARE_WIDTH = 10
SQUARE_HEIGHT = 10
SQUARE_MIN_WIDTH = 10
SQUARE_MIN_HEIGHT = 10
OBJ_NUM = 200
LVL = 3  # 3 for 4x4  4 for 8x8  5 for 16x16

list = np.array([square.Square(
    x*CANVAS_WIDTH,
    y*CANVAS_HEIGHT,
    w*SQUARE_WIDTH+SQUARE_MIN_WIDTH,
    h*SQUARE_HEIGHT+SQUARE_MIN_HEIGHT) for x,y,w,h in np.random.rand(OBJ_NUM,4) ] )

# Naive

def calcNaive():
    print "Naive"
    image = np.zeros( (CANVAS_WIDTH, CANVAS_HEIGHT, 3) , np.uint8)
    for s in list:
        s.draw(image,(0,0,255))

    start = time.time()
    pairs = square.getPairs(CANVAS_WIDTH,CANVAS_HEIGHT,list)
    interval = time.time() - start
    print "time:{0}[sec]".format(interval)

    print "pairs = " + str(len(pairs))

    for (s,t) in pairs:
        s.draw(image,(0,255,0))
        t.draw(image,(0,255,0))

    cv2.imwrite('result0.png',image)


# Quadtree with lvl

def calcQuadtree(lvl):
    print "Quadtree " + str(lvl)
    image = np.zeros( (CANVAS_WIDTH, CANVAS_HEIGHT, 3) , np.uint8)
    for s in list:
        s.draw(image,(0,0,255))

    start = time.time()
    pairs = quadtree.getPairs(lvl,CANVAS_WIDTH,CANVAS_HEIGHT,list)
    interval = time.time() - start
    print "time:{0}[sec]".format(interval)

    print "pairs = " + str(len(pairs))

    for (s,t) in pairs:
        s.draw(image,(0,255,0))
        t.draw(image,(0,255,0))

    cv2.imwrite('result' + str(lvl) + '.png',image)


calcNaive()
calcQuadtree(1)
calcQuadtree(2)
calcQuadtree(3)
calcQuadtree(4)
