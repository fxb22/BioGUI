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
        return "EInfo"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoEI.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile
    
    def OnDBISelect(self,event):
        idx = event.GetSelection()
        if self.dbOvals[0][idx] > 0:
            self.parent.text2.Show(False)
        else:
            self.dbOvals[0][idx] = 1
            self.DbInfoChoices.append([])
            if str(self.DbInfoChoices[0][idx]) in ['LinkList', 'FieldList']:
                grouper = []
                for i,e in enumerate(self.Eread['DbInfo'][self.DbInfoChoices[0][idx]]):
                    grouper.append(str(i))
                    
                self.parent.windowBin.append(wx.ListBox(self.parent.panelRSLT, -1, pos=(200,10),
                                                   choices=grouper,
                                                   size=(100,100),style=wx.LB_MULTIPLE))
            else:
                self.parent.windowBin.append(wx.TextCtrl(self.parent.panelRSLT, -1,
                         self.Eread['DbInfo'][self.DbInfoChoices[0][idx]], size=(500, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(300,10)))
           
                
            

    def GetExec(self,parent,dbName,query):
        self.parent = parent
        self.handle = Entrez.einfo(db=dbName,rettype='xml')
        self.Eread = Entrez.read(self.handle)
        
        idk = 0
        while idk < len(parent.windowBin):
            parent.windowBin[idk].Show(False)
            parent.windowBin.pop(idk)

        self.DbInfoChoices = [[]]
        self.dbOvals = [[]]
        for e in self.Eread['DbInfo']:
            self.DbInfoChoices[0].append(e)
            self.dbOvals[0].append(0)

        parent.windowBin = []
        parent.windowBin.append(wx.ListBox(parent.panelRSLT, -1, pos=(75,10),
                                       choices=self.DbInfoChoices[0],
                                       size=(100,100),style=wx.LB_MULTIPLE))
        parent.Bind(wx.EVT_LISTBOX, self.OnDBISelect, parent.windowBin[-1])

    def helpEXE(self,parent):
        parent.l2.Show(True)
        parent.l3.Show(True)
        
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

def GetExec(dbName):
    return Entrez.einfo(db=dbName)
