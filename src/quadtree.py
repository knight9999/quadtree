# -*- coding: utf-8 -*-

import numpy as np
import math
import itertools as it
import cv2
import time
import morton
import square


def test1():
    m = morton.Morton(4)

    (x1,y1) = (3.0/8.0,4.0/8.0)
    (x2,y2) = (2.0/8.0,5.0/8.0)
    mc1 = m.getMortonCoordinate(x1,y1)
    mc2 = m.getMortonCoordinate(x2,y2)

    print format(mc1,m.filterFormat())
    print format(mc2,m.filterFormat())


    (lvl,mc) = m.getObjectLvlAndObjectCoordinate(mc1,mc2)

    print lvl
    print mc

def test2():
    COLS = 400
    ROWS = 400
    WIDTH = 10
    HEIGHT = 10
    MIN_WIDTH = 10
    MIN_HEIGHT = 10
    OBJ_NUM = 100
    LVL = 3  # 3 for 4x4  4 for 8x8  5 for 16x16

    list = np.array([square.Square(
        x*COLS,
        y*ROWS,
        w*WIDTH+MIN_WIDTH,
        h*HEIGHT+MIN_HEIGHT) for x,y,w,h in np.random.rand(OBJ_NUM,4) ] )

    image = np.zeros( (ROWS, COLS, 3) , np.uint8)
    for s in list:
        s.draw(image,(0,0,255))

    m = morton.Morton(5)

    indexMax = m.getObjectLinearIndexMax()
    spaceList = [ [] for i in range(indexMax) ]
    # print "indexMax " + str( indexMax )
    # print "len = " + str( len( spaceList )  )


    # spaceListに、Squareを格納していく
    for s in list:
        x1 = float( s.left() ) / COLS
        x2 = float( s.right() ) / COLS
        y1 = float( s.top() ) / ROWS
        y2 = float( s.bottom() ) / ROWS
        # print "(" + str(x1) + "," + str(y1) + ")   (" + str(x2) + "," + str(y2) + ")"
        # print "(" + str( m.getCellValue(x1) ) + "," + \
        #       str( m.getCellValue(y1) ) + ")   (" + \
        #       str( m.getCellValue(x2) ) + ", " + \
        #       str( m.getCellValue(y2) ) + ")"
        mc1 = m.getMortonCoordinate(x1,y1)
        mc2 = m.getMortonCoordinate(x2,y2)
        i = m.getObjectLinearIndex(mc1,mc2)
        # print i
        spaceList[i].append( s )

    # for i, v in enumerate( spaceList ):
    #     print "spc[" + str(i) + "] = " + str( len(v) )


    # すべてのループさせていく
    maxlvl = m.lvl - 1
    lvl = 0
    mc = 0
    stack = []
    pair = []

    while True:
        idx = (4**lvl - 1) / 3 + mc
#        print "idx:" + str(idx)

        mlist = spaceList[idx]

        for (s,t) in it.combinations( mlist , 2 ):
            if (s.collide(t)):
                pair.append( (s,t) )
                s.draw(image,(0,255,0))
                t.draw(image,(0,255,0))

        # TODO stackとmlistの中での衝突をチェック
        for s in mlist:
            for sublist in stack:
                for t in sublist:
                    if (s.collide(t)):
                        pair.append( (s,t) )
                        s.draw(image,(0,255,0))
                        t.draw(image,(0,255,0))

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

    cv2.imwrite('result.png',image)

start = time.time()
test2()
interval = time.time() - start
print "time:{0}[sec]".format(interval)
