import numpy as np
import math


class Morton(object):
    def __init__(self,lvl):
        self.lvl = lvl
        self.filters = None

    def getMax(self):
        return 2 ** (self.lvl-1) # TODO Cache

    def getCanonicalValue(self,x):
        return int( math.ceil( x * self.getMax() ) )

    def getCalcBitLength(self):
        n = int( math.ceil( math.log(self.lvl-1,2) ) )  # TODO Cache
        return 2 ** n

    def getFiltersLength(self):
        return int( math.log( self.getCalcBitLength() , 2 ) ) # TODO Cache

    def getFilterLength(self):
        return 2 * self.getCalcBitLength()  # TODO Cache

    def getFilters(self):
        if self.filters is None:
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

    def getMortonCoodinateFromCanonicalCoodinate(self,cx,cy):
        mx = self.getEveryOtherBitValue(cx)
        my = self.getEveryOtherBitValue(cy)
        mc = mx | my << 1
        return mc

    def getMortonCoodinate(self,x,y):  # x in [0,1), y in [0,1)
        cx = self.getCanonicalValue(x)
        cy = self.getCanonicalValue(y)
        return self.getMortonCoodinateFromCanonicalCoodinate(cx,cy)

    def getObjectLvlAndObjectCooridnate(self,mc1,mc2):
        v = mc1 ^ mc2
        n = 0
        for l in range(0,self.lvl-1):
            x = v & 3
            if x != 0:
                n = l
            x = x >> 2
        print "n = " + str(n)
        lvl = self.lvl-1 - n
        mc = mc1 >> (2 * n)
        return (lvl,mc)

    def filterFormat(self):
        filLen = self.getFilterLength()
        return '0' + str(filLen) + 'b'

    def show(self):
        for fil in filters:
            print format(fil,self.filterFormat())


morton = Morton(4)

(x1,y1) = (3.0/8.0,6.0/8.0)
print "x1 = " + str(x1)
print "y1 = " + str(y1)
mc = morton.getMortonCoodinate(x1,y1)
print format(mc, morton.filterFormat() )
print mc

(x2,y2) = (6.0/8.0,4.0/8.0)
print "x2 = " + str(x2)
print "y2 = " + str(y2)
mc2 = morton.getMortonCoodinate(x2,y2)
print format(mc2, morton.filterFormat() )
print mc2

(x3,y3) = (7.0/8.0,6.0/8.0)
print "x3 = " + str(x3)
print "y3 = " + str(y3)
mc3 = morton.getMortonCoodinate(x3,y3)
print format(mc3, morton.filterFormat() )
print mc3

(lvl,mc) = morton.getObjectLvlAndObjectCooridnate(mc2,mc3)

print lvl
print mc
