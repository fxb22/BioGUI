import os
import sys
from Bio import Entrez
import wx
import re
from xml.dom import minidom

class etPlugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "EGQuery"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoEG.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile
    
    def GetExec(self,parent,dbName,query):
        handle = Entrez.egquery(term=query)
        Eread = minidom.parseString(handle.read())
        resultNodes = Eread.childNodes[3].childNodes[3].childNodes
        idk = 0
        while idk < len(parent.text2):
            parent.text2[idk].Show(False)
            parent.text2.pop(idk)

        parent.text2 = []
        parent.text2.append(wx.TextCtrl(parent.panelRSLT, -1, "", size=(892, 390),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10)))
        wx.CallAfter(parent.text2[0].SetInsertionPoint, 0)
        
        i = 1
        while i < len(resultNodes):
            j = 0
            font = parent.text2[-1].GetFont()
            newFont = wx.Font(font.PointSize, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
            parent.text2[-1].SetFont(newFont)
            while j < len(resultNodes[i].childNodes):
                lengthWrite = 0
                
                parent.text2[-1].write(str(resultNodes[i].childNodes[j].localName))
                lengthWrite += len(str(resultNodes[i].childNodes[j].localName))
                parent.text2[-1].write(r':  ')
                lengthWrite += len(r':  ')
                parent.text2[-1].write(str(resultNodes[i].childNodes[j].childNodes[0].data))
                lengthWrite += len(str(resultNodes[i].childNodes[j].childNodes[0].data))
                addLength = 8 - lengthWrite % 8
                lengthWrite += addLength
                while addLength > 0:
                    parent.text2[-1].write(' ')
                    addLength -= 1
                if j == 2:
                    lengthWrite += 16
                while lengthWrite < 32:
                    parent.text2[-1].write('\t')
                    lengthWrite += 8
                
                j += 1
            parent.text2[-1].write('\n')
            i += 2
            wx.CallAfter(parent.text2[-1].SetInsertionPoint, 0)
        return 2

    def helpEXE(self,parent):
        parent.l1.Show(True)
        parent.text1.Show(True)
        parent.l2.Show(True)
        
def GetExec(dbName,idName):
    return Entrez.egquery(db=dbName,id=idName)
