import wx
import os
import math
import numpy as np
import Ttest
import HeatMap
import sqlite3
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
import wx.lib.mixins.listctrl  as  listmix
import random
import time

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    #List Control to display available objects
    
    def __init__(self, parent, ID, style, pos=(5,49), size=(88,148)):
        #Simple constructor for list. Calls and initializes a wxListCtrl window
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, 3)

    def GetListCtrl(self):
        #List control accessor method
        return self

    def SortItems(self,sorter=cmp):
        #Method to allow sorting of objects
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        
        # redraw the list
        self.Refresh()

    def OnGetItemText(self, item, col):
        #Required List Control method
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s

class Plot(wx.Panel):
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, size=(1000,1500), **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2.9,2.75), facecolor='w')
        self.canvas = Canvas(self, -1, self.figure)
        self.SetBackgroundColour('WHITE')
        #self.toolbar = Toolbar(self.canvas)
        #self.toolbar.Realize()

class PlotNotebook(wx.Panel):
    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id=id, size=(2250,5000), pos=(-40,-32))

    def add(self,name="plot"):
       page = Plot(self)
       
       return page.figure


class Plugin():
    def GetParamList(self):
        return self.geoMat

    def GetName(self):
        return "Binary"

    def GetExec(self, frame, BigPanel, Rec, geoMat, colorList):
        
        self.BigPanel = BigPanel
        bpSize = self.BigPanel.GetSize()

        self.statText1 = wx.StaticText(self.BigPanel, -1, "Results to\n   Show:", size=(75, -1), pos=(193,62))
        searchButton = wx.Button(self.BigPanel, -1, "Search GBDB", pos=(188,bpSize[1]/2 + 10), size=(90,22), style=wx.NO_BORDER)
        self.BigPanel.Bind(wx.EVT_BUTTON, self.doSearch, searchButton)

        self.BigPanel.NumGen = wx.SpinCtrl(self.BigPanel, -1, size=(75, -1), pos=(188,90))
        self.BigPanel.NumGen.SetValue(5)

        self.mat2save = pluginEXE(Rec,geoMat, -1)

        self.lc = TestListCtrl(self.BigPanel, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL)
        self.BigPanel.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.lc)
        
        #self.lc.SetBackgroundColour(colorList[5][0])
        #self.lc.SetForegroundColour(colorList[5][1])
        musicdata = dict()
        self.ListCntrlFill()

        mat2plot = []
        i = 0
        while i < 17300:
            mat2plot.append(2)
            i += 1

        i = 0
        #print len(self.mat2save[1])
        while i < len(self.mat2save[0]):
            pos = self.mat2save[0][i]
            #print i
            #print pos
            mat2plot[int(pos)+700]=self.mat2save[1][i]
            musicdata[i] = int(pos),self.mat2save[1][i]
            i += 1

        self.lc.itemIndexMap = musicdata.keys()
        self.lc.itemDataMap = musicdata
        self.lc.SetItemCount(i)
        
        mat2plot = np.array([mat2plot])
        #print mat2plot.transpose()
        self.BigPanel.plotPanel = wx.Panel(self.BigPanel, -1, style=wx.RAISED_BORDER, pos=(98,39), size=(80,169))
        self.BigPanel.plotPanel.SetBackgroundColour('NAVY')
        self.BigPanel.plotter = PlotNotebook(self.BigPanel.plotPanel)
        self.BigPanel.axes1 = self.BigPanel.plotter.add('figure 1').gca()
        plt.spectral()
        c = self.BigPanel.axes1.pcolor(mat2plot.transpose(),vmin=-1,vmax=1.1)
        self.BigPanel.axes1.set_ylim(0,18000)
        self.BigPanel.axes1.set_xlim(0,1)
        return []

    def doSearch(self,event):
        rankings = binarysearchEXE(self.mat2save,self.BigPanel.NumGen.GetValue())

        #wx.CallAfter(self.rankBox.SetInsertionPoint, 0)
        print rankings

    def OnColClick(self, event):
        #Respond to mouse click of list column header
        self.col2Sort = event.GetColumn()
        if self.col2Sort == self.colsort:
            self.sortvar = abs(self.sortvar-1)
        else:
            self.sortvar=1
        self.colsort=self.col2Sort
        
        self.lc.SortListItems(self.col2Sort,ascending=self.sortvar)

    def ListCntrlFill(self):
        #Method to create list control column headers
        self.lc.ClearAll()
        self.lc.InsertColumn(0, 'DBN')
        self.lc.InsertColumn(1, "Dir")

        self.lc.SetColumnWidth(0, 42)
        self.lc.SetColumnWidth(1, 27)

