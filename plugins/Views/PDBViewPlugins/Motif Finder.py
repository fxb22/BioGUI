import wx
import math
import plotter as mpl
import GetMotifs as gm
import numpy
from numpy import arange, cos, sin, arctan, pi

class Plugin():     
    def GetMeth(self):
        return self.ssCombo.GetSelection()

    def SetMeth(self,meth):
        self.ssCombo.SetSelection(meth)
        
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(False)
        self.plotter.SetSize(self.bPSize[0] - 125, self.bPSize[1])
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.plotter.SetSize(self.plotPanel.GetSize())
        self.ssText.SetPosition((5,self.bPSize[1]/3 - 50))
        self.ssCombo.SetPosition((5,self.bPSize[1]/3))
        self.plotter.Show(True)
        self.DoDraw()
        
    def FrChange(self,frSize):
        self.frSize = frSize
        self.motifChoice.Show(False)
        self.moCh = self.motifChoice.GetSelection()
        self.DoDraw()

    def Refresh(self,rec,pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.moCh = 0
        self.motifChoice.Show(False)
        self.MotifComboUpdate()
        self.DoDraw(wx.EVT_IDLE)

    def SComboInit(self):
        self.ssText = wx.StaticText(self.coverPanel, -1,
                                    "Secondary\n  Structure\n    Algorithm:",
                                    pos = (5, self.bPSize[1] / 3 - 50))
        self.ssCombo = wx.ComboBox(self.coverPanel, -1,
                                   choices = ['Backbone','DSSP'],
                                   pos = (5, self.bPSize[1] / 3),
                                   style = wx.CB_READONLY)
        self.ssCombo.SetSelection(0)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoDraw, self.ssCombo)

    def MotifComboInit(self, chose):
        self.motifChoice = wx.ComboBox(self.coverPanel, -1,
                                       choices = chose,
                                       pos = (5,self.bPSize[1]*2/3),
                                       style = wx.CB_READONLY)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoMotifCombo,
                             self.motifChoice)
        self.motifChoice.Show(False)

    def GetExec(self, rec, frame, coverPanel, frSize, pdbMat):
        self.rec = rec
        self.frame = frame
        self.coverPanel = coverPanel
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.SetForegroundColour('WHITE')
        self.pdbMat = pdbMat
        self.frSize = frSize
        self.bPSize = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                size = (self.bPSize[0] - 125, self.bPSize[1]),
                                pos = (125, 0))
        self.moCh = 0
        self.plotter.Show(True)
        self.coverPanel.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.SComboInit()
        self.MotifComboInit([''])
        self.motifChoice.Show(True)
        self.DoDraw(wx.EVT_IDLE)

    def DoDraw(self, event):
        self.axes1.clear()
        motifs = gm.GetMotifs()
        temp = motifs.GetExec(self.rec, self.frSize,
                                     self.pdbMat, self.GetMeth())
        self.orders = temp[0][0]
        self.helices = temp[1]
        self.MotifComboUpdate()
        self.axes1.axis('off')
        self.axes1.set_xlim(0,4)
        self.axes1.set_ylim(-1,1)
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.plotter.Show(True)
        self.motifChoice.Show(True)

    def MotifComboUpdate(self):
        self.motifChoice.Show(False)
        self.axes1.clear()
        chose = []
        for i,o in enumerate(self.orders):
            tc = str(len(o))
            chose.append('Motif '+str(i)+'; '+tc+' strands')
        self.MotifComboInit(chose)
        self.motifChoice.SetSelection(0)
        self.motifChoice.Show(True)
        self.DoMotifCombo(wx.EVT_IDLE)

    def ArrowPrint(self):
        o = self.orders[self.motifChoice.GetSelection()]
        self.mt = 1
        if len(o) > 5:
            self.mt = self.mt - (len(o) - 5.0) / len(o)
        x = .05
        rot = 90
        placevaldir = []
        for oh in o:
            if oh[1] == -1:
                rot *= -1
            col = (.9,1,.9)
            c = 'g'
            ordir = 1
            if rot == -90:
                col = (1,.9,.8)
                c = (1,.5,.1)
                ordir = -1
            placevaldir.append([x, oh[0], ordir])
            bbox_props = dict(boxstyle="rarrow", fc=col, ec=c, lw=2)
            self.axes1.text(x, -rot*.025/90, "   ", ha = "center",
                            va = "center", rotation = rot,
                            size = 50 * self.mt, bbox = bbox_props)
            self.axes1.text(x, -rot * .275/90 * self.mt, str(oh[0][0]),
                            ha = "center", va = "center", rotation = 0,
                            size = 10*self.mt)
            self.axes1.text(x, rot*.125/90*self.mt, str(int(oh[0][1] - 0.6)),
                            ha = "center", va = "center", rotation = 0,
                            size= 10 * self.mt)
            x += .9*self.mt
        return placevaldir

    def NoHelixLines(self, pvd):
        x = [0, .1*self.q, .2*self.q, .25*self.q,
             -(pvd[0]-self.p)*self.q-.1, -(pvd[0]-self.p)*self.q]
        y = [.475*pvd[2], .675*pvd[2], 0, -.575*pvd[2],
             -.675*pvd[2], -.475*pvd[2]]
        mat = numpy.linalg.inv(numpy.array([[4.,1.,0,0,0], [1.,4.,1.,0,0],
                               [0,1.,4.,1.,0],[0,0,1.,4.,1.],[0,0,0,1.,4.]]))
        nums = [0]
        bmat = numpy.array([y[0]-2.*y[1]+y[2],y[1]-2.*y[2]+y[3],
                            y[2]-2.*y[3]+y[4],y[2]-2.*y[3]+y[4],
                            y[3]-2.*y[4]+y[5]])
        for m in mat:
            s = 0
            for k,n in enumerate(m):
                s += bmat[k]*n
            nums.append(s)
        z = 0
        while z < 5:            
            t = ((x[z+1]-x[z])**2)
            trax = nums[z + 1]*6/t
            t = arange(0,(x[z+1]-x[z]),.0001)
            a = ((trax-nums[z])/(6.*(x[z+1]-x[z])))*t**3
            b = (nums[z]/2.)*t**2
            c = (y[z+1]-y[z])/(x[z+1]-x[z])
            e = (((trax+2.*nums[z])/6.)*(x[z+1]-x[z]))
            f = (c-e)*t
            ell = (a + b + f + y[z])*self.mt
            ecc = (t + x[z])*-self.q + self.p
            self.axes1.plot(ecc,ell,'b')
            z += 1

    def HelixLines(self, pvd):
        t = arange(0, 53*pi/16 ,.01)*self.q
        s = sin(4*t)/4
        u = cos(4*t)/4
        self.axes1.plot((s-u+(pvd[0] - self.p)*self.q*t)/10+self.p,
                ((s+u)/6+t/pi/3*self.q*-pvd[2]+.55*pvd[2])*self.mt, 'r-')
        t = 0
        s = sin(4*t)/4
        u = cos(4*t)/4
        a = [self.p,(s-u+(pvd[0]-self.p)*self.q*t)/10 + self.p]
        b = [.475*pvd[2]*self.mt,
             ((s+u)/6+t/pi/3*self.q*-pvd[2]+.55*pvd[2])*self.mt]
        self.axes1.plot(numpy.array(a), numpy.array(b), 'b-')
        t = 53*pi/16*self.q
        s = sin(4*t)/4
        u = cos(4*t)/4
        self.axes1.plot(numpy.array([pvd[0],
                                 (s-u+(pvd[0]-self.p)*self.q*t)/10+self.p]),
                        numpy.array([-.475*pvd[2]*self.mt,
                         ((s+u)/6+pvd[2]*(t/pi/3*-self.q+.55))*self.mt]),'b-')

    def NotHelix(self, pvd):
        t = arange(0.0, 0.5*-self.q, 0.01*-self.q)
        meanposY = -pvd[2]*0.475
        angle_phi = 0
        distXY = math.sqrt(abs((pvd[0] - self.p)) ** 2)
        distarc = 0.1 * distXY
        meanposX = (pvd[0] + self.p) / 2
        ecc = meanposX + distXY / 2 * cos(2*pi*t)
        ell = (meanposY + self.q*distarc * sin(2*pi*t*pvd[2]))*self.mt
        self.axes1.plot(ecc,ell,'b')

    def Helix(self, pvd):
        t = arange(0, 53*pi/16 ,.01)*self.q*(pvd[0] - self.p)
        s = sin(4*t)/4/(pvd[0] - self.p)
        u = cos(4*t)/4/(pvd[0] - self.p)
        self.axes1.plot((s-u+self.q*t)/10+self.p,
                    -((s+u)/6+.55*pvd[2]+0.05*(pvd[0]-self.p))*self.mt+.05,'r-')
        t = 0
        s = sin(4*t)/4/(pvd[0] - self.p)
        u = cos(4*t)/4/(pvd[0] - self.p)
        a = numpy.array([.4*pvd[2]*self.mt,
                         ((s+u)/6+.55*pvd[2])*self.mt])
        self.axes1.plot(numpy.array([self.p,self.p]), -a, 'b-')
        t = 53*pi/16*self.q*(pvd[0] - self.p)
        s = sin(4*t)/4/(pvd[0] - self.p)
        u = cos(4*t)/4/(pvd[0] - self.p)
        self.axes1.plot(numpy.array([pvd[0],
                                     (s-u+self.q*t)/10 + self.p]), -a, 'b-')
                        
    def FindMinVal(self, placevaldir):
        t = placevaldir[0]
        minval = t[1][0]
        for pvd in placevaldir[1:]:
            if pvd[1][0] <= minval:
                minval = pvd[1][0]
                t = pvd
        return t
    
    def DoPrint(self, placevaldir):
        pvd = self.FindMinVal(placevaldir)
        self.p = pvd[0]
        placevaldir.remove(pvd)
        self.d = pvd[2]
        self.v = pvd[1][1]
        while len(placevaldir) > 0:
            pvd = self.FindMinVal(placevaldir)
            self.q = 1
            if self.p < pvd[0]:
                self.q = -1
            helix = False
            for h in self.helices:
                if h > self.v and h < pvd[1][0]:
                    helix = True
                elif h < self.v and h > pvd[1][1]:
                    helix = True
            if self.d == pvd[2]:
                if not helix:
                    self.NoHelixLines(pvd)
                else:
                    self.HelixLines(pvd)                        
            elif not helix:
                self.NotHelix(pvd)
            else:
                self.Helix(pvd)
            placevaldir.remove(pvd)
            self.d = pvd[2]
            self.p = pvd[0]
            self.v = pvd[1][1]
        
    def DoMotifCombo(self,event):        
        self.axes1.clear()
        placevaldir = self.ArrowPrint()
        self.DoPrint(placevaldir)
        self.axes1.axis('off')
        self.axes1.set_xlim(0,4)
        self.axes1.set_ylim(-1,1)
        self.plotter.resize([3.05 / 244, 3.05 / 244])
            
def GetExec(rec, frSize, pdbMat, meth):
    cpss = cpc.SecondaryStructure()
    cpss.GetExec(rec, frSize, pdbMat, meth)
    return cpss

def GetName():
    return "Motif Finder"
