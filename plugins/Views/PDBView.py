import wx
import os
from Bio.PDB.PDBParser import PDBParser
import getPlugins as gpi
import warnings

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        self.frame.SetPosition((self.bPSize[0] - 307,0),-1)
        self.frame.SetSize((200,self.bPSize[1] - 8))
        self.coverPanel.SetSize((self.bPSize[0] - 307,self.bPSize[1]))
        self.coverPanel.SetPosition((0,0))
        if self.timesCalled > 2:
            self.curView.OnSize()
        self.frame.Show(True)

    def Refresh(self,record):
        self.rec = record
        if self.timesCalled > 2:
            self.DefinePdbMat()
            if self.buttonLabel == 'CPCompS':
                self.curView.Refresh(self.rec,
                                     [self.pdbMat[0][self.mo],
                                      self.pdbMat[1][self.mo]])
            else:
                self.curView.Refresh(self.rec[0][1]+'/'+self.rec[0][0],
                                     self.pdbMat[0][self.mo])
        else:
            self.GetExec(record)

    def Clear(self):
        self.frame.Show(False)
        self.coverPanel.Show(False)

    def OnCombo(self, event):
        event.SetEventObject(self.lastButton)
        self.mo = self.modelChoice.GetCurrentSelection()
        self.DoView()

    def OnFrSize(self, event):
        self.curView.FrChange(self.frSize.GetValue())        

    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\PDBViewPlugins")
        xPos = 10
        yPos = 130
        for i,v in enumerate(self.views.values()):
            if xPos > 150:
                xPos = 10
                yPos += 22
            viewName = v.GetName()
            self.tabButtons.append(wx.Button(self.frame, -1, str(viewName),
                                             pos=(xPos, yPos), size=(60, 22),
                                             style = wx.NO_BORDER))
            self.tabButtons[i].SetBackgroundColour(
                self.cL['ViewPanelGrayFrame']['Back'])
            self.tabButtons[i].SetForegroundColour(
                self.cL['ViewPanelGrayFrame']['Fore'])
            xPos += 60
            self.frame.Bind(wx.EVT_BUTTON, self.OnButton, self.tabButtons[i])
        self.curView = self.views.values()[0].Plugin()
        self.lastButton = self.tabButtons[0]
        self.buttonLabel = self.tabButtons[0].GetLabelText()

    def CoverInit(self):               
        self.coverPanel = wx.Panel(self.bigPanel, -1, style = wx.NO_BORDER,
                                   pos = (0, 0))
        self.coverPanel.SetSize((self.bPSize[0] - 307, self.bPSize[1] - 3))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.Show(False)

    def FrameInit(self):
        self.frame = wx.Panel(self.bigPanel, -1, style = wx.RAISED_BORDER)
        self.frame.SetPosition((self.bPSize[0] - 307, 0), -1)
        self.frame.SetSize((200, self.bPSize[1] - 3))
        self.frame.SetBackgroundColour(self.cL['ViewPanelGrayFrame']['Back'])
        self.frame.SetForegroundColour(self.cL['ViewPanelGrayFrame']['Fore'])
        self.textFrameSize = wx.StaticText(self.frame, -1, pos = (40, 70),
                                           label="Max. Interaction\nDistance")
        self.frSize = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(40, 100))
        self.frSize.SetValue(6)
        self.frame.Bind(wx.EVT_SPINCTRL, self.OnFrSize)
        self.frame.Show(False)

    def ModelUpdate(self):
        self.modelText = wx.StaticText(self.frame, -1, "Active Model:",
                                       pos = (40, 20))
        self.modelChoice = wx.ComboBox(self.frame, -1, choices = self.choose,
                                       pos = (40, 40), style = wx.CB_READONLY)
        self.modelChoice.SetSelection(0)
        self.mo = self.modelChoice.GetCurrentSelection()
        self.bigPanel.Bind(wx.EVT_COMBOBOX, self.OnCombo, self.modelChoice)

    def Init(self, parent, bigPanel, colorList):
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.cL = colorList
        self.tabButtons = []
        self.FrameInit()
        self.CoverInit()
        self.TabButtonInit()
        self.timesCalled = 0
        self.ssMeth = 0
        self.p = PDBParser(PERMISSIVE=1)
        
    def DefinePdbMat(self):
        self.pdbMat = []
        for r in self.rec:
            filename = str(r[0])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore") 
                structure = self.p.get_structure('WHYY',
                                                 str(r[1])+'/'+filename)
                self.pdbMat.append(structure.get_list())
            for c in self.pdbMat:
                self.choose.append(str(c)[1:-1])
        if len(self.pdbMat) < 2:
            self.rec.append(self.rec[0])
            self.pdbMat.append(self.pdbMat[0])
                
    def GetExec(self, rec):
        self.pdbMat = []
        self.frame.Show(True)
        self.coverPanel.Show(True)     
        self.rec = rec
        self.choose = []
        if self.timesCalled > 2:
            self.DefinePdbMat()
            self.ModelUpdate()
            self.DoView()

    def OnButton(self,event):        
        self.DefinePdbMat()
        if self.timesCalled > 2:
            if self.buttonLabel in ['CPSS', 'Motif Finder']:
                self.ssMeth = self.curView.GetMeth()
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        self.timesCalled = 2
        self.ModelUpdate()
        self.DoView()

    def DoView(self):
        self.frame.Show(True)
        self.coverPanel.Show(True)
        self.coverPanel.SetBackgroundColour('WHITE')
        for o in self.coverPanel.GetChildren():
            o.Show(False)
            o.Destroy()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                self.curView = v.Plugin()
                if self.timesCalled > 2:
                    if self.buttonLabel in ['CPSS', 'Motif Finder','CPcompS']:
                        self.ssMeth = self.curView.GetMeth()
        self.timesCalled += 1
        if self.buttonLabel == 'CPCompS':
            self.curView.GetExec(self.rec, self.frame,
                                 self.coverPanel, self.frSize.GetValue(),
                                 [self.pdbMat[0][self.mo],
                                  self.pdbMat[1][self.mo]])
        else:
            self.curView.GetExec(self.rec[0][1]+'/'+self.rec[0][0], self.frame,
                         self.coverPanel, self.frSize.GetValue(),
                         self.pdbMat[0][self.mo])

    def GetType(self):
        return "PDB"

    def GetName(self):
        return "PDBView"

def GetType():
    return "PDB"

def GetName():
    return "PDBView"
