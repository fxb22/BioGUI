import numpy
import math
import Catche
import os

def getMedPol(valMat):
    valMat = numpy.array(valMat)
    im = 0
    while im < len(valMat):
        jm = 0
        while jm < len(valMat[0]):
            valMat[im][jm] = math.log(valMat[im][jm],2)
            jm += 1
        im += 1
    iters = 0
    rowFx = numpy.zeros(len(valMat[0]))
    colFx = numpy.zeros(len(valMat))
    rowMed = numpy.median(valMat,axis=0)
    while iters < 10:
        idk = 0
        while idk < len(rowMed):
            jk = 0
            while jk < len(valMat):
                valMat[jk][idk] -= rowMed[idk]
                jk += 1
            rowFx[idk] += rowMed[idk]
            idk += 1

        colMed = numpy.median(valMat,axis = 1)
        idk = 0
        while idk < len(colMed):
            jk = 0
            while jk < len(valMat[0]):
                valMat[idk][jk] -= colMed[idk]
                jk += 1
            colFx[idk] += colMed[idk]
            idk += 1
        rowMed = numpy.median(valMat,axis=0)
        colMed = numpy.median(valMat,axis = 1)
        stopper = True
        for r in rowMed:
            if abs(r) > 0.01:
                stopper = False
        for c in colMed:
            if abs(c) > 0.01:
                stopper = False
        if stopper:
           iters = 10
        iters += 1
            
    temp = numpy.median(rowFx)
    ret = []
    for c in colFx:
        ret.append(c + temp)
    return ret

names = []
geoMat = []
Xes = os.listdir(r'.\Gene Expressions\CurrentCel')
for x in Xes:
    if x[-7:] == r'.CEL.gz':
        names.append(x[:-7])
        geoMat.append([x[:-7]])
i = 0
ProbeSet = Catche.opickle(r'.\Gene Expressions\CurrentCel/ProbeSets.pickle')
rollingSum = 0
valMat = []
for n in names:
    valMat.append(Catche.opickle(r'.\Gene Expressions\CurrentCel\RMAPreSum' + n + r'.pickle'))
print 'begin sum'
while i < len(ProbeSet):
    print i
    rHoMat = []
    for n,na in enumerate(names):
        k = rollingSum
        rHoMat.append([])
        while k < ProbeSet[i][1]:
            rHoMat[-1].append(valMat[n][k])
            k += 1
    temp = getMedPol(rHoMat)
    for n,na in enumerate(names):
        if na == geoMat[n][0]:
            geoMat[n].append(temp[n])
        else:
            print '??????????????????????????????'
    rollingSum = ProbeSet[i][1]
    i += 1
print 'done rmaSum'

geoMat.append([])
for pname in ProbeSet:
    geoMat[-1].append(pname[0])
Catche.spickle(r'.\Gene Expressions\CurrentCel/RMAFinal.pickle',geoMat)

        
