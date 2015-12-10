import os

#List View Plugin for a folder containing objects of unknown types
#Plugin provides a list of available files
#TODO: When a file is selected, a user (maybe a comp based) selection of object type
#   is available. Selection opens appropriate view.

def GetExec():
    Recs = os.listdir(os.getcwd())
    
    newList=[]
    j = 0

    listdata=dict()
    k = 0
    while k < len(Recs):
        print len(Recs)

        newList.append(Recs[k])
        
        listdata[j] = j,str(Recs[k])
        j+=1
    
        k += 1
    return [newList,listdata]

        








            
