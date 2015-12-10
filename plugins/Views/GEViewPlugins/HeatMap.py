import wx
import plotter as mpl
import numpy as np
import matplotlib.pyplot as plt

class Plugin():
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(False)
        self.plotter.SetSize((self.bPSize[1], self.bPSize[1]))
        self.plotter.SetPosition(((self.bPSize[0]-self.bPSize[1])/2, 0))
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.plotter.Show(True)
        self.DoDraw(wx.EVT_IDLE)
        
    def GetParamList(self):
        return self.rec

    def Clear(self):
        for o in self.coverPanel.GetChildren():
            o.Show(False)
            o.Destroy()

    def GetGeMat(self):
        return self.geMat

    def GetExec(self, f, coverPanel, rec,  geMat, colorList):
        self.rec = rec
        self.coverPanel = coverPanel
        self.geMat = geMat
        self.bPSize = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                size = (self.bPSize[1], self.bPSize[1] * 1.08),
                                pos = ((self.bPSize[0]-self.bPSize[1])/2,
                                       -self.bPSize[1] * .08))
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        colMat = GetExec(self.rec, geMat, 'tri')
        self.Z3 = np.transpose(np.array(colMat))
        plt.spectral()
        self.DoDraw()
        return self.geMat
        
    def DoDraw(self):
        self.axes1.pcolor(self.Z3, vmin=-.9, vmax=1.1)
        lab = []
        for r in self.rec:
            for a in r:
                lab.append(a)
        self.axes1.set_xticks(np.arange(self.Z3.shape[0])+0.5, minor=False)
        self.axes1.set_xticklabels(lab, rotation = -20,
                                   size = int(self.bPSize[1] * .02))
        self.axes1.set_yticks([],False)
        self.axes1.set_xlim(0,len(self.geMat)-1)
        self.axes1.set_ylim(0,len(self.geMat[0]))
        self.plotter.Show(True)        
        self.plotter.resize([3.05 / 244, 3.05 / 244])

def BitCompare(meanIn, meanOut):
    colMat = []
    for i,m in enumerate(meanIn):
        if m >= meanOut[i]:
            colMat.append(1)
        else:
            colMat.append(0)
    return colMat

def TempMat(meanIn, meanOut, inMat, outMat):
    ti = inMat
    to = outMat
    i = 0
    j = len(ti) - 1
    for check,val in enumerate(meanIn):
        if val > meanOut[check]:
            for q,row in enumerate(ti):
                row[i] = inMat[q][check]
            for q,row in enumerate(to):
                row[i] = outMat[q][check]
            i += 1
        else:
            for q,row in enumerate(ti):
                row[j] = inMat[q][check]
            for q,row in enumerate(to):
                row[j] = outMat[q][check]
            j -= 1
    tempMat = []
    for row in ti:
        tempMat.append(row)
    for row in to:
        tempMat.append(row)
    return np.array(tempMat)

def TriCompare(Z):
    colMat = Z
    meanZ = np.mean(Z, dtype=np.float64, axis=0)
    stdZ = np.std(Z, dtype=np.float64, axis=0)
    for i,row in enumerate(Z):
        for j,val in enumerate(row):
            if ((val - meanZ[j]) / stdZ[j]) > -.5:
                if ((val - meanZ[j]) / stdZ[j]) > .5:
                    colMat[i][j] = 1
                else:
                    colMat[i][j] = -1
            else:
                colMat[i][j] = 0
        i += 1
    return colMat
        
def GetExec(rec, geMat, comp):
    inMat = []
    outMat = []
    for row in geMat[:-1]:
        if row[0] in rec[0]:
            inMat.append(row[1:])
        else:
            outMat.append(row[1:])
    t = np.array(inMat)
    meanIn = np.mean(t, dtype=np.float64, axis=0)
    meanOut = np.mean(np.array(outMat), dtype=np.float64, axis=0)
    if comp == 'bit':
        colMat = BitCompare(meanIn, meanOut)
    elif comp == 'tri':
        Z = TempMat(meanIn, meanOut, inMat, outMat)
        colMat = TriCompare(Z)
    return colMat


def GetName():
    return "Heat Map"
