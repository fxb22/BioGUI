import os
import sys
from Bio import Entrez
import wx
from xml.dom import minidom
import re

class Plugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "EFetch"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoEF.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def recursive(self,cc):
        if cc.hasChildNodes():
            for c in cc.childNodes:
                self.recursive(c)
        else:
            if cc.localName == None:
                if not re.search('\S',cc.toxml()) == None:
                    self.trac.append(cc.parentNode.localName)
                    self.trac.append(cc.toxml())        

    def parse(self):
        b=self.handle.read()
        self.trac=[]
        try:
            b1=re.sub('&lt;','<',b)
            b2=re.sub('/?&gt;','>',b1)
            b3=re.sub('&quot;','"',b2)
            b4=re.sub('\n</pre></body></html>','',b3)
            b5=re.sub('<html><head><title>PmFetch response</title></head><body>\n<pre>\n','',b4)
            textbase=minidom.parseString(b5)
            for c in textbase.childNodes:
                #print c.localName
                self.recursive(c)
        except:
            lines = b.split('\n')
            tempf = open('toobigxml.txt','w')
            for iters,line in enumerate(lines[2:]):
                line1 = re.sub('&lt;','<',line)
                line2 = re.sub('&gt;','>',line1)
                line3 = re.sub('&quot;','"',line2)
                line4 = re.sub('</pre></body></html>','',line3)
                line5 = re.sub('<html><head><title>PmFetch response</title></head><body>','',line4)
                line6 = re.sub('<pre>','',line5)
                tempf.write(line6+'\n')
            tempf.close()
        
            textbased = open('toobigxml.txt','r')
            textbase = minidom.parse(textbased)
            
            for c in textbase.childNodes:
                #print c.localName
                self.recursive(c)
                
            
        retmat=self.trac
        return retmat
    
    def GetExec(self,parent,dbName,query):
        parent.text2.Clear()

        self.handle = Entrez.efetch(db=dbName,id=query,rettype='xml')
        if parent.dbCB.GetValue() == 'journals':
            erl = self.handle.read()
            lines = erl.split('\n')
            for line in lines[3:-2]:
                parent.text2.write(line)
                parent.text2.write('\n')

        else:
            erl = self.parse()
                
            for idk,e in enumerate(erl):
                parent.text2.write(str(e))
                parent.text2.write('\n')

    def helpEXE(self,parent):
        parent.l1.Show(True)
        parent.text1.Show(True)
        parent.l2.Show(True)
        parent.l3.Show(True)

        parent.text2 = wx.TextCtrl(parent.panelRSLT, -1, "", size=(892, 370),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10))
        wx.CallAfter(parent.text2.SetInsertionPoint, 0)

        tempVal = parent.dbCB.GetValue()
        parent.dbList = ['pubmed', 'protein', 'nuccore', 'nucleotide',
                       'nucgss', 'nucest', 'genome', 'gene', 'homologene',
                       'journals', 'nlmcatalog', 'omim', 'pmc', 'popset',
                       'snp', 'sra', 'taxonomy']

        parent.dbGoMenu=[]             # Database menu options.
        for dummy in parent.dbList:    # Iterate through all available databases
            parent.dbGoMenu.append(wx.NewId())

        tempIdNum = len(parent.menuHandlers)
        for itnum,tool in enumerate(parent.dbList):       
            parent.menuHandlers.append((parent.dbGoMenu[itnum],     parent.helpDB))
            
        parent.lowDB,dummy = parent.menuHandlers[tempIdNum]

        #Setup the database menu options
        parent.dbaseMenu = wx.Menu()
        for itnum,tool in enumerate(parent.dbList):
            parent.dbaseMenu.Append(parent.dbGoMenu[itnum],   tool,      kind=wx.ITEM_RADIO)
        
        #Update the menu bar
        parent.menuBar.Replace(2,parent.dbaseMenu, "Database")
        parent.menuBar.UpdateMenus()

        parent.dbCB.Show(False)
        parent.dbCB = wx.ComboBox(parent=parent.panelSQ, id=-1, pos=(256,6),
                 choices=parent.dbList, style=wx.CB_READONLY)
        tempChk = 0
        while tempChk < len(parent.dbList):
            if tempVal == parent.dbList[tempChk]:
                parent.dbCB.SetSelection(tempChk)
                tempChk = len(parent.dbList)
            tempChk += 1

        if tempChk == len(parent.dbList):
            parent.dbCB.SetSelection(0)
        
        parent.dbCB.Show(True)
        parent.Bind(wx.EVT_COMBOBOX, parent.helpDB, parent.dbCB)
        
            

def GetExec(dbName,idName):
    return Entrez.efetch(db=dbName,id=idName,tool='BioGUI')
