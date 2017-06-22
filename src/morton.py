import numpy as np
import math

def sheet(lvl):  # shift_filter
  print "bit num " + str(lvl-1)
  n = int( math.ceil( math.log(lvl-1) / math.log(2) ) )
  print "n = " + str(n)


  vmax = 2 * (2**n)
  arr = []
  for l in range(0, n+ 1):
    c = 0
    f = 0
    m = 2 ** (n-l)
    list = np.array([0]*vmax)
    for i in range(0,vmax):
      list[i] = 0 if f == 0 else 1
      c = c + 1
      if c >= m:
          c = 0
          f = 1 - f
    arr.append( list )
#  arr = [ np.array([0]*vmax) for i in range(0,lvl-1)]
  return arr

sheets = sheet(4)

def show(arr):
  for l in arr:
    print l

show(sheets)
