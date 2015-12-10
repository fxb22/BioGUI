import wx
import math
from numpy import arange, cos, sin, pi
import plotter as mpl

class Plugin():
    def Clear(self):
        self.axes1.clear()
        self.plotter.remove()
        self.plotter.Show(False)
        self.goButton.Show(False)
        
    def OnSize(self):
        self.plotter.Show(False)
        try:
            self.plotter.SetSize(self.coverPanel.GetSize())
            self.plotter.resize([3.05 / 244, 3.05 / 244])
        except:
            2
        self.plotter.Show(True)
        self.goButton.SetPosition((10,self.frame.GetSize()[1] - 34))
        
    def GbInit(self):
        self.goButton = wx.Button(self.frame, -1, label = 'GO!',
                                  pos = (10, self.frame.GetSize()[1] - 34),
                                  size = (self.frame.GetSize()[0] - 20, 22),
                                  style = wx.NO_BORDER, name='go1')
        self.goButton.SetBackgroundColour('RED')
        self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.goButton)

    def GetExec(self, frame, coverPanel, seqRec, frameObjs):
        self.frame = frame
        self.rec = seqRec
        self.coverPanel = coverPanel
        self.frameObjs = frameObjs
        self.GbInit()
        self.ps = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                        size = self.ps,
                                        pos = (0, 0))
        self.plotter.Show(False)

    def SearchColours(self):
        searchCols = []
        for f in self.frameObjs.keys():
            if self.frameObjs[f][0].GetValue():
                self.searchTypes.append(f)
                tempC = self.frameObjs[f][1].GetBackgroundColour()
                searchCols.append([tempC[0] / 255.,
                                   tempC[1] / 255.,
                                   tempC[2] / 255.])
        return searchCols
        
    def Annotate(self):
        searchCols = self.SearchColours()
        distX = (self.ps[0] - 100) / len(self.rec)
        meanposY1 = self.ps[1] - 30
        meanposX = 50 + distX / 2
        for r,rec in enumerate(self.rec):
            self.DoAxes(meanposX, distX, meanposY1, len(rec[0]))
            iTypes = 0
            while iTypes < len(self.searchTypes):
                f = 0
                col = searchCols[iTypes]
                for f in rec[0].features:
                    if f.type == self.searchTypes[iTypes]:
                        self.DoPlot(f, meanposX, distX, meanposY1, col)
                iTypes += 1
            self.axes1.text(meanposX, 20, r, ha = 'center', fontsize = 12)
            meanposX += distX
        self.axes1.set_xticks([-self.ps[0],self.ps[0]*2])
        self.axes1.set_yticks([-self.ps[1],self.ps[1]*2])
        self.axes1.set_xlim(0, self.ps[0])
        self.axes1.set_ylim(0, self.ps[1])
        self.plotter.resize([3.05 / 244, 3.05 / 244])

    def DoPlot(self, f, mX, dX, mY1, c):
        featLoc = f.location
        sP = int(featLoc.nofuzzy_start)
        eP = len(f)
        self.axes1.broken_barh([(mX - (1+f.strand) * dX/8 + 5, dX/4 - 10)],
                               (mY1  - (sP/self.maxLen*(self.ps[1] - 100.)),
                                -f.strand*(eP)/self.maxLen*(self.ps[1]-100.)),
                               facecolors = c, edgecolors = c)
        self.axes1.annotate(f.qualifiers['locus_tag'],
                            (mX - f.strand * (dX / 2 - 40),
                             mY1  - (sP / self.maxLen * (self.ps[1] - 100.))),
                            xytext = (mX - f.strand * (dX / 2 - 20),
                                      mY1-(sP/self.maxLen*(self.ps[1]-100.))),
                            textcoords = 'data', fontsize = 2,
                            horizontalalignment = 'center',
                            verticalalignment = 'top')

    def DoAxes(self, mX, dX, mY1, l):
        t = arange(0.0, 0.5, 0.01)
        ecc = mX + dX / 4 * sin(2*pi*t + pi / 2)
        ell = mY1 - 20 * cos(2*pi*t + pi / 2)
        self.axes1.plot(ecc,ell,'k-')
        mY = (mY1 - (self.ps[1] - 100 * self.maxLen / l / 1. )) 
        t = arange(0.5, 1.0, 0.01)
        ecc = mX + dX / 4 * sin(2*pi*t + pi / 2)
        ell = mY - 20 * cos(2*pi*t + pi / 2)
        self.axes1.plot(ecc,ell,'k-')
        self.axes1.plot([(mX - dX / 4) - 1,(mX - dX / 4) -1],
                        [mY1, mY], 'k-')
        self.axes1.plot([(mX + dX / 4),(mX + dX / 4)],
                        [mY1, mY], 'k-')

    def DoView(self, event):
        self.plotter.remove()
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.maxLen = 0
        for r in self.rec:
            if len(r[0]) >= self.maxLen:
                self.maxLen = len(r[0]) * 1.
        self.searchTypes = []
        self.Annotate()

def GetName():
    return "Map"
