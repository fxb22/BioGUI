import wx
import plotter as mpl
import CirclePlotClass as cpc
from numpy import arange, cos, sin, pi

class Plugin():            
    def GetMeth(self):
        return self.ssCombo.GetSelection()

    def SetMeth(self, meth):
        self.ssCombo.SetSelection(meth)
    
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(False)
        self.plotter.SetSize(self.bPSize[1], self.bPSize[1])
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.ssText.SetPosition((5,self.bPSize[1]/2 - 50))
        self.ssCombo.SetPosition((5,self.bPSize[1]/2))
        self.resNameCheck(5, self.bPSize[1] / 2 + 50)
        self.plotter.Show(True)
        
    def FrChange(self, frSize):
        self.frSize = frSize
        self.DoDraw(wx.EVT_IDLE)

    def Refresh(self, rec, pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.DoDraw(wx.EVT_IDLE)

    def SComboInit(self):
        self.ssText = wx.StaticText(self.coverPanel, -1,
                                    "Secondary\n  Structure\n    Algorithm:",
                                    pos = (5, self.bPSize[1] / 2 - 50))
        self.ssCombo = wx.ComboBox(self.coverPanel, -1,
                                   choices = ['Backbone','DSSP'],
                                   pos = (5, self.bPSize[1] / 2),
                                   style = wx.CB_READONLY)
        self.ssCombo.SetSelection(0)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoDraw, self.ssCombo)
        
    def ResNameCheckInit(self):
        self.resNameCheck = wx.CheckBox(self.coverPanel, -1,
                                        label = "Show Names?",
                                        pos = (5, self.bPSize[1] / 2 + 50))
        self.resNameCheck.SetValue(False)
        self.resNameCheck.Show(True)
        self.coverPanel.Bind(wx.EVT_CHECKBOX, self.DoDraw, self.resNameCheck)

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
        self.SComboInit()
        self.ResNameCheckInit()
        self.DoDraw(wx.EVT_IDLE)

    def PrintResName(self, rL):
        for t,res in enumerate(rL):
            if res != 'W':
                if t % 5 == 0:
                    stl = self.total_length
                    s = 1.15 * sin(2*pi*t/(stl+1))
                    u = 1.2 * cos(2*pi*t/(stl+1))
                    if cos(2 * pi * t / (stl)) < 0:  
                        self.axes1.text(s, u, str(t),fontsize = 6,
                                        rotation = 180 - 360*(stl-t-1)/(stl),
                                        ha = 'center', va = 'center')
                    else:
                        self.axes1.text(s, u, str(t),fontsize = 6,
                                        rotation = 360 * t / (stl),
                                        ha = 'center', va = 'center')
        
    def DefineCircle(self):
        chainEnds = self.cpss.cp.GetChainEnds()
        starter = 0.0
        while len(chainEnds) > 0:
            while starter < chainEnds[0]:
                self.Draw_Arc(starter, starter + .6, 'k', 1)
                starter += 1
            starter = chainEnds[0]
            chainEnds.remove(chainEnds[0])
        if self.resNameCheck.GetValue():
            self.PrintResName(self.cpss.cp.GetResidues())
            
    def DoDraw(self, event):
        self.cpss = GetExec(self.rec, self.frSize, self.pdbMat,
                            self.GetMeth())
        self.total_length = self.cpss.cp.GetLength()
        self.axes1.clear()
        self.DefineCircle()
        for sse in self.cpss.GetSSE():
            if sse[2] == 0:
                sse = self.Draw_Arc(sse[0], sse[1], 'g', 6)
            elif sse[2] == 1:
                sse = self.Draw_Arc(sse[0], sse[1], 'y', 6)
        for sL in self.cpss.GetSecLinks():
            if sL[2] == 0:
                self.Draw_Ellipse(sL[0], sL[1], 'b-',.001)
            elif sL[2] == 1:
                self.Draw_Ellipse(sL[0], sL[1], 'r-',.15)
            elif sL[2] == 2:
                self.Draw_Ellipse(sL[0], sL[1], 'm-',.1)
        self.axes1.set_xlim(-1.3, 1.3)
        self.axes1.set_ylim(-1.3, 1.3)
        self.axes1.axis('off')
        self.plotter.resize([3.05 / 244, 3.05 / 244])

    def Draw_Ellipse(self, numa, numb, col, distarc):
        ecc1 = sin(2 * pi * numa / self.total_length)
        ecc2 = sin(2 * pi * numb / self.total_length)
        ell1 = cos(2 * pi * numa / self.total_length)
        ell2 = cos(2 * pi * numb / self.total_length)
        eccb = .1*sin(2*pi*((numa-numb)/2+numb)/self.total_length)
        ellb = .1*cos(2*pi*((numa-numb)/2+numb)/self.total_length)
        i = 0
        ecc = []
        ell = []
        while i <= 1:
            ecc.append((1-i)*((1-i)*ecc1+i*eccb)+i*((1-i)*eccb+i*ecc2))
            ell.append((1-i)*((1-i)*ell1+i*ellb)+i*((1-i)*ellb+i*ell2))
            i += 0.01
        self.axes1.plot(ecc,ell,col)

    def Draw_Arc(self, starter, chainEnds, col, num):
        t = arange(starter, chainEnds, 0.1)
        s = cos(-2*pi*t/(self.total_length)+pi/2)
        u = sin(2*pi*t/(self.total_length)+pi/2)
        self.axes1.plot(s,u, col+'-', lw = num)

def GetExec(rec, frSize, pdbMat, meth):
    cpss = cpc.SecondaryStructure()
    cpss.GetExec(rec, frSize, pdbMat, meth)
    return cpss

def GetName():
    return "CPSS"
