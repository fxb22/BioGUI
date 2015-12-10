import wx
import plotter as mpl
import SSEPlotGenerator as spg

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        self.coverPanel.SetSize((self.bPSize[0]-257,self.bPSize[1]-8))
        for p in self.panes:
            p.SetSize((self.bPSize[0]-294,100))
        self.DoView(wx.EVT_IDLE)
        
    def Clear(self):
        # Erase view
        if hasattr(self, 'coverPanel'):
            self.coverPanel.Show(False)
            while len(self.plots) > 0:
                self.plots[0].remove()
                self.plots[0].Destroy()
                self.plots.pop(0)

    def CoverInit(self):
        self.coverPanel = wx.ScrolledWindow(self.bigPanel, -1,
                                            style = wx.VSCROLL,
                                            pos = (0, 0),
                                            size = (self.bPSize[0] - 257,
                                                    self.bPSize[1] - 8))
        self.coverPanel.SetScrollbars(0, 1, 0, len(self.cur)*150 - 30)
        self.coverPanel.SetScrollRate(15, 35)
        self.coverPanel.Show(True)

    def PaneInit(self):
        self.panes = []
        self.plots = []
        self.texts = []
        for i,c in enumerate(self.cur):
            self.texts.append(wx.StaticText(self.coverPanel, -1,
                                            pos = (10, 150 * i + 15),
                                            label = ''))
            pane = wx.Panel(self.coverPanel, -1, size=(self.bPSize[0]-294,100),
                            pos = (10,150*i+40), style = wx.SIMPLE_BORDER)
            t = mpl.PlotNotebook(pane, pos = (-25, 0),
                                 size = (self.bPSize[0] - 269, 100))
            self.panes.append(pane)
            self.plots.append(t)

    def ButtonInit(self):
        # Create button
        self.manyButton = wx.Button(self.gf, -1, 'Combine', pos = (10, 150),
                                    size = (130, 50), style = wx.NO_BORDER)
        self.manyButton.SetBackgroundColour('RED')
        self.manyButton.SetForegroundColour('WHITE')
        self.gf.Bind(wx.EVT_BUTTON, self.Combine, self.manyButton)
        
    def GetExec(self, bp, gf, rec, cL):
        self.bigPanel = bp
        self.gf = gf
        self.bPSize = self.bigPanel.GetSize()
        self.rec = rec
        self.name = rec[0].name
        self.cur = []
        for r in rec:
            if r.name == self.name:
                self.cur.append(r)
        self.ButtonInit()
        self.CoverInit()
        self.PaneInit()
        self.DoView(wx.EVT_IDLE)

    def DoView(self, event):
        for i,c in enumerate(self.cur):
            self.plots[i].remove()
            self.texts[i].SetLabel(c.id)
            self.plots[i].SetSize((self.bPSize[0] - 269, 100))
            axes1 = spg.SSEPlot(c.seq, self.plots[i])
            self.plots[i].resize([3.05 / 244, 3.05 / 244])

    def Combine(self, event):
        dic = {'H':{} , 'E':{}, '.':{}}
        for c in self.cur:
            for i,s in enumerate(c.seq):
                if not i in dic[s].keys():
                    dic[s][i] = 0
                dic[s][i] += 1
        seq = ['']
        for c in self.cur[0].seq:
            seq.append('.')
        for pos in dic['H'].keys():
            if dic['H'][pos] > len(self.cur) / 2.:
                seq[pos] = 'H'
        for pos in dic['E'].keys():
            if dic['E'][pos] > len(self.cur) / 2.:
                seq[pos] = 'E'
        seqStr = ''
        for s in seq[1:]:
            seqStr += s
        self.cur = [self.cur[0]]
        self.cur[0].id = 'Combined'
        self.cur[0].seq = seqStr
        self.Clear()
        self.CoverInit()
        self.PaneInit()
        self.DoView(wx.EVT_IDLE)

def GetName():
    return "PlotBars"
