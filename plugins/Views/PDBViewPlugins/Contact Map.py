import wx
import math
import plotter as mpl
import CirclePlotClass as cpc
from numpy import arange, cos, sin, pi

class Plugin():
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(True)
        self.plotter.SetSize(self.bPSize[1], self.bPSize[1])
        self.plotter.resize([5.5 / 244, 3.05 / 244])
        self.resNameCheck(5, self.bPSize[1] / 2 + 50)
        self.plotter.Show(True)

    def FrChange(self, frSize):
        self.frSize = frSize
        self.DoDraw(wx.EVT_IDLE)

    def Refresh(self,rec,pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.DoDraw(wx.EVT_IDLE)

    def Clear(self):
        for o in self.coverPanel.GetChildren():
            o.Show(False)

    def GetExec(self, rec, frame, coverPanel, frSize, pdbMat):
        self.rec = rec
        self.frame = frame
        self.coverPanel = coverPanel
        self.pdbMat = pdbMat
        self.frSize = frSize
        self.bPSize = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                size = (self.bPSize[0],self.bPSize[1]),
                                pos = (0, 0))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.SetForegroundColour('WHITE')
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.DoDraw(wx.EVT_IDLE)

    def DoDraw(self, event):
        self.cp = GetExec(self.rec, self.frSize, self.pdbMat)
        tl = self.cp.GetLength()
        x = []
        y = []
        self.axes1.clear()
        i = 0
        while i < tl:
            x.append(i)
            y.append(i)
            x.append(i)
            y.append(i+1)
            x.append(i)
            y.append(i-1)
            x.append(i)
            y.append(i+2)
            x.append(i)
            y.append(i-2)
            i += 1
        for l in self.cp.GetLinks():
            if l[2] <= self.frSize:
                x.append(l[0])
                y.append(l[1])
                x.append(l[1])
                y.append(l[0])
        self.axes1.scatter(x, y, s = 10, c = 'b', marker = 's')
        self.axes1.set_xlim(-1, tl)
        self.axes1.set_ylim(-1, tl)
        self.plotter.resize([3.05 / 244, 3.05 / 244])

def GetExec(rec, frSize, pdbMat):
    cp = cpc.CirclePlot()
    cp.Dist_Calc(rec, frSize, pdbMat)
    return cp

def GetName():
    return "Contact Map"                    
