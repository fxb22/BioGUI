import wx
import plotter as mpl
from numpy import arange, cos, sin, pi

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

    def GetExec(self, frame, coverPanel, rec, frameObjs):
        self.frame = frame
        self.rec = rec[0]
        self.coverPanel = coverPanel
        self.frameObjs = frameObjs
        self.GbInit()        
        cs = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel, size = (cs[1],cs[1]),
                                        pos = ((cs[0] - cs[1]) / 2,0))
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
        iTypes = 0
        srf = self.rec[0].features
        while iTypes < len(self.searchTypes):
            f = 0
            col = searchCols[iTypes]
            while f < len(srf):
                if srf[f].type == self.searchTypes[iTypes]:
                    featLoc = srf[f].location
                    startPos = int(featLoc.nofuzzy_start)
                    endPos = startPos + len(srf[f])
                    a = (1+srf[f].strand*0.1)
                    t = arange(endPos, startPos, -0.1) * a
                    b = 2*pi*t/(self.seqLen)/(1+srf[f].strand*0.1)+pi/2
                    s = a*sin(b)
                    u = a*cos(b)
                    self.axes1.plot(s, u, linewidth = 3, color = col)
                    a = (1 + srf[f].strand * 0.35)
                    b = (startPos + (1 - srf[f].strand) * len(srf[f]) / 2)
                    self.axes1.annotate(srf[f].qualifiers['locus_tag'],
                        (a * sin(2 * pi * b / (self.seqLen) + pi / 2),
                         a * cos(2 * pi * b / (self.seqLen) + pi / 2)),
                        xytext = (a * sin(2 * pi * b / (self.seqLen) + pi / 2),
                                  a * cos(2 * pi * b / (self.seqLen) + pi / 2)),
                        textcoords = 'data', fontsize = 4,
                        horizontalalignment = 'center',
                        verticalalignment = 'center')
                f += 1
            iTypes += 1

    def DoPlot(self):
        t = arange(self.seqLen - 1, 0, - self.seqLen / 1000)
        s = sin(2 * pi * t / (self.seqLen) + pi/2)
        u = cos(2 * pi * t / (self.seqLen) + pi/2)        
        self.axes1.plot(s,u, 'k-', linewidth = 3)
        self.axes1.set_ylabel('')
        self.axes1.set_xlabel(str(self.seqLen - 1) + ' bp')
        self.axes1.set_xticks([-2, 2])
        self.axes1.set_yticks([-2, 2])        
        self.axes1.set_ylim(-1.5, 1.5)
        self.axes1.set_xlim(-1.5, 1.5)
        self.plotter.resize([3.05 / 244, 3.05 / 244])

    def DoView(self, event):
        self.plotter.remove()
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.seqLen = len(self.rec[0]) + 1
        self.searchTypes = []
        self.Annotate()
        self.DoPlot()

def GetName():
    return "Circular"
