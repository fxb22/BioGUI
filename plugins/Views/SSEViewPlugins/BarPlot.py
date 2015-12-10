import wx
import plotter as mpl
import SSEPlotGenerator as spg

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        if hasattr(self, 'plot'):
            self.plot.remove()
            self.plot.Destroy()
        self.DoView(wx.EVT_IDLE)
        
    def Clear(self):
        # Erase view
        if hasattr(self, 'combo'):
            self.combo.Show(False)
        if hasattr(self, 'plot'):
            self.plot.remove()
            self.plot.Destroy()
        
    def SetCombo(self):
        choose = {}
        for r in self.cur:
            choose[r.id] = r
        self.combo = wx.ComboBox(self.gf, -1, choices = choose.keys(),
                                 pos = (15, 120), size = (120, -1),
                                 style = wx.CB_READONLY)
        self.combo.SetSelection(0)
        self.bigPanel.Bind(wx.EVT_COMBOBOX, self.DoView, self.combo)

    def GetExec(self, bp, gf, rec, cL):
        self.gf = gf
        self.bigPanel = bp
        self.bPSize = self.bigPanel.GetSize()
        self.rec = rec
        self.name = rec[0].name
        self.cur = []
        for r in self.rec:
            if r.name == self.name:
                self.cur.append(r)
        self.SetCombo()
        self.DoView(wx.EVT_IDLE)

    def DoView(self, event):
        self.plot = mpl.PlotNotebook(self.bigPanel, pos = (-25, 70),
                                     size = (self.bPSize[0] - 232,
                                             self.bPSize[1] - 95))
        c = self.combo.GetSelection()
        axes1 = spg.SSEPlot(self.cur[c].seq, self.plot)
        self.plot.resize([3.05 / 244, 3.05 / 244])

def GetName():
    return "Bar Plot"
