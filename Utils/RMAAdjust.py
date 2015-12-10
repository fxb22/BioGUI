import math
import os
import Catche
import sys
from multiprocessing import Pool

def adjust(iters):
    Xes = os.listdir(r'.\Gene Expressions\CurrentCel')
    names = []
    for x in Xes:
        if x[-7:] == r'.CEL.gz':
            names.append(x[:-7])
        
    geoMat = Catche.opickle(r'.\Gene Expressions\CurrentCel\PMIntense'+names[iters]+r'.pickle')
    sigma = 0
    alpha = 0
    a = []
    y = []
    vector = []

    for row in geoMat:
        vector.append(row)


    #print vector[1]
    #print i
    m1 = mode(vector)
    m2 = mode(leftOf(vector,m1))
        
    #estimate sigma?
    #find elements in dataO less than mu. group in leftz
    leftZ = leftOf(vector,m2)
    n = len(leftZ)
    zSum = 0
    for lZ in leftZ:
        zSum += (lZ - m2) ** 2
    if n > 1:
        sigma = math.sqrt( zSum / (n - 1)) * math.sqrt(2.0)
    else:
        sigma = math.sqrt(zSum) * math.sqrt(2.0)
        

        #estimate alpha
        #find elements in dataO greater than mu. store in rightz. rightz - mu for all
        #find mode of rightz
        
    alpha = 1 / mode(rightOf(vector,m2))
    for j,val in enumerate(vector):
        a.append(val - m2 - alpha * (sigma ** 2))
    print 'pass 1'
    for val in a:
        if sigma == 0:
            y.append(1)
        elif normcdf(val / sigma) == 0:
            y.append(2)
        else:
            y.append(val + sigma * normpdf(val / sigma) / normcdf(val / sigma))
    print 'pass 2'

    for i,col in enumerate(y):
        geoMat[i] = col

    print 'pass 3'
    Catche.spickle(r'.\Gene Expressions\CurrentCel/BAIntense'+names[iters]+r'.pickle',geoMat)
    

def mode(inMat):
    iMin = 1000000
    iMax = 0
    for val in inMat:
        if val < iMin:
            iMin = val
        if val > iMax:
            iMax = val
    #print iMin,iMax
    n = (iMax - iMin) / 2000.

    i = 0
    counter = []
    while i <= 2000:
        counter.append(0)
        i += 1
        
    for val in inMat:
        pos = int(int(val - iMin) / n)
        counter[pos] += 1

    i = 0
    count = 0
    countPos = -1
    while i < len(counter):
        if counter[i] > count:
            count = counter[i]
            countPos = i
        i += 1
    if countPos <= 1:
        countPos = 2
    #print (countPos) * n + iMin
    return (countPos - 0.5) * n + iMin
    
def leftOf(vect, num):
    retList = []
    for vecs in vect:
        if vecs <= num:
            retList.append(vecs)
    return retList                     

def rightOf(vect, num):
    retList = []
    for vec in vect:
        if vec >= num:
            retList.append(vec - num)
    return retList

def normpdf(x):
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def normcdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))



Xes = os.listdir(r'.\Gene Expressions\CurrentCel')
lenX = 0
for x in Xes:
    if x[-7:] == r'.CEL.gz':
        lenX +=1

iters = 0
print 'Into adjust'
if __name__ == '__main__':
    sortedVals = []
    rankerVals = []
    out = []
    pool = Pool(processes=3)
    i=0
    while i < lenX-2:
        print i
        pods = [i,i+1,i+2]
        pool.map(adjust,pods)
        i+=3
    diff = lenX - i
    baggage = []
    if diff > 0:
        while diff > 0:
            baggage.append(i)
            i += 1
            diff -= 1
        pool.map(adjust,baggage)


