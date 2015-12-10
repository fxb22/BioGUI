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
            
            if ext=='':
                2+2
            elif ext[0:4]==".fas":
                if name != "my_fasta":
                    seqIORec=list(SeqIO.parse(Recs[k],'fasta'))
                    for i,v in enumerate(seqIORec):
                        newList.append([v,v.id])
                        
                        listdata[j]=str(v.id),len(v),str(name)+str(ext)
                        j+=1
                    
        except IOError, e:
            print e

        k += 1

    return [newList,listdata]

        








            
