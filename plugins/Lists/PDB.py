import os
import sys
import errno
import time
from datetime import datetime
import filemtime as fmt
import Catche as mP
import warnings

from Bio.PDB.PDBParser import PDBParser

def GetExec():
    Recs = os.listdir(os.getcwd())
    newList = []
    j = 0
    listdata=dict()
    k = 0
    p = PDBParser(PERMISSIVE=1)
    ftime = open('lastChecked.txt','r')
    pT = float(ftime.readline())
    ftime.close()
    f = open('lastChecked.txt','w')
    f.write(str(time.time()))
    f.close()
    while k < len(Recs):
        try:
            (name, ext) = os.path.splitext(Recs[k])
            if ext=='':
                2+2
            elif ext==".pdb":
                f = name + ".pickle"
                newList.append([Recs[k],os.getcwd()])
                if not os.path.isfile(f) or float(fmt.filemtime(Recs[k])) > pT:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore") 
                        pdbRec = p.get_structure(name, Recs[k])
                    models = pdbRec.get_list()
                    listdata[j] = str(name), len(models), os.getcwd()+'/'+str(name) + str(ext)
                    rHoward = [str(name), len(models), str(name) + str(ext)]
                    mP.spickle(f, rHoward)
                else:
                    rHoward = mP.opickle(f)
                    listdata[j] = str(rHoward[0]), rHoward[1], rHoward[2]
                
                j += 1
                
                    
        except IOError, e:
            print e

    
        k += 1
    
    return [newList,listdata]
