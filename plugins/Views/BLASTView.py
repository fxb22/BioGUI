import wx
import listControl as lc
import getPlugins as gpi
from decimal import Decimal
import os

class Plugin():
    def OnSize(self):
        # Respond to size change
        self.bPSize = self.bigPanel.GetSize()
        self.list.SetSize((self.bPSize[0] - 118, self.bPSize[1] - 40))
        self.ButtonShow(False)
        self.SetButtons()
        self.ButtonShow(True)

    def Refresh(self,record):
        self.GetExec(record)

    def Clear(self):
        self.list.Show(False)
        self.ButtonShow(False)
    
    def ButtonShow(self,tf):
        for b in self.buttons:
            b.Show(tf)

    def SetButtons(self):
        self.views = gpi.GetPlugIns(
            self.hd+r"\plugins\Views\BLASTViewPlugins")
        xPos = 300
        self.buttons = []
        for v in self.views.values():
            self.buttons.append(wx.Button(self.bigPanel, -1,
                                          str(v.GetName()),
                                          pos = (self.bPSize[0] * xPos / 747,
                                                 self.bPSize[1] - 35),
                                          size = (90, 22),
                                          style = wx.NO_BORDER))
            self.buttons[-1].SetBackgroundColour(
                self.colorList[v.GetColors()]['Back'])
            self.buttons[-1].SetForegroundColour(
                self.colorList[v.GetColors()]['Fore'])
            xPos += 100
            self.bigPanel.Bind(wx.EVT_BUTTON, self.DoView, self.buttons[-1])

    def Init(self, parent, bigPanel, colorList):
        self.hd = os.getcwd()
        self.colorList = colorList
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.list = lc.TestListCtrl(self.bigPanel, -1, size = (0,0),
                                    pos = (self.bPSize[0] - 118,
                                           self.bPSize[1] - 40),
                                    style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                    numCols = 7)
        self.list.SetBackgroundColour(
            self.colorList['ViewPanelList']['Back'])
        self.list.SetForegroundColour(
            self.colorList['ViewPanelList']['Fore'])
        self.SetButtons()
        self.ListCntrlFill()
        self.list.Show(True)
        self.ButtonShow(False)
               
    def GetExec(self, Rec):
        self.SetButtons()
        self.list.Show(True)
        self.ButtonShow(True)
        self.BlastRec = Rec[0]
        self.OnSelect(wx.EVT_IDLE)
        
    def ListRefill(self):
        listData = dict()
        j = 0
        for alignment in self.BlastRec.alignments:
            for hsp in alignment.hsps:
                listData[j] = (str(alignment.title), alignment.length,
                               hsp.score,
                               Decimal(hsp.expect).quantize(Decimal(10) ** -5),
                               hsp.identities, hsp.positives, hsp.gaps)
                j += 1
        self.list.Refill(listData)
        
    def ListCntrlFill(self):
        cols = ['Title', 'Length', 'Score', 'E Values',
                'Idents.', 'Posits.', 'Gaps']
        colWidths = [318, 50, 50, 59, 48, 48, 40]
        self.list.Fill(cols, colWidths)

    def OnSelect(self, event):                    
        self.ListCntrlFill()
        self.ListRefill()

    def RecInfo(self):
        pos = self.list.GetSelected()
        matches = ['']
        seqs = []
        titles = []
        alignment = self.BlastRec.alignments[self.list.itemIndexMap[0]]
        titles.append('query')
        for p in pos:
            alignment = self.BlastRec.alignments[self.list.itemIndexMap[p]]
            for hsp in alignment.hsps:
                query = ''
                i = 1
                strtblnk = ''
                while i < hsp.query_start:
                    strtblnk += '-'
                    query += self.BlastRec.alignments[0].hsps[0].query[i-1]
                    i += 1
                query += hsp.query
                i = 0
                endblnk = ''
                j = len(strtblnk)+len(hsp.query)
                while i + j < len(self.BlastRec.alignments[0].hsps[0].query):
                    endblnk += '-'
                    query += self.BlastRec.alignments[0].hsps[0].query[j+i]
                    i += 1
                t = str(alignment.title).split('|')
                titles.append(str(t[0] + '|' + t[1]))
                matches.append(strtblnk + str(hsp.match) + endblnk)
                seqs.append(query)
                seqs.append(strtblnk + str(hsp.sbjct) + endblnk)
        return [matches,seqs,titles]

    def DoView(self,event):
        for v in self.views.values():
            if v.GetName() == event.GetEventObject().GetLabelText():
                v.Plugin().GetExec(self.RecInfo(), self.bigPanel, self.hd,
                                   self.BlastRec.alignments,
                                   self.BlastRec.application)

    def GetType(self):
        return "Blast Results"

    def GetName(self):
        return "BLASTView"

def GetType():
    return "Blast Results"

def GetName():
    return "BLASTView"
