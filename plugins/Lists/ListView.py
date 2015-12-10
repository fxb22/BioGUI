import sys
import wx
import os
import listControl as lc

#List View provides a list of available files
class ListView():          
    def OnSize(self):
        # Respond to sizing of the window
        self.bPSize = self.bigPanel.GetSize()
        self.lc.Show(False)
        self.lc.SetSize((self.bPSize[0] - 7, self.bPSize[1] - 2))
        self.lc.Show(True)
                               
    def Clear(self):
        # Method to hide and therefor destroy plugin while allowing future calls
        for c in self.bigPanel.GetChildren():
            c.Show(False)
        
    def GetRec(self):
        # Accessor to obtain currently selected objects
        pos = self.lc.GetSelected()
        rec = []
        for p in pos:
            rec.append(self.newList[self.lc.itemIndexMap[p]])
        return rec

    def OnSelect(self, event):
        # Respond to a selection of a list object
        # Sends selected objects to bioguimain
        self.parent.Refresh(self.GetRec())

    def ListCntrlFill(self):
        # Method to create list control column headers
        self.lc.Fill(self.viewTypes[self.type][0],
                     self.viewTypes[self.type][1])
            
    def ListRefill(self):
        # Fill and update list control
        t = self.lv.GetExec()
        self.newList = t[0]
        self.lc.Refill(t[1])
                     
    def Init(self, parent, bp, hd, cl):
        # Dictionary of List Types
        # Included: name (key), file (value)
        self.hD = hd
        self.parent = parent
        self.bigPanel = bp
        self.colorList = cl
        self.viewTypes = {
            "Alignments":         [['File','Alignment',"Seq. #'s",
                                    'Length','Format'],
                                   [400,75,75,75,104]],
            "Amino Acids":        [['Sequence','Length','File'],
                                   [350,110,347]],
            "Blast Results":      [['File','Query','Type','Date'],
                                   [350,110,200,147]],
            "Chromosomes":        [['Sequence','Length','File'],
                                   [350,110,347]],
            "Gene Expressions":   [['Record','Title','Platform','Samples'],
                                   [100,475,75,72]],
            "Images":             [['File'],
                                   [700]],
            "Nucleic Acids":      [['Sequence','Length','File'],
                                   [350,110,347]],
            "Phylogenetic Trees": [['#','File'],
                                   [25,677]],
            "SSE":                [['Sequence','# Methods','File'],
                                   [350,110,347]],
            "PDB":                [['PDB ID','# Models','File'],
                                   [350,110,347]],
            "Unknown":            [['#','File'],
                                   [25,677]]}

    def GetExec(self, typeName, cd):
        # Enable list control
        self.curDir = cd
        self.type = typeName
        sys.path.append(self.hD + r'.\plugins\listviewPlugins')
        self.lv = __import__(str(typeName))
        os.chdir(self.curDir)
        self.bPSize = self.bigPanel.GetSize()
        self.lc = lc.TestListCtrl(self.bigPanel, -1,
                                  pos = (self.bPSize[0] - 7,
                                         self.bPSize[1] - 2),
                                  size = (0, 0),
                                  style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                  numCols = len(self.viewTypes[self.type][0]))
        self.ListCntrlFill()
        self.ListRefill()
        self.lc.Show(True)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.lc.Select(0)
        os.chdir(self.hD)








            
