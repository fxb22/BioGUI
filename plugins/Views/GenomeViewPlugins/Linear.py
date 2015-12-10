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
        fs = self.frame.GetSize()
        self.goButton.SetPosition((150, fs[1] - 34))
        self.textFrameSize.SetPosition((10, fs[1] - 30))
        self.frSize.SetPosition((70, fs[1] - 33))

    def GbInit(self):
        self.goButton = wx.Button(self.frame, -1, label = 'GO!',
                                  pos = (150, self.frame.GetSize()[1] - 34),
                                  size = (self.frame.GetSize()[0] - 160, 22),
                                  style = wx.NO_BORDER, name = 'go1')
        self.goButton.SetBackgroundColour('RED')
        self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.goButton)

    def FrSizeInit(self):
        self.textFrameSize = wx.StaticText(self.frame, -1,
                                       label = "# of Bars: ",
                                       pos = (10,self.frame.GetSize()[1] - 30),
                                       name = 'go1')
        self.frSize = wx.SpinCtrl(self.frame, -1, size=(75, -1),
                                  pos = (70,self.frame.GetSize()[1] - 33),
                                  name = 'go2')
        self.frSize.SetValue(6)

    def GetExec(self, frame, coverPanel, rec, frameObjs):
        self.frame = frame
        self.rec = rec[0]
        self.coverPanel = coverPanel
        self.frameObjs = frameObjs
        self.GbInit()
        self.FrSizeInit()
        cs = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                        size = (cs[0], cs[1]),
                                        pos = (0,0))
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

    def DoAxes(self, srf, sP, eP, bar, col):
        self.axes1.broken_barh([(sP,eP)],
                               (20*(self.numBars-bar-.5)+srf.strand*2.5+5,5),
                               facecolors = col)
        self.axes1.annotate(srf.qualifiers['locus_tag'],
            (sP+(1-srf.strand)*eP/2,
             20*(self.numBars-bar-.5)+srf.strand*(self.numBars+1) + 5.25),
            xytext=(sP+(1-srf.strand)*eP/2,
                    20*(self.numBars-bar-.5)+srf.strand*(self.numBars+1)+5.25),
            textcoords='data',
            fontsize=4,
            horizontalalignment='center',
            verticalalignment='bottom')

    def Annotate(self):
        searchCols = self.SearchColours()
        self.numBars = float(self.frSize.GetValue())
        self.barLen = math.ceil(self.seqLen / self.numBars)
        iTypes = 0
        while iTypes < len(self.searchTypes):
            col = searchCols[iTypes]
            for f in self.rec[0].features:
                if f.type == self.searchTypes[iTypes]:
                    featLoc = f.location
                    startTemp = int(featLoc.nofuzzy_start)
                    barNum = math.floor(startTemp / self.barLen)
                    startPos = startTemp % self.barLen
                    if startPos + len(f) > self.barLen:
                        endPos = self.barLen - startPos
                        end2Pos = startPos + len(f) - self.barLen
                        start2Pos = 0
                        bar2Num = barNum + 1
                        self.DoAxes(f, start2Pos, end2Pos, bar2Num, col)
                    else:
                        endPos = len(f)
                    self.DoAxes(f, startPos, endPos, barNum, col)
            iTypes += 1
            
    def DoPlot(self):
        i = 0
        yTicks = []
        tickIds = []
        while i < self.numBars - 1:
            self.axes1.axhline(y = 20 * (self.numBars - i - .5) + 7.5,
                               xmin = 0, xmax = self.barLen,
                               linewidth = 3, color = 'k')
            yTicks.append(20 * (self.numBars - i - .5) + 7.5)
            tickIds.append(i + 1)
            i += 1
        a = (self.seqLen - (self.barLen * (self.numBars - 1)))
        self.axes1.axhline(y = 20 * (self.numBars - i - .5) + 7.5, xmin = 0,
                           xmax = a / self.barLen - .25, linewidth = 3,
                           color = 'k')
        yTicks.append(20 * (self.numBars - i - .5) + 7.5)
        tickIds.append(i + 1)
        self.axes1.set_ylabel('Fragment')
        self.axes1.set_xlabel(str(int(self.barLen)) + ' bp per fragment')
        self.axes1.set_xticks([-self.barLen,2*self.barLen])
        self.axes1.set_yticks(yTicks)
        self.axes1.set_yticklabels(tickIds)
        self.axes1.set_ylim(5,20 * self.numBars + 10)
        self.axes1.set_xlim(0,self.barLen)
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        
    def DoView(self, event):
        self.plotter.remove()
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.seqLen = len(self.rec[0])
        self.searchTypes = []
        self.Annotate()
        self.DoPlot()
        
def GetName():
    return "Linear"
