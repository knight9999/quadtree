import numpy as np
import math


# def getMinCalcBitLength(lvl):
#   n = int( math.ceil( math.log(lvl-1,2) ) )
#   return n

def getCalcBitLength(lvl):
  n = int( math.ceil( math.log(lvl-1,2) ) )
  return 2**n

def getFiltersLength(lvl):
  return int( math.log( getCalcBitLength(lvl) , 2 ) )

def getFilterLength(lvl):
  return 2 * getCalcBitLength(lvl)

def getFilters(lvl):  # shift_filter
  print "level = " + str(lvl)
  print "bit length = " + str(lvl-1)
  cbLen = getCalcBitLength(lvl)
  print "calc bit length = " + str(cbLen)
  filLen = getFilterLength(lvl)
  print "filter length (columns) = " + str(filLen)
  filsLen = getFiltersLength(lvl)
  print "filters length (rows) = " + str(filsLen)

  arr = []
  for l in range(1, filsLen + 1):
    c = 0  # counter
    f = False  # flag
    m = 2 ** (filsLen - l)  # part of filter length
    fil = 0
    for i in range(0,filLen):
      fil = fil << 1
      fil += 0 if f == False else 1
      c = c + 1
      if c >= m:
          c = 0
          f = not f
    arr.append( fil )
  return arr


def getEveryOtherBitValue(x,lvl):
  cbLen = getCalcBitLength(lvl)
  filters = getFilters(lvl)
  bitShift = cbLen / 2
  v = x
  for i in range(0,len(filters)):
      v = (v << bitShift | v) & filters[i]
      bitShift = bitShift / 2
  return v


lvl = 5

filters = getFilters(lvl)

def show( filters , lvl ):
  filLen = getFilterLength(lvl)
  for fil in filters:
    print format(fil,'0' + str(filLen) + 'b')

show( filters , lvl )


filLen = getFilterLength(lvl)

x = 9
v = getEveryOtherBitValue(x,lvl)

print format(x,'0' + str(filLen) + 'b')
print format(v,'0' + str(filLen) + 'b')
