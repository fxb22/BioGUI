import os
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#List View Plugin for a folder containing protein objects
def GetExec():
    Recs = os.listdir(os.getcwd())  
    newList = []
    listdata = dict()
    for k,r in enumerate(Recs):
        if r[-6:]==".fasse":
            if r[:-6] != "my_fasse":
                s = open(r,'r').read().split('>')
                for i,v in enumerate(s[1:]):
                    try:
                        t = []
                        b = v.split('\n')
                        nam = str(b[0])
                        aa = str(b[1])
                        j = 2
                        while j < len(b)-1:
                            if len(b[j])>0 and b[j][0]=='$' and b[j+1][0]=='&':
                                typ = str(b[j][1:])
                                sse = str(b[j+1][1:])
                                t.append(SeqRecord(Seq(sse), id = typ,
                                                   name = nam,
                                                   description = aa))
                            j += 2
                        newList.append(t)
                        listdata[i] = str(nam), len(t), str(r)                    
                    except:
                        2
    return [newList,listdata]

        








            
