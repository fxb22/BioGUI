import Catche
import os

def countSort(xe):

    names = []    
    Xes = os.listdir(r'.\Gene Expressions\CurrentCel')
    out = [[0]]
    for x in Xes:
        if x[-7:] == r'.CEL.gz':
            names.append(x[:-7])
            
    arrayX = Catche.opickle(r'.\Gene Expressions\CurrentCel/BAIntense'+names[xe]+r'.pickle')
    counter = []
    final = []
    ranker = []
    finRank = []
    i = 0
    while i < len(arrayX):
        counter.append(0)
        final.append(0)
        ranker.append([])
        finRank.append(0)
        i += 1
    
    for j,val in enumerate(arrayX):
        counter[int(val)] += 1
        ranker[int(val)].append(j)

    preSum = []
    preSum.append(0)
    i = 0
    while i < len(arrayX) - 1:
        preSum.append(preSum[i] + counter[i])
        i += 1
    i = len(counter) - 1
    while i >= 0:
        while counter[i] > 0:
            final[preSum[i]] = i
            finRank[preSum[i]] = ranker[i][-1]
            preSum[i] += 1            
            del ranker[i][-1]
            counter[i] -= 1
        i -= 1

    Catche.spickle(r'.\GeneExpressions\CurrentCel/SortAndRank'+names[xe]+r'.pickle',[final,finRank])
