import wx
import getPlugins as gpi
import os
import math
from Bio import SeqIO
from time import strftime
import re

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        for i in self.seqText:
            i.Show(False)
            i.SetSize((self.bPSize[0]-315,self.bPSize[1]-16))
            i.seqText.Show(True)
        self.frame.Show(False)
        self.frame.SetPosition((self.bPSize[0]-175,0))
        self.frame.SetSize((200,self.bPSize[1]-8))
        self.frame.Show(True)
        self.grayFrame.SetPosition((self.bPSize[0]-175, 0))
        self.grayFrame.SetSize((67, self.bPSize[1]))
        self.frame.SetSize((self.bPSize[0]-178,238))

    def Refresh(self,record):
        for s in self.seqText:
            s.Show(False)
        self.seqText = []
        self.GetExec(record)

    def Clear(self):
        for i in self.seqText:
            i.Show(False)
        self.frame.Show(False)
        self.saveCheck.Show(False)
        self.grayFrame.Show(False)

    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\NAViewPlugins")
        newFont = wx.Font(7, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                          wx.FONTWEIGHT_NORMAL)
        self.tabButtons = []
        yPos = 20
        for i,v in enumerate(self.views.values()):
            viewName = v.GetName()
            v = v.Plugin()
            self.tabButtons.append(wx.Button(
                self.grayFrame, -1, str(viewName), pos = (1,yPos),
                size = (63,22), style = wx.NO_BORDER))
            self.tabButtons[i].SetBackgroundColour(
                v.GetBackColor())
            self.tabButtons[i].SetForegroundColour(
                v.GetForeColor())
            self.tabButtons[i].SetFont(newFont)
            self.curView = v
            self.grayFrame.Bind(wx.EVT_BUTTON, self.DoButtonClicked,
                                self.tabButtons[i])
            yPos += 40

    def FrameInit(self):
        self.frame = wx.ScrolledWindow(self.bigPanel, -1, pos = (0, 0),
                                       size = (self.bPSize[0]-178, 238),
                                       style = wx.NO_BORDER|wx.VSCROLL)
        self.frame.SetBackgroundColour(self.colorList['ViewPanelList']['Back'])
        self.frame.Show(False)

    def GrayFrameInit(self):
        self.grayFrame = wx.Panel(self.bigPanel, -1, style = wx.BORDER_RAISED,
                                  size = (67, self.bPSize[1]),
                                  pos = (self.bPSize[0] - 175, 0))
        self.grayFrame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.grayFrame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.grayFrame.Show(False)

    def SaveCheckInit(self):
        self.saveCheck = wx.CheckBox(self.grayFrame, -1, label = "Save?",
                                 pos = (0,0))
        self.saveCheck.SetValue(False)
        self.saveCheck.Show(False)
        
    def Init(self, parent, bigPanel, colorList):
        self.colorList = colorList
        self.bigPanel = bigPanel
        self.bPSize = bigPanel.GetSize()
        self.hD = os.getcwd()
        self.par = parent
        self.seqText = []
        self.FrameInit()
        self.GrayFrameInit()
        self.TabButtonInit()
        self.SaveCheckInit()
        self.lastButton = ''
        self.minY = 3
        self.textBackCol = self.colorList['ViewPanelList']['Back']
        self.textForeCol = self.colorList['ViewPanelList']['Fore']
               
    def GetExec(self, rec):
        self.rec = rec[0][0]
        self.frame.Show(True)
        self.saveCheck.Show(True)            
        self.grayFrame.Show(True)
        self.DoView()

    def DoView(self):
        for f in self.frame.GetChildren():
            f.Show(False)
        self.textList = []
        self.textList.append(["Base", self.rec.seq, "WHITE", "BLACK"])
        self.DoPrint(13 * (len(self.textList)-1), self.rec.seq, "?")
        self.frame.SetScrollbars(0, 43, 0, len(self.rec.seq)/100)

    def DoPrint(self, yPos, seq, buttonName):
        lent = len(self.textList)
        lens = math.ceil((len(seq) / 105)) + 1
        i = 1
        while i < len(self.seqText):
            self.seqText[i].Show(False)
            p = self.seqText[i].GetPosition()
            self.seqText[i].SetPosition((p[0],p[1]+(13*(i%(lens)))))
            self.seqText[i].Show(True)
            i+=1
        newFont = wx.Font(7, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                          wx.FONTWEIGHT_NORMAL)
        i = 1
        while i <= lens:
            seq1 = seq[(i-1) * 105 : i * 105]
            tempSeq = wx.StaticText(self.frame, -1, str(seq1),
                                    size = (self.bPSize[0] * 525 / 747, 12),
                                    pos = (10,yPos+13*lent*(i)))
            tempSeq.SetBackgroundColour(self.textList[-1][2])
            tempSeq.SetForegroundColour(self.textList[-1][3])
            tempSeq.SetFont(newFont)
            self.seqText.append(tempSeq)            
            i+=1
        
    def RemoveText(self, t):
        lens = math.ceil((len(self.rec.seq) / 105)) + 1
        x = t * lens
        holdX = int(x)
        self.textList.pop(t)
        i = 1
        while i < len(self.seqText):
            self.seqText[i].Show(False)
            p = self.seqText[i].GetPosition()
            if i > x:
                xp = p[1]-(13*(i%(lens)+1))
            else:
                xp = p[1]-(13*(i%(lens)))
            self.seqText[i].SetPosition((p[0],xp))
            self.seqText[i].Show(True)
            i+=1
        while x < (t+1) * lens:
            self.seqText[holdX].Show(False)
            self.seqText.pop(holdX)
            x += 1

    def SaveText(self, seq, n, t, rec):
        d = strftime('%d%m%y')
        rn = str(re.sub('[\|,.]','_',rec.name))
        f = open(self.hD+r"/"+t+"/"+rn+"_"+n+"_"+d+r".fasta",'w')
        writeSeq = rec
        writeSeq.seq = seq
        SeqIO.write(writeSeq,f,'fasta')
        f.close()
        self.par.listView.ListRefill()
            
    def DoButtonClicked(self, event):
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                t = -1
                for i,name in enumerate(self.textList):
                    if name[0] == self.buttonLabel:
                        t = i
                if t > -1:
                    self.RemoveText(t)
                else:
                    name = v.GetName()
                    v = v.Plugin()
                    v.GetExec(self.frame, self.bigPanel, self.rec.seq)
                    seq = v.GetList()
                    self.textBackCol = v.GetBackColor()
                    self.textForeCol = v.GetForeColor()
                    self.textList.append([name, seq, self.textBackCol,
                                          self.textForeCol])
                    self.DoPrint(0, seq, name)
                    if self.saveCheck.GetValue():
                        self.SaveText(seq, name, v.GetType(), self.rec)

    def GetType(self):
        return "Nucleic Acids"

    def GetName(self):
        return "NAView"

def GetType():
    return "Nucleic Acids"

def GetName():
    return "NAView"
