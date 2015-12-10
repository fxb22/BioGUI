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
        return "ELink"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\ncbi_logoEL.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile
    
    def GetExec(self,parent,dbName,query):
        self.parent = parent
        handle = Entrez.esearch(db=dbName,term=query)
        erl = Entrez.read(handle)
        
        for idk,e in enumerate(erl):
            parent.windowBin.append(wx.TextCtrl(parent.panelRSLT, -1, '', size=(892, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10 + (idk * 55))))
            parent.windowBin[idk].write(str(e))
            parent.windowBin[idk].write('   ')
            parent.windowBin[idk].write(str(erl[e]))
            parent.windowBin[idk].write('\n')
            wx.CallAfter(parent.windowBin[idk].SetInsertionPoint, 0)

    
    def helpDBCheck(self,event):
        callerObj = event.GetEventObject()
        if callerObj.GetValue():
            self.parent.windowBin.append(wx.ComboBox(self.parent.panelSQ, -1, pos=(130,67),
                                                     choices=self.parent.dbList, style=wx.CB_READONLY, name='db2CB'))
            self.parent.windowBin[-1].SetSelection(0)

        else:
            i = 0
            while i < len(self.parent.windowBin):
                if self.parent.windowBin[i].GetName()[:5] == 'db2CB':
                    self.parent.windowBin[i].Show(False)
                    self.parent.windowBin.pop(i)
                else:
                    i += 1

    def helpCMDCheck(self,event):
        callerObj = event.GetEventObject()
        if callerObj.GetValue():
            cmdVals = ['prlinks', 'ref', 'llinks', 'llinkslib', 'lcheck', 'ncheck',
                       'neighbor', 'neighbor_score', 'neighbor_history', 'acheck']
            self.parent.windowBin.append(wx.ComboBox(self.parent.panelSQ, -1, pos=(375,67),
                                                     choices=cmdVals, style=wx.CB_READONLY, name='cmdCB'))
            self.parent.windowBin[-1].SetSelection(0)

        else:
            i = 0
            while i < len(self.parent.windowBin):
                if self.parent.windowBin[i].GetName()[:6] == 'cmdCB':
                    self.parent.windowBin[i].Show(False)
                    self.parent.windowBin.pop(i)
                else:
                    i += 1

    def helpCBsel(self,event):
        i = 0
        while i < len(self.parent.windowBin):
            if self.parent.windowBin[i].GetName()[:7] == 'Link2CB':
                self.parent.windowBin[i].Show(False)
                self.parent.windowBin.pop(i)
            else:
                i += 1
                
        callerObj = event.GetEventObject()
        idx = callerObj.GetSelection()
        self.link2names = ['']
        if not callerObj.GetValue() == '':
            for link in self.linkNames:
                tabs = link.split('_')
                if tabs[0] == self.linkDes[idx]:
                    self.link2names.append(link[(len(tabs[0])+1):])

            self.parent.windowBin.append(wx.StaticText(self.parent.panelSQ, -1, "Link\nNames:", pos=(200,35), name='linkCBtext'))
            self.parent.windowBin[-1].SetForegroundColour('WHITE')
            self.parent.windowBin.append(wx.ComboBox(self.parent.panelSQ, -1, pos=(245,37),
                                                     choices=self.link2names, style=wx.CB_READONLY, name='Link2CB'))
            self.parent.windowBin[-1].SetSelection(0)

    def helpEXE(self,parent):
        self.parent = parent
        parent.l1.Show(True)
        parent.text1.Show(True)
        parent.l2.Show(True)
        parent.l3.Show(False)
        
        tempVal = parent.dbCB.GetValue()
        parent.dbList =['all', 'pubmed', 'protein', 'nuccore', 'nucleotide', 'nucgss', 'nucest',
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
            parent.dbCB.SetSelection(1)
        parent.Bind(wx.EVT_COMBOBOX, parent.helpDB, parent.dbCB)

        self.linkDes = ['']
        self.linkNames = []
        self.link2names = []

        f = open(r'C:\Users\francis\Documents\Monguis\BioGui\plugins\Tools\EtoolsPlugins\eLinkDescriptions.text[1]')
        fhandle = f.read()
        lines = fhandle.split('\n')
        for line in lines:
            tabs = line.split('\t')
            self.linkNames.append(tabs[0])
            spacers = tabs[0].split('_')
            if not spacers[0] in self.linkDes:
                self.linkDes.append(spacers[0])
                
        parent.windowBin.append(wx.StaticText(parent.panelSQ, -1, r"Link: ", pos=(18,42)))
        parent.windowBin[-1].SetForegroundColour('WHITE')
        parent.windowBin.append(wx.ComboBox(parent.panelSQ, -1, pos=(50,37),
                         choices=self.linkDes, style=wx.CB_READONLY, name='Link1CB'))
        parent.windowBin[-1].SetSelection(0)
        parent.Bind(wx.EVT_COMBOBOX, self.helpCBsel, parent.windowBin[-1])

        parent.dbCB.Show(True)
        parent.windowBin.append(wx.StaticText(parent.panelSQ, -1, "Database (to): ", pos=(175,10), name='db1CB'))
        parent.windowBin[-1].SetForegroundColour('WHITE')

        parent.windowBin.append(wx.CheckBox(parent.panelSQ, -1, r"Database (from): ", pos=(18,70), name='check2DB'))
        parent.windowBin[-1].SetForegroundColour('WHITE')
        parent.Bind(wx.EVT_CHECKBOX, self.helpDBCheck, parent.windowBin[-1])

        parent.windowBin.append(wx.CheckBox(parent.panelSQ, -1, r"Link Command: ", pos=(275,70), name='checkCMD'))
        parent.windowBin[-1].SetForegroundColour('WHITE')
        parent.Bind(wx.EVT_CHECKBOX, self.helpCMDCheck, parent.windowBin[-1])


def GetExec(dbName,idName):
    return Entrez.elink(db=dbName,id=idName)
