import wx
import getPlugins as gpi
import os
import subprocess
import AffyWorx
import tarfile

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        self.grayFrame.SetPosition((self.bPSize[0] - 307, 0), -1)
        self.grayFrame.SetSize((200, self.bPSize[1] - 8))
        self.coverPanel.SetSize((self.bPSize[0] - 307, self.bPSize[1]))
        self.coverPanel.SetPosition((0, 0))
        
    def Refresh(self,record):
        self.GetExec(record)

    def Clear(self):
        self.grayFrame.Show(False)
        self.coverPanel.Show(False)
        for o in self.coverPanel.GetChildren():
            o.Destroy()

    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\GEViewPlugins")
        self.tabButtons = []
        self.selPos = -1
        yPos = 10
        xPos = 10
        for i,v in enumerate(self.views.values()):
            viewName = v.GetName()
            if viewName == 'Selection':
                self.selPos = i
            v = v.Plugin()
            self.tabButtons.append(wx.Button(
                self.grayFrame, -1, str(viewName), pos = (xPos, yPos),
                size = (62, 22), style = wx.NO_BORDER))
            self.tabButtons[i].SetBackgroundColour(
                self.colorList['ViewPanelGrayFrame']['Back'])
            self.tabButtons[i].SetForegroundColour(
                self.colorList['ViewPanelGrayFrame']['Fore'])
            self.curView = v
            self.grayFrame.Bind(wx.EVT_BUTTON, self.DoButtonClicked,
                                self.tabButtons[i])
            if xPos < 120:
                xPos += 60
            else:
                xPos = 10
                yPos += 22
        self.lastButton = self.tabButtons[0]

    def GrayFrameInit(self):
        self.grayFrame = wx.Panel(self.bigPanel, -1, style = wx.RAISED_BORDER,
                                  size = (200, self.bPSize[1]),
                                  pos = (self.bPSize[0] - 307, 0))
        self.grayFrame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.grayFrame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.grayFrame.Show(True)
        self.coverPanel = wx.Panel(self.bigPanel, -1, style = wx.NO_BORDER,
                                   size = (self.bPSize[0]-300, self.bPSize[1]),
                                   pos = (0, 0))
        self.coverPanel.SetBackgroundColour(
            self.colorList['ViewPanelList']['Back'])
        self.coverPanel.Show(True)   
    
    def Init(self, parent, bigPanel, colorList):
        self.colorList = colorList
        self.bigPanel = bigPanel
        self.bPSize = bigPanel.GetSize()
        self.hD = os.getcwd()
        self.par = parent
        self.timesCalled = 0
        self.GrayFrameInit()
        self.TabButtonInit()
        
    def GetExec(self, rec):
        self.rec = rec[0][0]
        self.groups = self.rec
        self.geMat = []
        self.bPSize = self.bigPanel.GetSize()
        self.grayFrame.Show(True)
        self.coverPanel.Show(True)

    def minimalreader(self, itsgo, j):
        if self.rec[-8:] == '.xml.tgz':
            if itsgo[:3] == r"GSM":
                self.geMat[j].append(str(itsgo))
                f = self.filelib.extractfile(itsgo + r'-tbl-1.txt')
                rows = [line.split('\t') for line in f]
                for r in rows:
                    self.geMat[j].append(float(r[1]))
                j += 1
                if j == 1:
                    for r in rows:
                        self.geMat[-1].append(r[0])

    def tarreader(self, itsgo):
        if self.rec[-4:] == r'.tar':
            os.chdir(self.hD)
            if not pset:
                pfc = open(r'.\Gene Expressions\GPL\PlatformConvert.txt')
                for lines in pfc.read().split('\n'):
                    l = lines.split('\t')
                    if l[0] == self.Rec[0][1]:
                        b = l[4].split(']')
                        platform = b[0][1:]
                pset = True
                pfc.close()
                AffyWorx.worx(platform)
            lenX = 0
            for n in nameHolder:
                if n[-7:] == r'.CEL.gz':
                    lenX += 1
            p = subprocess.Popen(r'C:\Program Files (x86)\py27\python.exe '+self.homeDir+r'\Utils\AffyWorx.py')
            p.wait()
            k = len(nameHolder)
        self.filelib.extractall('.\CurrentCel')
        
    def DoView(self):
        #os.chdir(self.hD + r'\Gene Expressions')       
        if self.rec[-4:] == '.tgz':
            self.filelib = tarfile.TarFile.gzopen(self.rec)
        elif self.rec[-4:] == r'.tar':
            self.filelib = tarfile.TarFile.taropen(self.rec)
        self.groups = self.curView.GetParamList()
        pset = False
        if self.buttonLabel == 'Selection':
            nameHolder = []
            self.sampleList = self.groups[0]
            for g in self.groups[0]:
                nameHolder.append(g)
                self.geMat.append([])
            for g in self.groups[1]:
                nameHolder.append(g)
                self.geMat.append([])
            self.geMat.append([])
            k = 0
            while k < len(nameHolder):
                itsgo = nameHolder[k]
                if self.rec[-4:] == '.tgz':
                    self.minimalreader(itsgo, k)
                else:
                    self.tarreader(itsgo)
                k += 1
        #self.rec = self.sampleList        
   
    def DoButtonClicked(self, event):
        for o in self.coverPanel.GetChildren():
            o.Show(False)
            o.Destroy()
        if self.lastButton.GetLabelText() == "T-Test":
            self.geMat = self.curView.GetGeMat()
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                name = v.GetName()
                self.curView = v.Plugin()
                self.curView.GetExec(self.grayFrame,
                                     self.coverPanel, self.groups,
                                     self.geMat, self.colorList)
        self.DoView()
                   
    def GetType(self):
        return "Gene Expressions"

    def GetName(self):
        return "GEView"

def GetType():
    return "Gene Expressions"

def GetName():
    return "GEView"
