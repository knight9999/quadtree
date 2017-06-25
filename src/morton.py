# -*- coding: utf-8 -*-

import numpy as np
import math

class Morton(object):
    def __init__(self,lvl):
        self.lvl = lvl
        self.filters = None
        self.cellValueMax = 2 ** (self.lvl-1)
        self.filtersLength = int( math.ceil( math.log(self.lvl-1,2) ) )
        self.calcBitLength = 2 ** self.filtersLength
        self.filterLength = 2 * self.calcBitLength
        # calc filters
        cbLen = self.getCalcBitLength()
        filLen = self.getFilterLength()
        filsLen = self.getFiltersLength()
        # print "lvl : " + str(self.lvl)
        # print "cbLen : "+ str(cbLen)
        # print "filLen : "+ str(filLen)
        # print "filsLen : "+ str(filsLen)
        arr = []
        for l in range(1, filsLen + 1):
            c = 0
            f = False
            m = 2 ** (filsLen - l)
            fil = 0
            for i in range(0,filLen):
                fil = fil << 1
                fil += 0 if f == False else 1
                c = c + 1
                if c >= m:
                    c = 0
                    f = not f
            arr.append( fil )
        self.filters = arr

    def getCellValueMax(self):
        return self.cellValueMax

    def getCellValue(self,x):
        return int( math.floor( x * self.getCellValueMax() ) )

    def getCalcBitLength(self):
        return self.calcBitLength

    def getFiltersLength(self):
        return self.filtersLength

    def getFilterLength(self):
        return self.filterLength

    def getFilters(self):
        return self.filters

    def getEveryOtherBitValue(self,x):
        cbLen = self.getCalcBitLength()
        filters = self.getFilters()
        bitShift = cbLen / 2
        v = x
        for i in range(0,len(filters)):
            v = (v << bitShift | v) & filters[i]
            bitShift = bitShift / 2
        return v

    def getMortonCoordinateFromCanonicalCoodinate(self,cx,cy):
        mx = self.getEveryOtherBitValue(cx)
        my = self.getEveryOtherBitValue(cy)
        mc = mx | my << 1
        return mc

    def getMortonCoordinate(self,x,y):  # x in [0,1), y in [0,1)
        cx = self.getCellValue(x)
        cy = self.getCellValue(y)
        return self.getMortonCoordinateFromCanonicalCoodinate(cx,cy)

    def getObjectLvlAndObjectCoordinate(self,mc1,mc2):
        v = mc1 ^ mc2
        n = 0
        for l in range(0,self.lvl-1):
            x = v & 3
            if x != 0:
                n = l + 1
            v = v >> 2
        lvl = self.lvl-1 - n
        mc = mc1 >> (2 * n)
        return (lvl,mc)

    def getObjectLinearIndex(self,mc1,mc2):
        (lvl,mc) = self.getObjectLvlAndObjectCoordinate(mc1,mc2)
        oi = (4**lvl-1) / 3 + mc
        return oi

    def getObjectLinearIndexMax(self):
        return (4**self.lvl-1)/3

    def filterFormat(self):
        filLen = self.getFilterLength()
        return '0' + str(filLen) + 'b'

    def show(self):
        for fil in filters:
            print format(fil,self.filterFormat())

# class Node(object):
#     def __init__(self,mo):
#         self.mo = mo
#         self.next = None

if __name__ == '__main__':
    morton = Morton(4)

    (x1,y1) = (3.0/8.0,6.0/8.0)
    print "x1 = " + str(x1)
    print "y1 = " + str(y1)
    mc = morton.getMortonCoordinate(x1,y1)
    print format(mc, morton.filterFormat() )
    print mc

    (x2,y2) = (6.0/8.0,4.0/8.0)
    print "x2 = " + str(x2)
    print "y2 = " + str(y2)
    mc2 = morton.getMortonCoordinate(x2,y2)
    print format(mc2, morton.filterFormat() )
    print mc2

    (x3,y3) = (7.0/8.0,6.0/8.0)
    print "x3 = " + str(x3)
    print "y3 = " + str(y3)
    mc3 = morton.getMortonCoordinate(x3,y3)
    print format(mc3, morton.filterFormat() )
    print mc3

    (lvl,mc) = morton.getObjectLvlAndObjectCoordinate(mc2,mc3)

    print lvl
    print mc

    oi = (4**lvl-1) / 3 + mc

    print oi

    print morton.getObjectLinearIndex(mc2,mc3)

    print morton.getObjectLinearIndexMax()
