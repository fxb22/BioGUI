import os
import errno

from Bio import AlignIO

#List View Plugin for a folder containing alignment objects
def GetExec():
    Recs = os.listdir(os.getcwd())

    newList=[]
    j = 0

    listdata=dict()
    k = 0
    while k < len(Recs):
        try:
            (name, ext) = os.path.splitext(Recs[k])
            typo = ''
            if ext in [".txt",".fas",".fasta"]:
                IORec = AlignIO.parse(Recs[k],'fasta')
                typo = 'fasta'
            elif ext in [".aln"]:
                IORec = AlignIO.parse(Recs[k],'clustal')
                typo = 'clustal'
            aNum = 1
            for align in IORec:
                newList.append([align,name])
                NumSeqs = 0
                for rec in align:
                    NumSeqs += 1
            
                listdata[j] = str(Recs[k]),aNum, NumSeqs,align.get_alignment_length(),str(typo)
                j += 1
                aNum += 1
        
        except IOError, e:
            print e

        k += 1
        
    return [newList,listdata]

        








            
