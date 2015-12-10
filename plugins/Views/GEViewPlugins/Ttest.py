import wx
import math
import tTestClass as ttc
import listControl as lc

class Plugin():
    def GetParamList(self):
        return self.rec

    def GetName(self):
        return "T-Test"

    def GetGeMat(self):
        return self.geMat


    def AlphaInit(self):
        self.aOpt = ['0.05', '0.01', '0.001', 'other']
        self.alphaText = wx.StaticText(self.coverPanel, -1,
                                       pos = (10, self.bPSize[1]/2 - 50),
                                       label = "alpha value:")
        self.alphaChoice = wx.ComboBox(self.coverPanel, -1, choices = self.aOpt,
                                       pos = (10, self.bPSize[1]/2 - 30),
                                       size = (55, -1), style = wx.CB_READONLY)
        self.alphaChoice.SetSelection(0)
        #self.alphaChoice.Bind(wx.EVT_COMBOBOX, self.OnCombo)

    def Test(self, event):
        a = self.alphaChoice.GetSelection()
        if a == 3:
            #ToDo: add popup asking for alpha value
            a = 0
        probes = self.geMat[-1]
        temp = GetExec(self.rec, self.geMat, float(self.aOpt[a]))
        self.geMat = temp[0]
        listData = dict()
        for j, ps in enumerate(probes):
            listData[j] = (str(ps), temp[1][j], temp[2][j], temp[3][j])
        self.list.Refill(listData)
        self.list.Show(True)
        
    def ButtonInit(self):
        self.button = wx.Button(self.coverPanel, -1,
                                     "Test", size = (55, -1),
                                     pos = (10, self.bPSize[1]/2),
                                     style = wx.NO_BORDER)
        self.button.SetBackgroundColour('RED')
        self.button.SetForegroundColour('WHITE')
        self.coverPanel.Bind(wx.EVT_BUTTON, self.Test)

    def ListInit(self):
        self.list = lc.TestListCtrl(self.coverPanel, -1, size = (75,10),
                                    pos = (self.bPSize[0] - 100,
                                           self.bPSize[1] - 20),
                                    style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                    numCols = 4)
        cols = ['ProbeSet ID', 't-value', 'dof', 'p-score']
        space = (self.bPSize[0] - 100) / 4. - 15
        colWidths = [space + 30, space, space, space]
        self.list.Fill(cols, colWidths)
        self.list.Show(False)

    def GetExec(self, frame, coverPanel, rec, geMat, colorList):
        self.rec = rec
        self.geMat = geMat
        self.coverPanel = coverPanel
        self.bPSize = coverPanel.GetSize()
        self.AlphaInit()
        self.ButtonInit()
        self.ListInit()
        #return GetExec(rec, geMat, 0.05)

def GetExec(rec, geMat, alpha):
    tc = ttc.tTestClass()
    return [tc.GetExec(rec, geMat, alpha), tc.GetTScores(),
            tc.GetDof(), tc.GetPMat()]
        
def CalculateTCDF(t, df):
    step = t / 1000.
    iters = 0.
    rollingSum = 0.
    
    numerator = math.gamma((df + 1)/2)
    denominator1 = math.gamma(df / 2)
    denominator2 = math.sqrt(df * math.pi)
    while iters < t-.001:
        denominator3 = (1 + (iters ** 2 / df)) ** ((df + 1) / 2)
        tpdf1 = (numerator / denominator1 / denominator2 / denominator3)
        iters += step
        denominator3 = (1 + (iters ** 2 / df)) ** ((df + 1) / 2)
        tpdf2 = (numerator / denominator1 / denominator2 / denominator3)

        rollingSum += step * (tpdf1 + tpdf1) / 2
    return 1-(rollingSum + 0.5)

        
def GetName():
    return "T-Test"







"""The Simpsons: Season 4, Episode 6 
Itchy & Scratchy: The Movie (3 Nov. 1992)

Homer:  Bart, didn't I ask you to watch Maggie?
Bart:   Sounds like something you'd say...
<cut to Maggie>
  Maggie is driving Homer's car down the street.  ...
  The car finally slams into the Springfield Correctional
  Institute, the air bag breaks Maggie's fall, and provides a
  convenient pillow for her afternoon nap. Several inmates escape.
Snake:  All right! Time for a crime spree!
<cut to living room>
  As Homer punishes Bart, Snake runs across the front lawn carrying
  an electronic device.
<cut to Snake examining his plunder>
Snake: Oh no! Beta!


http://www.snpp.com/episodes/9F03.html"""
