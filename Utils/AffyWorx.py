import CelFileReader
import gzip
import os
import cdfParser
import Catche
from multiprocessing import Pool
import sys
import numpy as nP


#This is a very ugly hack...
#Sooo very ugly...
#Abe Lincoln ugly...
#If anyone can rewrite this to perform the multiprocessing in a better way,
#I'd be much obliged.


def funccall(x):
    bogus = os.listdir(r'.\Gene Expressions\CurrentCel')
    names = []
    for bug in bogus:
        if bug[-7:]=='.CEL.gz':
            names.append(bug)
    h = gzip.GzipFile(r'.\Gene Expressions\CurrentCel/'+names[x])
    b = CelFileReader.read(h)
    g=b.intensities
    PMIntense = []
    PMLoc = Catche.opickle(r'.\Gene Expressions\CurrentCel/PMLoc.pickle')
    for loc in PMLoc:
        PMIntense.append(g[loc[1]][loc[0]])
    Catche.spickle(r'.\Gene Expressions\CurrentCel/PMIntense' + names[x][:-7] + r'.pickle',PMIntense)
    return x

def worx(platform):
    bogus = os.listdir(r'.\Gene Expressions\CurrentCel')
    names = []
    for bug in bogus:
        if bug[-7:]=='.CEL.gz':
            names.append(bug)
    platPath = ''
    try:
        pforms = os.listdir(r'.\Gene Expressions\GPL')
        i = 0
        while i < len(pforms):
            if pforms[i][:-4] == platform:
                platPath = r'.\Gene Expressions\GPL/' + pforms[i]
                i = len(pforms)
            i += 1
    except:
        errno
    cdfP = cdfParser.cdfParse()
    print 'Reading .CDF file:',platform,r'...'
    cdfP.parse(platPath)
    print 'Done'
    PMLoc = cdfP.getPMLocs()
    Catche.spickle(r'.\Gene Expressions\CurrentCel/PMLoc.pickle',PMLoc)
    Catche.spickle(r'.\Gene Expressions\CurrentCel/ProbeSets.pickle',cdfP.getProbeSets())

if __name__ == '__main__':
    bogus = os.listdir(r'.\Gene Expressions\CurrentCel')
    names = []
    for bug in bogus:
        if bug[-7:]=='.CEL.gz':
            names.append(bug)
    pool = Pool(processes=3)               # start 3 worker processes
    i=0
    while i < len(names)-2:
        print 'Reading .CEL files: ',names[i],names[i+1],names[i+2],'...'
        dummy = pool.map(funccall, [i,i+1,i+2,])         # prints "[0, 1, 4,..., 81]"
        print 'Done'
        i+=3
    diff = len(names) - i
    baggage = []
    if diff > 0:
        prntTxt = 'Reading .CEL files: '
        while diff > 0:
            baggage.append(i)
            i += 1
            diff -= 1
            prntTxt += names[i]+' '
        print prntTxt,r'...'
        dummy = pool.map(funccall,baggage)
        print 'Done'

