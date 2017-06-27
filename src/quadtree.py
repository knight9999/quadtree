# -*- coding: utf-8 -*-

import numpy as np
import math
import itertools as it
import cv2
import time
import morton
import square

def getPairs(lvl,width,height,list):

    m = morton.Morton(lvl)

    indexMax = m.getObjectLinearIndexMax()
    spaceList = [ [] for i in range(indexMax) ]

    # spaceListに、Squareを格納していく
    for s in list:
        x1 = float( s.left() ) / width
        x2 = float( s.right() ) / width
        y1 = float( s.top() ) / height
        y2 = float( s.bottom() ) / height
        mc1 = m.getMortonCoordinate(x1,y1)
        mc2 = m.getMortonCoordinate(x2,y2)
        i = m.getObjectLinearIndex(mc1,mc2)
        spaceList[i].append( s )

    # すべてのループさせていく
    maxlvl = m.lvl - 1
    lvl = 0
    mc = 0
    stack = []
    pairs = []

    while True:
        idx = (4**lvl - 1) / 3 + mc

        mlist = spaceList[idx]

        # mlistの中での衝突をチェック
        for (s,t) in it.combinations( mlist , 2 ):
            if (s.collide(t)):
                pairs.append( (s,t) )

        # stackとmlistの中での衝突をチェック
        for s in mlist:
            for sublist in stack:
                for t in sublist:
                    if (s.collide(t)):
                        pairs.append( (s,t) )

        if lvl < maxlvl:
            stack.append( mlist )
            lvl = lvl + 1
            mc = mc << 2
        else:
            while (mc & 3) == 3:
                stack.pop()
                lvl = lvl - 1
                mc = mc >> 2
            if lvl == 0:
                break
            mc += 1

    return pairs



##############################################################
# For Debug
##############################################################

if __name__ == '__main__':
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

    # Quadtree

    image = np.zeros( (CANVAS_WIDTH, CANVAS_HEIGHT, 3) , np.uint8)
    for s in list:
        s.draw(image,(0,0,255))

    start = time.time()
    pairs = getPairs(LVL,CANVAS_WIDTH,CANVAS_HEIGHT,list)
    interval = time.time() - start
    print "time:{0}[sec]".format(interval)

    print "pairs = " + str(len(pairs))

    for (s,t) in pairs:
        s.draw(image,(0,255,0))
        t.draw(image,(0,255,0))

    cv2.imwrite('result3.png',image)
