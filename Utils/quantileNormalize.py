import countSort as cS
import numpy as nP
import Catche
from multiprocessing import Pool
import os

if __name__ == '__main__':
    names = []    
    Xes = os.listdir(r'.\GeneExpressions\CurrentCel')
    lenX = 0
    out = [[0]]
    for x in Xes:
        if x[-7:] == r'.CEL.gz':
            names.append(x[:-7])
            lenX += 1
        
    sortedVals = []
    rankerVals = []
    pool = Pool(processes=3)
    i=0
    while i < lenX-2:
        print i
        pods = [i,i+1,i+2]
        pool.map(cS.countSort,pods)
        i+=3
    diff = lenX - i
    baggage = []
    if diff > 0:
        while diff > 0:
            baggage.append(i)
            i += 1
            diff -= 1
        pool.map(cS.countSort,baggage)

    i = 0
    while i < lenX:
        sorts = Catche.opickle(r'.\GeneExpressions\CurrentCel/SortAndRank' + names[i] + r'.pickle')
        sortedVals.append(sorts[0])
        rankerVals.append(sorts[1])
        print 'ranked and sorted'
        i += 1
    sortedVals = nP.array(sortedVals)
    meanVals = nP.mean(sortedVals, axis=0)
    for i,n in enumerate(names):
        out.append([])
        for mV in meanVals:
            out[i+1].append(0)
        for j,mV in enumerate(meanVals):
            out[i+1][rankerVals[i][j]] = mV
    print 'done qn'
        
    i = 0
    while i < lenX:
        Catche.spickle(r'.\GeneExpressions\CurrentCel/RMAPreSum' + names[i] + r'.pickle',out[i + 1])
        i += 1
    #print out[0][:5]
    #print out[1][:5]
    #print out[2][:5]
    #print out[-1][:5]
    #print out[0][:20]
    #return out
