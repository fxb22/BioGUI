import wx
import math
import plotter as mpl
import CirclePlotClass as cpc
from numpy import arange, cos, sin, pi
import matplotlib.colors as colt
import matplotlib.cm as cm

class Plugin():
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(False)
        self.plotter.SetSize((self.bPSize[1], self.bPSize[1]))
        self.plotter.SetPosition(((self.bPSize[0]-self.bPSize[1])/2, 0))
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.resNameCheck.SetPosition((5, self.bPSize[1] / 2 + 50))
        self.plotter.Show(True)
        self.DoDraw(wx.EVT_IDLE)

    def FrChange(self, frSize):
        self.frSize = frSize
        self.DoDraw(wx.EVT_IDLE)

    def Refresh(self,rec,pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        #self.DoDraw()

    def Clear(self):
        for o in self.coverPanel.GetChildren():
            o.Show(False)
            o.Destroy()

    def ResNameCheckInit(self):
        self.resNameCheck = wx.CheckBox(self.coverPanel, -1,
                                        label = "Show Names?",
                                        pos = (5, self.bPSize[1] / 2 + 50))
        self.resNameCheck.Show(True)
        self.coverPanel.Bind(wx.EVT_CHECKBOX, self.DoDraw, self.resNameCheck)
        self.resNameCheck.SetValue(True)

    def GetExec(self, rec, frame, coverPanel, frSize, pdbMat):
        self.rec = rec
        self.frame = frame
        self.coverPanel = coverPanel
        self.pdbMat = pdbMat
        self.frSize = frSize
        self.bPSize = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                size = (self.bPSize[1],self.bPSize[1]),
                                pos = ((self.bPSize[0]-self.bPSize[1])/2, 0))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.SetForegroundColour('WHITE')
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.ResNameCheckInit()
        self.DoDraw(wx.EVT_IDLE)

    def PrintResName(self, rL):
        fs = 3*(self.bPSize[1]/247.-(self.total_length-80.)/80.)
        for t,res in enumerate(rL):
            if res != 'W':
                stl = self.total_length
                s = 1.15*cos(-2*pi*(t+0.2*self.bPSize[1]/633.*stl/80.)/stl+pi/2)
                u = 1.15*sin(2*pi*(t+0.2*self.bPSize[1]/633.*stl/80.)/stl+pi/2)
                self.axes1.text(s, u, '- ' + str(t + 1) + ' ' + res,
                                fontsize = fs, rotation = 90 - 360 * t / stl,
                                ha = 'center', va = 'center')
        
    def DefineCircle(self):
        spacing = 0.4*(self.bPSize[1]/633.-(self.total_length-80.)/80.)
        if spacing < 0.5:
            spacing = 0.5
        maxx = 0
        minn = self.numAtRes[0]
        for m,n in enumerate(self.numAtRes):
            if n > maxx:
                maxx = n
            elif n < minn and self.residueList[m] != 'W':
                minn = n
        chainEnds = self.cp.GetChainEnds()
        starter = 0
        while len(self.residueList) > starter:
            if self.residueList[starter] == 'W':
                col = 'w'
            else:
                col = colt.rgb2hex(cm.jet(int(math.floor(
                         255*(self.numAtRes[starter]-minn)/(maxx-minn)))))
            self.Draw_Arc(starter * 80. / self.total_length,
                          (starter + spacing) * 80. / self.total_length,
                          col, 2 * self.bPSize[1] / 247.)
            starter += 1
        if self.resNameCheck.GetValue():
            self.PrintResName(self.cp.GetResidues())

    def DoDraw(self, event):
        self.cp = GetExec(self.rec, self.frSize, self.pdbMat)
        self.total_length = self.cp.GetLength()
        self.residueList = self.cp.GetResidues()
        self.numAtRes = []
        self.spacesAtRes = []
        resCols = []
        linkCols = []
        self.axes1.clear()
        spacing = 0.4*(self.bPSize[1]/633.-(self.total_length-80.)/80.)
        if spacing < 0.5:
            spacing = 0.5
        i = 0
        while i < len(self.cp.GetCarbonPos()):
            self.numAtRes.append(0)
            self.spacesAtRes.append(0)
            i += 1
        for l in self.cp.GetLinks():
            col = colt.rgb2hex(cm.jet(int(
                math.floor(255*(l[2]-4.)/(self.frSize-4.)))))
            self.Draw_Ellipse((l[0]+spacing / 2) * 80. / self.total_length,
                              (l[1]+spacing/2)*80. / self.total_length,
                              col, (self.frSize-l[2]+1)*(self.frSize-l[2]))
            self.spacesAtRes[l[0]] += l[2]
            self.spacesAtRes[l[1]] += l[2]
            self.numAtRes[l[0]] += 1.
            self.numAtRes[l[1]] += 1.
        self.DefineCircle()
        self.axes1.set_xlim(-1.3, 1.3)
        self.axes1.set_ylim(-1.3, 1.3)
        self.axes1.axis('off')
        self.plotter.resize([3.05 / 244, 3.05 / 244])

    def Draw_Ellipse(self, numa, numb, col, distarc):
        ecc1 = sin(2 * pi * numa / 80)
        ecc2 = sin(2 * pi * numb / 80)
        ell1 = cos(2 * pi * numa / 80)
        ell2 = cos(2 * pi * numb / 80)
        eccb = .1*sin(2*pi*((numa-numb)/2+numb)/80)
        ellb = .1*cos(2*pi*((numa-numb)/2+numb)/80)
        i = 0
        ecc = []
        ell = []
        while i <= 1:
            ecc.append((1-i)*((1-i)*ecc1+i*eccb)+i*((1-i)*eccb+i*ecc2))
            ell.append((1-i)*((1-i)*ell1+i*ellb)+i*((1-i)*ellb+i*ell2))
            i += 0.01
        self.axes1.plot(ecc,ell,color = col, lw = distarc)

    def Draw_Arc(self, starter, chainEnds, col, num):
        t = arange(starter, chainEnds, 0.1)
        s = cos(-2*pi*t/(80)+pi/2)
        u = sin(2*pi*t/(80)+pi/2)
        self.axes1.plot(s,u, color = col, lw = num)

def GetExec(rec, frSize, pdbMat):
    cp = cpc.CirclePlot()
    cp.Dist_Calc(rec, frSize, pdbMat)
    return cp

def GetName():
    return "Circle Plot"
