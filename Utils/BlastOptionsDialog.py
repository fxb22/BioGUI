import wx

class optDialog(wx.Dialog):
    def __init__(self, parent, title, menuIn, fileName=None):
        self.parent = parent
        self.abet = 'AA'
        self.blstType = 'BLASTN'
        wx.Dialog.__init__(self, parent, title=title, size=(300, 450))
        self.menuList = {}
        for i,a in enumerate(menuIn.GetMenuItems()):
            self.menuList[a.GetItemLabel()] = i
        self.typeBox = wx.ComboBox(parent = self, id = -1, pos = (30,50),
                                   choices = self.menuList.keys(),
                                   style = wx.CB_READONLY)
        self.typeBox.SetSelection(0)
        self.typeBox.Bind(wx.EVT_COMBOBOX, self.DoType)
        self.abetBox = wx.ComboBox(parent = self, id = -1, pos = (30,150),
                                   choices = ['Amino Acid', 'Nucleotide'],
                                   style = wx.CB_READONLY)
        self.abetBox.SetSelection(0)
        self.abetBox.Bind(wx.EVT_COMBOBOX, self.DoAbet)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.parent.SetAbet(self.abet)
        self.parent.SetType(self.blstType)
        opts = {}
        for o in self.boxList:
            if not self.boxList[o] == '':
                opts[o] = self.boxList[o]
        self.parent.SetOptions(opts)
        self.Destroy()

    def GetOpts(self, bet, name):
        self.abet = bet
        if self.abet == 'AA':
            self.abetBox.SetSelection(0)
        else:
            self.abetBox.SetSelection(1)
        self.typeBox.SetSelection(self.menuList[name])
        self.DoBoxes(wx.EVT_IDLE)

    def DoAbet(self, event):
        if self.abetBox.GetSelection() == 0:
            self.abet = 'AA'
        else:
            self.abet = 'DNA'
        
    def DoType(self, event):
        for n in self.menuList.keys():
            if self.typeBox.GetSelection() == self.menuList[n]:
                self.blstType = n

    def DoBoxes(self,event):
        self.boxList = {}
        boxes = ['DB size', 'Culling Limit', 'Gap Open Cost', 'Gap Extend Cost',
             'Max. Number of Aligned Targets', 'Number of Alignments to Show',
             'Number of 1-line Descriptions to Show', 'Number of Threads to Use']
        y = 30
        for b in boxes:
            s = wx.StaticText(self, -1, b, pos=(125,y))
            self.boxList[b]=wx.TextCtrl(self,-1,"",size=(75,-1),pos=(150,y+20))
            y += 50
        
        #self.menuList[self.typeBox.GetCurrentSelection()]
        #Possibly not shown often self.matFileButton = filebrowsebutton.DirBrowseButton(parent=self, id=-1,pos=wx.Point(50,200), size=(500,50), labelText="Select Location\nof Desired Matrix")
            #gilist browser
        #XML or HTML output check boxes
        #Masking options could get messy
        #parse deflines checkbox
        #useful options for rest
        #To add:text-box for adding own options...l could present errors. need error calls.