def pluginEXE(Rec, geoMat, numToGen):
    #Assume that record is loaded, but not tested
    #Apply ttest and heat map bit to record
    #look up platform from sqliteDB and translate to 570Plus
    #
    #Display binary as 1,0s and colors
    #button to compare to other binaries (may take time :-(
    #List ~20 most similar?
    
    geoMat = Ttest.pluginEXE(Rec,geoMat,0.05)
    PSids = geoMat[-1]
    colMat = HeatMap.pluginEXE(Rec,geoMat,'bit')
    #print "a ok"
    con = sqlite3.connect(r"C:\Users\francis\Documents\platforms\AffyHuman.sqlite")
    c = con.cursor()
    mat2save = [[],[]]
    
    pos = 0
    #print len(PSids)
    #print len(colMat)
    while pos < len(PSids):
        #print pos
        query = PSids[pos]
        c.execute('''select Homolog from %s where AffyPSId = ?''' %Rec[1], [query])
        Hlog = c.fetchone()
        if not Hlog == None:
            c.execute('''select Position from GPL570Plus where Homolog = ?''', [Hlog[0]])
            hLogPos = c.fetchone()
            if not hLogPos == None:
                nLogPos = int(hLogPos[0])
                if not nLogPos == 15:
                    if not hLogPos in mat2save[0]:
                        mat2save[0].append(nLogPos)
                        mat2save[1].append(colMat[pos])
                    else:
                        seeker = 0
                        while seeker < len(mat2save[0]):
                            if mat2save[0][seeker] == nLogPos:
                                if not colMat[pos] == mat2save[1][seeker]:
                                    mat2save[1].pop(seeker)
                                    mat2save[0].remove(nLogPos)
                                seeker = len(mat2save[0])
                            seeker += 1
        pos += 1
    con.close()
    #print "b ok"
    if numToGen > 0:
        return binarysearchEXE(mat2save,numToGen)
    else:
        return mat2save

def binCount(temp):
    retr = 0
    while temp > 0:
        retr += 1
        temp1 = temp - 1
        temp = temp & temp1

    return retr

def binarysearchEXE(mat2save,numToGen):
    #return [[2,'2'],[2,'3']]

    scoreMat = []
    sand = os.getcwd()
    os.chdir(r"D:\francis\bitfingstuff")

    con = sqlite3.connect(r"GeoBinaryDB.sqlite")
    c = con.cursor()

    qbin = []
    i = 0
    while i < 16600:
        qbin.append(0)
        i += 1

    i = 0
    while i < len(mat2save[1]):
        if qbin[mat2save[0][i]] > 0:
            if not queryBin[mat2save[0][i]] == mat2save[1][i]:
                qbin[mat2save[0][i]] = 0
        else:
            qbin[mat2save[0][i]] == 2 + mat2save[1][i]
        i += 1
    print "wait"    
    queryBin = []
    rowCtr = 0
    while rowCtr < 16600:
        comp = 0
        comptimes = 0
        while comptimes < 25:
            comp = comp << 2
            comp += qbin[rowCtr]
            comptimes += 1
            rowCtr += 1
        queryBin.append(comp)

    odds = 0
    i = 0
    while i < 25:
        odds = odds << 2
        odds += 2
        i += 1
    print "wait some more"
    queryN = 0
    i = 0
    while i < 664:
        queryN += binCount(queryBin[i] & odds)
        i += 1
        
    print 'start clock'
    #print bin2save
    time.clock()
    toll = 0
    colNames = []
    c.execute(''' select name from sqlite_master where type="table"''')
    tableNames = c.fetchall()
    for tn in tableNames:
        print tn
        c.execute('''SELECT * FROM %s''' %tn[0])
        col_name_list = [cn[0] for cn in c.description]
        bigMat = c.fetchall()
        #print bigMat[10]
        col = 1
        while col < len(col_name_list):
            savings = []
            N11 = 0
            N00 = 0
            Nxx = 0
            totalN = queryN
            cols = col_name_list[col]
            rowCtr = 0
            while rowCtr < 664:
                savings.append(int(bigMat[rowCtr][col]))
                rowCtr += 1
            colNames.append(cols)

            iconfused = 0

            while iconfused < 664:
                totalN += binCount(savings[iconfused] & odds)
                
                andkey = queryBin[iconfused]&savings[iconfused]
                orkey = queryBin[iconfused]|savings[iconfused]
                xorkey = queryBin[iconfused]^savings[iconfused]

                N00 += 25 - binCount(xorkey & odds)

                bTemp = andkey & odds
                Nxx += binCount((bTemp >> 1) & xorkey)
                Nxx += binCount(xorkey & odds)

                iconfused += 1

            N11 = 16600 - N00 - Nxx                
            p = totalN / 33200.
            
            scoreMat.append([cols,((((2.0-p)/3.0)*N11/totalN)+(((1.0+p)/3.0)*N00/(33200-totalN)))*10000])
            col += 1
            toll += 1
        print toll
            
    i = 0
    ranker = []
    while i <= 5000:
        ranker.append([])
        i += 1

    ranked = []
    for namscor in scoreMat:
        ranker[int(math.floor(namscor[1]))].append(namscor)

    random.seed()
    i = 5000
    j = 0
    while j < numToGen:
        if len(ranker[i]) > 0:
            ranInt = random.randint(0,len(ranker[i])-1)
            ranked.append(ranker[i][ranInt])
            ranker[i].pop(ranInt)
            j += 1
        else:
            i -= 1
    os.chdir(sand)
    return ranked
            



def GetName():
    return "Binary"








        
