import os
import errno

from Bio.Blast import NCBIXML

#List View Plugin for a folder containing blast objects

def GetExec():
    Recs = os.listdir(os.getcwd())
    BlastRec = []
    newList=[]
    j = 0
    
    listdata=dict()
    for k,itsgo in enumerate(Recs):  
        try:
            (name, ext) = os.path.splitext(itsgo)
            if ext=='':
                2+2
            elif ext == ".xml":
                result_handle = open(itsgo)
                BlastRec = list(NCBIXML.parse(result_handle))#ext[1:]))
                for v in BlastRec:
                    IORec = v
                    newList.append(IORec)
                    
                    listdata[j]=str(name)+str(ext),str(IORec.query),str(IORec.application),IORec.date
                    j+=1
                    
        except IOError, e:
            print e

    return [newList,listdata]

        








            
