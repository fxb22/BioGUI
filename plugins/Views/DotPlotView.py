import wx
import plotter as mpl

class Plugin():
    def OnSize(self):
        self.plotter.Show(False)
        self.boxer.Show(False)
        self.bPSize = self.bigPanel.GetSize()
        ps = (self.bPSize[0] / 2., self.bPSize[1] * 220. / 247.)
        self.boxer.SetPosition((self.bPSize[0] * 0.735,
                                self.bPSize[1] / 2 - 30))
        self.plotter.SetSize(ps)
        self.plotter.SetPosition((self.bPSize[0] * .23, 10))
        self.plotter.resize([2.9 / 225., 2.75 / 220.])
        self.textSeq1.SetPosition((15, self.bPSize[1] / 6.))
        self.seq1Combo.SetPosition((15, self.bPSize[1] / 6. + 20))
        self.seq1Combo.SetSize((self.bPSize[0] * 0.2 - 15, -1))
        self.textSeq2.SetPosition((15, self.bPSize[1] / 2.))
        self.seq2Combo.SetPosition((15, self.bPSize[1] / 2. + 20))
        self.seq2Combo.SetSize((self.bPSize[0] * 0.2 - 15, -1))
        self.plotter.Show(True)
        self.boxer.Show(True)
        
    def GetType(self):
        types = ["Amino Acids", "Nucleic Acids"]
        return types
    
    def GetName(self):
        return "DotPlotView"

    def Refresh(self,record):
        self.axes1.clear()
        self.plotter.remove()
        self.seq1Combo.Show(False)
        self.seq2Combo.Show(False)
        self.GetExec(record)

    def Clear(self):
        self.textSeq1.Show(False)
        self.textSeq2.Show(False)
        self.seq1Combo.Show(False)
        self.seq2Combo.Show(False)
        self.axes1.clear()
        self.plotter.remove()
        self.plotter.Show(False)
        self.boxer.Show(False)

    def OnFrSize(self, event):
        self.axes1.clear()
        self.plotter.remove()
        self.DoView()
    
    def Init(self, parent, bigPanel, colorList):
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.colorList = colorList
        ps = (self.bPSize[0] / 2., self.bPSize[1] * 220. / 247.)
        self.plotter = mpl.PlotNotebook(self.bigPanel,
                                        size = ps,
                                        pos = (self.bPSize[0] * .23, 10))
        self.boxer = wx.Panel(self.bigPanel, -1, style = wx.NO_BORDER,
                              pos = (self.bPSize[0] * 0.735,
                                     self.bPSize[1] / 2 - 30),
                              size = (90, 60))
        self.boxer.SetBackgroundColour('NAVY')
        self.textFrameSize = wx.StaticText(self.boxer, -1, pos = (10, 5),
                                           label = "Window Size:")
        self.textFrameSize.SetForegroundColour('WHITE')
        self.frSize = wx.SpinCtrl(self.boxer, -1, size=(75, -1), pos=(10, 30))
        self.bigPanel.Bind(wx.EVT_SPINCTRL, self.OnFrSize)
        self.frSize.SetValue(10)
        self.textSeq2 = wx.StaticText(self.bigPanel, -1,
                                 pos = (15, self.bPSize[1] / 2.),
                                 label = "Sequence 2:")
        self.textSeq2.SetBackgroundColour(
            self.colorList['ViewPanel']['Back'])
        self.textSeq2.SetForegroundColour(
            self.colorList['ViewPanel']['Fore'])
        self.textSeq1 = wx.StaticText(self.bigPanel, -1,
                                 pos = (15, self.bPSize[1] / 6.),
                                 label = "Sequence 1:")
        self.textSeq1.SetBackgroundColour(
            self.colorList['ViewPanel']['Back'])
        self.textSeq1.SetForegroundColour(
            self.colorList['ViewPanel']['Fore'])
        self.boxer.Show(False)
        self.plotter.Show(False)

    def OnRecPick(self, event):
        r = [self.seq1Combo.GetSelection(),self.seq2Combo.GetSelection()]
        self.recs = [self.rec[r[0]][0].seq, self.rec[r[1]][0].seq]
        self.data = []
        self.FindDots()
        self.DoView()
        
    
    def SeqCombosInit(self):
        ps = (self.bPSize[0] / 2., self.bPSize[1] * 220. / 247.)
        self.chose = []
        for r in self.rec:
            self.chose.append(r[0].id)
        self.seq1Combo = wx.ComboBox(self.bigPanel, -1,
                                      choices = self.chose,
                                      pos = (15, self.bPSize[1] / 6. + 20),
                                      size = (self.bPSize[0] * 0.2 - 15, -1),
                                      style = wx.CB_READONLY)
        
        self.seq2Combo = wx.ComboBox(self.bigPanel, -1,
                                      choices = self.chose,
                                      pos = (15, self.bPSize[1] / 2. + 20),
                                      size = (self.bPSize[0] * 0.2 - 15, -1),
                                      style = wx.CB_READONLY)
        self.seq2Combo.Bind(wx.EVT_COMBOBOX, self.OnRecPick)
        self.seq1Combo.Bind(wx.EVT_COMBOBOX, self.OnRecPick)
        self.seq2Combo.SetSelection(0)
        self.seq1Combo.SetSelection(0)
        self.OnRecPick(wx.EVT_IDLE)

    def GetExec(self, rec):
        self.boxer.Show(True)
        self.plotter.Show(True)
        self.rec = rec
        self.SeqCombosInit()

    def DotCheck(self, iters, i, d, h):
        if d > 0:
            if h > 0:
                self.data.append([iters + 1, iters + d + 1, d])
                self.data.append([i + 1, i + d + 1, d])
            if h < 0:
                self.data.append([i , i - d , d])
                self.data.append([iters + 1, iters + d + 1, d])                
        return 0
                    
    def FindDots(self):
        minL = len(self.recs[0])
        if len(self.recs[1]) < minL:
            minL = len(self.recs[1])
            maxL = len(self.recs[0])
            self.recs = [self.recs[1], self.recs[0]]
        else:
            maxL = len(self.recs[1])
            self.recs = [self.recs[0], self.recs[1]]
        iters = 0
        while iters < minL + maxL - 1:
            if iters >= maxL:
                i = maxL + minL - iters - 1
                ip = maxL - 1
            else:
                ip = iters
                i = minL - 1
            diagUp = 0
            diagDn = 0
            
            while i >= 0 and ip >= 0:
                if self.recs[0][i] == self.recs[1][ip]:
                    diagUp += 1
                else:
                    diagUp = self.DotCheck(ip, i, diagUp, 1)
                if self.recs[0][minL - i - 1] == self.recs[1][ip]:
                    diagDn += 1
                else:
                    diagDn = self.DotCheck(ip, minL - i - 1, diagDn, -1)
                i -= 1
                ip -= 1
            diagUp = self.DotCheck(ip, i, diagUp, 1)             
            diagDn = self.DotCheck(ip, minL - i - 1, diagDn, -1)
            iters += 1
        """iters = 0
        while iters <= maxL:
            i = 0
            diagUp = 0
            diagDn = 0
            while i < minL - iters:
                if self.recs[0][iters + i] == self.recs[1][i]:
                    diagUp += 1
                else:
                    diagUp = self.DotCheck(iters, i, diagUp, 1)
                ls = len(self.recs[1])
                if self.recs[0][iters + i] == self.recs[1][ls - 1 - i]:
                    diagDn += 1
                else:
                    diagDn = self.DotCheck(iters, i, diagDn, -1)
                i += 1
            i -= 1
            diagUp = self.DotCheck(iters, i, diagUp, 1)                
            diagDn = self.DotCheck(iters, i, diagDn, -1)
            iters += 1"""

    def DoView(self):
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        i = 0
        while i < len(self.data):
            if self.data[i] == self.data[i+1]:
                colorCode = 'r'
            else:
                colorCode = 'k'
            if self.data[i][2] >= self.frSize.GetValue():
                self.axes1.plot(self.data[i][:2],self.data[i+1][:2], colorCode)
            i += 2
        self.axes1.set_xlim(0,len(self.recs[0]))
        self.axes1.set_ylim(0,len(self.recs[1]))
        self.plotter.resize([2.9 / 225., 2.75 / 220.])

    def GetType(self):
        types = ["Amino Acids", "Nucleic Acids"]
        return types

    def GetName(self):
        return "DotPlotView"

def GetType():
    types = ["Amino Acids", "Nucleic Acids"]
    return types

def GetName():
    return "DotPlotView"
