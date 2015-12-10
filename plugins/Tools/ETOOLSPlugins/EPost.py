import os
import sys
from Bio import Entrez
import wx
import re

class etPlugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "EPost"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoEP.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile
    
    def GetExec(self,parent,dbName,query):
        handle = Entrez.esearch(db=dbName,term=query)
        erl = Entrez.read(handle)
        idk = 0
        while idk < len(parent.text2):
            parent.text2[idk].Show(False)
            parent.text2.pop(idk)
        for idk,e in enumerate(erl):
            parent.text2.append(wx.TextCtrl(parent.panelRSLT, -1, '', size=(892, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10 + (idk * 60))))
            parent.text2[idk].write(str(e))
            parent.text2[idk].write('   ')
            parent.text2[idk].write(str(erl[e]))
            parent.text2[idk].write('\n')
            wx.CallAfter(parent.text2[idk].SetInsertionPoint, 0)

def GetExec(dbName,idName):
    return Entrez.epost(db=dbName,id=idName)
