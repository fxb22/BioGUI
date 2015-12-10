import wx
import plotter as mpl
import matplotlib.colors as colt
import pylab
import numpy as np
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties

class Plugin():
    def Clear(self):
        if hasattr(self, 'coverPanel'):
            self.coverPanel.Show(False)
            self.frameBox.Show(False)
            self.createButton.Show(False)
            
    def CoverInit(self):
        self.coverPanel = wx.Panel(self.bigPanel, -1, pos = (0, 0),
                                   size = (self.bPSize[0] - 277,
                                           self.bPSize[1] - 8))
        self.coverPanel.Show(True)
        fs = self.frame.GetSize()
        self.frameBox = wx.ScrolledWindow(self.frame, -1, pos = (2, 80),
                                          size = (fs[0] - 10, fs[1] - 120),
                                          style = wx.VSCROLL|wx.BORDER_SUNKEN)
        self.frameBox.SetBackgroundColour('WHITE')
        self.frameBox.Show(True)
        self.plotter = mpl.PlotNotebook(self.coverPanel,pos = (-50, 0),
                                        size = (self.bPSize[0] - 227,
                                                self.bPSize[1] - 8))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.axes1 = self.plotter.add('figure 1').gca()

    def FrameBoxFill(self):
        yPos = 5
        for opt in self.options:
            if '\n' in opt[1]:
                yp = yPos - 3
            else:
                yp = yPos + 3
            dummy = wx.StaticText(self.frameBox, -1, opt[1], pos=(3,yp))
            opt[2].SetSize((self.frameBox.GetSize()[0] - 80, -1))
            osi = opt[2].GetSize()
            if not osi[1] == 21:
                opt[2].SetPosition((57, yPos + (21-osi[1])/2))
            else:                
                opt[2].SetPosition((57, yPos))
            opt[2].SetValue(opt[3])
            yPos += 30

    def OptionsInit(self):
        tb = ['probability','entropy']
        self.options = [['lines','Number\nof lines:',
                         wx.SpinCtrl(self.frameBox, -1),1],
                        ['units','Units:',
                         wx.ComboBox(self.frameBox,-1,choices=tb,
                                     style=wx.CB_READONLY),tb[1]],
                        ['start','Start res.:',
                         wx.TextCtrl(self.frameBox, -1, "",),'1'],
                        ['end','Final res.:',
                         wx.TextCtrl(self.frameBox, -1, "",),
                         str(len(self.rec[0].seq))],
                        ['title','Title:',
                         wx.TextCtrl(self.frameBox, -1, ""),'']]
        self.FrameBoxFill()

    def Colors(self):
        self.colorDict = {'A':'b', 'C':'c', 'D':'r', 'E':'r', 'F':'b',
                          'G':'k', 'H':'y', 'I':'b', 'K':'y', 'L':'b',
                          'M':'b', 'N':'g', 'P':'k', 'Q':'g', 'R':'y',
                          'S':'g', 'T':'g', 'V':'b', 'W':'b', 'Y':'b',
                          'U':'m', 'O':'m', 'B':'g', 'Z':'g', 'J':'b',
                          'X':'w', ' ':'w', '.':'k', '-':'k'}

    def MessageDia(self, string):
        dialog = wx.MessageDialog(self.frame, string, 'Error', style=wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
                
    def CreateRecMat(self):
        self.recMat = []
        for seq in self.rec[0].seq:
            self.recMat.append([])
        for record in self.rec:
            for i,r in enumerate(record.seq):
                self.recMat[i].append(r)
                
    def CharSort(self):
        self.sort = []
        for r in self.recMat:
            self.sort.append([])
            temp = dict()
            chars = dict()
            sumV = 0
            for c in r:
                if not c in chars.keys():
                    chars[c] = 0.
                chars[c] += 1.
            for c in chars.keys():
                if not chars[c] in temp.keys():
                    temp[chars[c]] = []
                sumV += chars[c]
                temp[chars[c]].append(c)
            i = len(r)
            while i > 1:
                if i in temp.keys():
                    for x in temp[i]:
                        self.sort[-1].append([x,i])
                i -= 1
            self.sort[-1].append(sumV)

    def DoEnt(self):
        figWidth = self.bPSize[0] - 277
        xPos = 0
        yPos = 0
        seqLen = int(self.options[3][2].GetValue())
        seqLen -= int(self.options[2][2].GetValue())
        numLines = self.options[0][2].GetValue()
        cpr = seqLen / self.options[0][2].GetValue()
        if seqLen % self.options[0][2].GetValue() > 0:
            cpr += 1
        for i,s in enumerate(self.sort[:-1]):
            sV = s[-1]
            if i%cpr == 0:
                yPos = 1 - (int(i / cpr + 1) * 1. / numLines)
                xPos = 0
            yp = yPos
            for c in s[:-1]:
                fs = 720.*c[1]/sV*figWidth/473./seqLen*(numLines**.99)
                self.axes1.text(xPos, yp, c[0], fontsize = fs,
                                color = self.colorDict[c[0]], ha = 'left', 
                                fontproperties = self.font, va = 'bottom')
                yp += fs / 200.
            xPos += 2.*s[0][1]/sV*figWidth/473./seqLen*.7*(numLines**.8)

    def ShowImage(self, event):
        self.axes1.clear()
        self.plotter.remove()
        self.plotter.Show(False)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.font = FontProperties()
        self.font.set_name('Georgia')
        self.recMat = []
        self.CreateRecMat()
        self.CharSort()
        if self.options[1][2].GetValue() == 'entropy':
            self.DoEnt()
        else:
            self.DoProb()
        self.axes1.set_ylim(0,1)
        #self.axes1.set_xlim(0,len(self.rec[0].seq))
        self.axes1.axis('off')
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.plotter.Show(True)
        
    def GetExec(self, fr, bp, rec, cL):
        self.frame = fr
        self.bigPanel = bp
        self.bPSize = bp.GetSize()
        self.colorList = cL
        self.rec = rec
        self.CoverInit()
        self.OptionsInit()
        self.Colors()
        self.createButton = wx.Button(self.frame, -1, "CREATE",
                                      pos = (5,self.frame.GetSize()[1] - 35),
                                      size = (self.frame.GetSize()[0] - 10,25))
        self.frame.Bind(wx.EVT_BUTTON, self.ShowImage, self.createButton)
        self.frameBox.SetScrollbars(0, 1, 0, len(self.options)*30+13)
        self.frameBox.SetScrollRate(15, 35)

def GetName():
    return "RecLogo"
