import os
import sys
from Bio import Entrez
import wx
from xml.dom import minidom
import re

class etPlugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "ESpell"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoES.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile
    
    def GetExec(self,parent,dbName,query):
        self.parent = parent
        self.handle = Entrez.espell(db=dbName,term=query,rettype='xml')
        erl = self.handle.read()

        parent.text2.Clear()

        lines = erl.split('\n')
        for line in lines[3:6]:
            parent.text2.write(line)
            parent.text2.write('\n')

        parent.text1.Clear()
        newQ = re.sub('.*<CorrectedQuery>','',lines[5])
        newQ = re.sub('</CorrectedQuery>','',newQ)
        parent.text1.write(newQ)
        print erl

    def helpEXE(self,parent):
        parent.l1.Show(True)
        parent.text1.Show(True)
        parent.l2.Show(True)
        parent.l3.Show(True)

        parent.text2 = wx.TextCtrl(parent.panelRSLT, -1, "", size=(892, 370),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10))
        wx.CallAfter(parent.text2.SetInsertionPoint, 0)
        
        tempVal = parent.dbCB.GetValue()
        parent.dbList =['pubmed', 'protein', 'nuccore', 'nucleotide', 'nucgss', 'nucest',
                      'structure', 'genome', 'genomeprj', 'bioproject', 'biosample',
                      'biosystems', 'blastdbinfo', 'books', 'cancerchromosomes', 'cdd',
                      'gap', 'dbvar', 'epigenomics', 'gene', 'gensat', 'gds', 'geo',
                      'geoprofiles', 'homologene', 'journals', 'mesh', 'ncbisearch',
                      'nlmcatalog', 'omia', 'omim', 'pmc', 'popset', 'probe',
                      'proteinclusters', 'pcassay', 'pccompound', 'pcsubstance',
                      'seqannot', 'snp', 'sra', 'taxonomy', 'toolkit', 'toolkitall',
                      'unigene', 'unists', 'gencoll', 'gcassembly']

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
        parent.Bind(wx.EVT_COMBOBOX, parent.helpDB, parent.dbCB)

def GetExec(dbName,idName):
    return Entrez.espell(db=dbName,id=idName)
