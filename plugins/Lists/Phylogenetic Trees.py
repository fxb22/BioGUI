import os
from Bio import Phylo

#List View Plugin for a folder containing phylogenetic tree objects

def GetExec():
    Recs = os.listdir(os.getcwd())
    
    newList=[]
    j = 0

    listdata=dict()
    k = 0
    while k < len(Recs):
        (name, ext) = os.path.splitext(Recs[k])
        if len(ext)>3 and ext[0:4]=='.dnd':
            tree = Phylo.read(Recs[k], "newick")
            tree.rooted = True
            newList.append([tree,'ok'])
            listdata[j] = j,str(Recs[k])
            j+=1
        elif len(ext)>3 and ext[0:4]=='.xml':
            tree = Phylo.read(Recs[k], "phyloxml")
            tree.rooted = True
            newList.append([tree,'ok'])
            listdata[j] = j,str(Recs[k])
            j+=1
    
        k += 1
    return [newList,listdata]

        








            
