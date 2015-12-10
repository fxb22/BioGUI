import wx
import os
import time
import re
from xml.dom import minidom
import tarfile
import listControl as lc

class SelectionDialog(wx.Dialog):    
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, title='Sample Selection Dialog',
                           size=(1500, 500))

    def GetButtons(self):
        self.buttons = []
        labels = ['Add', 'Add', 'Remove', 'Remove', 'Done']
        xp = [1300, 1300, 1300, 1300, 1370]
        yp = [80, 300, 145, 365, 219]
        col = ['GRAY', 'GRAY', 'RED', 'RED', 'BLUE']
        meth = [self.Add, self.Add, self.Remove,
                self.Remove, self.OnClose]
        for i,l in enumerate(labels):
            self.buttons.append(wx.Button(self.BigPanel, -1, l,
                                          pos=(xp[i], yp[i])))
            self.buttons[-1].SetBackgroundColour(col[i])
            self.buttons[-1].SetForegroundColour('WHITE')
            self.Bind(wx.EVT_BUTTON, meth[i], self.buttons[-1])
            
    def CntrlFill(self, l):
        #Method to create list control column headers
        cols = ['Accession', 'Title']
        colWidths = [75, 475]
        l.Fill(cols, colWidths)

    def GetLC(self):
        # listcontrol size and position not flipped
        # flipped position and size below
        self.lcLeft = lc.TestListCtrl(self.BigPanel, -1,
                                      size=(50,35), pos=(550,420),
                                      style=wx.LC_REPORT|wx.LC_VIRTUAL,
                                      numCols = 2)
        self.CntrlFill(self.lcLeft)
        self.lcTop = lc.TestListCtrl(self.BigPanel, -1,
                                     size=(700,35), pos=(550,175),
                                     style=wx.LC_REPORT|wx.LC_VIRTUAL,
                                     numCols = 2)
        self.CntrlFill(self.lcTop)
        self.lcTop.itemDataMap = dict()
        self.lcLow = lc.TestListCtrl(self.BigPanel, -1,
                                     size=(700,255), pos=(550,175),
                                     style=wx.LC_REPORT|wx.LC_VIRTUAL,
                                     numCols = 2)
        self.CntrlFill(self.lcLow)
        self.lcLow.itemDataMap = dict()

    def GetText(self):
        self.leftText = wx.StaticText(self.BigPanel, -1, "Record Samples",
                                      size=(100,25), pos=(275,10))
        self.topText = wx.StaticText(self.BigPanel, -1, "Group one",
                                     size=(100,25), pos=(915,10))
        self.lowText = wx.StaticText(self.BigPanel, -1, "Group two",
                                     size=(100,25), pos=(915,230))

    def View(self, parent, rec, colorList):
        self.parnt = parent
        self.colorList = colorList
        self.Bind(wx.EVT_CLOSE, self.OnClose)        
        self.BigPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER,
                                 size=(1500,500))
        self.fSize = self.GetSize()
        self.BigPanel.SetBackgroundColour(
            self.colorList['Main']['Back'])
        self.GetButtons()
        self.GetText()
        self.GetLC()
        self.CntrlFill(self.lcLeft)
        self.FillLeft(rec)
        self.topList = []
        self.lowList = []

    def DoCel(self, name):
        import ESearch
        import ESummary
        early = ESearch.GetExec('gds',str(name[0][:-8]))
        er = ESummary.GetExec('gds',str(early["IdList"][0]))
        l = 0
        while l < len(er.split('\n')):
            line = er.split('\n')[l]
            s = '.*<Item Name="GPL" Type="String">'
            if not re.search(s,line) == None:
                e = re.sub(s,'',line)
                gpl = e.split(r'<')
                #self.parnt.platform = self.parnt.pfTranslate[int(gpl[0])]
            else:
                s = '.*<Item Name="Accession" Type="String">'
                if not re.search(s,line) == None:
                    e = re.sub(s,'',line)
                    accnum = e.split(r'<')[0]
                    l += 1
                    line = er.split('\n')[l]
                    e = re.sub('.*<Item Name="Title" Type="String">','',line)
                    title = e.split(r'<')[0]
                    self.leftList.append([accnum, title])
            l += 1

    def DoMinimal(self, name):
        f = self.filelib.extractfile(name)
        m = minidom.parse(f).childNodes[0]
        i = 1
        while i < len(m.childNodes):
            if str(m.childNodes[i].localName) == "Sample":
                title = m.childNodes[i].childNodes[3].childNodes[0].toxml()
                accnum = m.childNodes[i].childNodes[5].childNodes[0].toxml()
                self.leftList.append([accnum, title])
            i += 2
            
    def FillLeft(self, rec):
        self.leftList = []
        os.chdir(r'.\Records\Gene Expressions')
        ftime = open(r'.\lastChecked.txt','r')
        prevTime = float(ftime.readline())
        ftime.close()
        """if len(Rec) < 2:
            if float(fmt.filemtime(Rec)) <= prevTime:
                self.filelib = tarfile.TarFile.gzopen(Rec)
            elif Rec[-4:] == '.tgz':
                self.filelib = tarfile.TarFile.taropen(Rec)
        elif Rec[0][-4:] == r'.tar':
            self.filelib = tarfile.TarFile.taropen(Rec)
        else:
            self.filelib = 'empty'"""
        self.filelib = tarfile.TarFile.gzopen(rec)
        #make so that it reads pickles
        if not self.filelib == 'empty':
            nameHolder = self.filelib.getnames()
            if nameHolder[0][-3:] == r'.gz':
                if nameHolder[0][-7:] == r'.CEL.gz':
                    self.DoCel(rec)                  
            elif nameHolder[0][-4:] == r'.xml':
                self.DoMinimal(nameHolder[0])
            listData = dict()
            for j,k in enumerate(self.leftList):
                listData[j] = k
            self.lcLeft.Refill(listData)

    def Add(self, event):
        obj = event.GetEventObject()
        pos = obj.GetPosition()[1]
        if pos > 200:
            obj = self.lcLow
        else:
            obj = self.lcTop
        sel = self.lcLeft.GetSelected()
        dataMap = obj.GetDataMap()        
        for s in sel:
            k = self.leftList[s]
            if k[0] in dataMap:
                x = 1
                while str(k[0] + str(x)) in dataMap:
                    x += 1
                dataMap[k[0] + str(x)] = k
            else:
                dataMap[k[0]] = k
        obj.Refill(dataMap)
        if pos > 200:
            self.lowList = dataMap.keys()
        else:
            self.topList = dataMap.keys()

    def Remove(self, event):
        obj = event.GetEventObject()
        pos = obj.GetPosition()[1]
        if pos > 200:
            obj = self.lcLow
            l = self.lowList
        else:
            obj = self.lcTop
            l = self.topList
        dataMap = obj.GetDataMap()
        for s in obj.GetSelected():
            del dataMap[l[s]]
        obj.Refill(dataMap)
        
    def OnClose(self, event):
        accnums = []
        accnums.append(self.lcTop.itemIndexMap)
        accnums.append(self.lcLow.itemIndexMap)
        self.parnt.SetGroups(accnums)
        self.Destroy()

class Plugin():
    def GetParamList(self):
        return self.accnums

    def SetGroups(self,acc):
        self.accnums = acc

    def GetExec(self, frame, BigPanel, rec, geMat, colorList):
        s = SelectionDialog()
        self.geMat = geMat
        s.View(self, rec, colorList)
        s.ShowModal()

    def GetGeMat(self):
        return self.geMat

def GetExec(rec, geMat, alpha):
    s = SelectionDialog()
    s.View(self, rec, colorList)
    s.ShowModal()

def GetName():
    return "Selection"
