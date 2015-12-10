import os
import errno
import time
from datetime import datetime
import filemtime as fmt
import Catche as mP
from Bio import SeqIO

def GetExec():
    Recs = os.listdir(os.getcwd())
    newList=[]
    j = 0

    listdata=dict()
    ftime = open('lastChecked.txt','r')
    prevTime = float(ftime.readline())
    ftime.close()
    f = open('lastChecked.txt','w')
    f.write(str(time.time()))
    f.close()
    k = 0
    while k < len(Recs):
        (name, ext) = os.path.splitext(Recs[k])         
        if len(ext) > 2 and not ext == '.pickle':
            ListFile = name + ".pickle"
            if not os.path.isfile(ListFile) or float(fmt.filemtime(Recs[k])) > prevTime:
                if ext[:3] == ".fa":
                    if name != "my_seq":
                        seqIORec = list(SeqIO.parse(Recs[k],'fasta'))
                        for i,v in enumerate(seqIORec):
                            newList.append([v,v.id])                   
                            listdata[j] = str(v.id),len(v.seq),str(name)+str(ext)
                            rHoward = [str(v.id),len(v.seq),str(name)+str(ext),v]
                            mP.spickle(ListFile,rHoward)
                            j+=1
                            
                elif ext[:3] == ".gb":                
                    seqIORec = list(SeqIO.parse(Recs[k],'genbank'))
                    for i,v in enumerate(seqIORec):
                        newList.append([v,v.id])                   
                        listdata[j] = str(v.id),len(v.seq),str(name)+str(ext)
                        rHoward = [str(v.id),len(v.seq),str(name)+str(ext),v]
                        mP.spickle(ListFile,rHoward)
                        j+=1
                
                        
            else:
                if ext[:3] in [".gb",".fa"]:
                    rHoward = mP.opickle(ListFile)
                    listdata[j] = str(rHoward[0]),rHoward[1],rHoward[2]
                    newList.append([rHoward[3],rHoward[0]])
                    j+=1
        k += 1

    return [newList,listdata]
