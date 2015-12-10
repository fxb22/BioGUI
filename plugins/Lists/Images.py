import os
import errno

from Bio import SeqIO

#List View Plugin for a folder containing protein objects
def GetExec():
    Recs = os.listdir(os.getcwd())     
    newList=[]
    j = 0
    listdata=dict()
    k = 0
    while k < len(Recs):
        try:
            (name, ext) = os.path.splitext(Recs[k])
            if ext=='.txt':
                2+2
            else:
                newList.append([Recs[k],Recs[k]])
                listdata[j]=Recs[k],Recs[k]
                j+=1         
        except IOError, e:
            print e
        k += 1

    return [newList,listdata]

        
