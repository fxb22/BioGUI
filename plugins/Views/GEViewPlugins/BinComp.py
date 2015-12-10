import wx
import os
import math
import numpy as np
import Catche
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
import wx.lib.mixins.listctrl  as  listmix


class Plot(wx.Panel):
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, size=(1000,5000), **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2.9,12.0), facecolor='w')
        self.canvas = Canvas(self, -1, self.figure)
        self.SetBackgroundColour('WHITE')
        #self.toolbar = Toolbar(self.canvas)
        #self.toolbar.Realize()

class PlotNotebook(wx.Panel):
    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id=id, size=(2250,15000), pos=(-40,-110))

    def add(self,name="plot"):
       page = Plot(self)
       
       return page.figure


class Plugin():
    def GetParamList(self):
        return self.geoMat

    def GetName(self):
        return "BinComp"

    def GetExec(self, frame, BigPanel, Rec, geoMat, colorList):
        
        self.BigPanel = BigPanel
        bpSize = self.BigPanel.GetSize()

        searchButton = wx.Button(self.BigPanel, -1, "Search GBDB", pos=(300,bpSize[1]/2 + 10), size=(90,22), style=wx.NO_BORDER)
        self.BigPanel.Bind(wx.EVT_BUTTON, self.doSearch, searchButton)

        self.box1=wx.TextCtrl(self.BigPanel, -1, '', size=(100, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,5))


        self.box2=wx.TextCtrl(self.BigPanel, -1, '', size=(100, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(200,5))
            
        self.box3=wx.TextCtrl(self.BigPanel, -1, '', size=(100, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(450,bpSize[1]/2 + 10))
        self.box3.write('THIS IS A WEBSITE')
        self.BigPanel.plotPanel = wx.Panel(self.BigPanel, -1, style=wx.RAISED_BORDER, pos=(98,39), size=(80,370))
        self.BigPanel.plotPanel2 = wx.Panel(self.BigPanel, -1, style=wx.RAISED_BORDER, pos=(98,39), size=(80,370))
        
        #print mat2plot.transpose()
        


        
        

        
        return []

    def doSearch(self,event):
        self.BigPanel.plotPanel2.Show(False)
        self.BigPanel.plotPanel.Show(False)
        f1=self.box1.GetValue()
        print f1
        f2=self.box2.GetValue()
        print f2
        self.mat2save=[[],[]]
        self.mat2save[0] = Catche.opickle(r"C:\Users\francis\Documents\DatabaseFingerprints/" + f1 + ' sig')
        self.mat2save[1] = Catche.opickle(r"C:\Users\francis\Documents\DatabaseFingerprints/" + f1 + ' updown')

        mat2plot1 = []
        i = 0
        while i < 17300:
            mat2plot1.append(2)
            i += 1


        i=0
        while i < len(self.mat2save[0]):
            pos = self.mat2save[0][i]
            #print pos
            mat2plot1[int(pos)+700]=self.mat2save[1][i]
            i += 1
        
        mat2plot1 = np.array([mat2plot1])
        self.BigPanel.plotPanel = wx.Panel(self.BigPanel, -1, style=wx.RAISED_BORDER, pos=(98,39), size=(80,770))
        self.BigPanel.plotPanel.SetBackgroundColour('NAVY')
        self.BigPanel.plotter = PlotNotebook(self.BigPanel.plotPanel)
        self.BigPanel.axes1 = self.BigPanel.plotter.add('figure 1').gca()
        plt.spectral()
        c = self.BigPanel.axes1.pcolor(mat2plot1.transpose(),vmin=-.1,vmax=1.1)
        self.BigPanel.axes1.set_ylim(0,18000)
        self.BigPanel.axes1.set_xlim(0,1)

        self.mat2save=[[],[]]
        self.mat2save[0] = Catche.opickle(r"C:\Users\francis\Documents\DatabaseFingerprints/" + f2 + ' sig')
        self.mat2save[1] = Catche.opickle(r"C:\Users\francis\Documents\DatabaseFingerprints/" + f2 + ' updown')

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
            i += 1

        mat2plot = np.array([mat2plot])
        self.BigPanel.plotPanel2 = wx.Panel(self.BigPanel, -1, style=wx.RAISED_BORDER, pos=(200,39), size=(80,770))
        self.BigPanel.plotPanel2.SetBackgroundColour('NAVY')
        self.BigPanel.plotter2 = PlotNotebook(self.BigPanel.plotPanel2)
        self.BigPanel.axes2 = self.BigPanel.plotter2.add('figure 1').gca()
        
        plt.spectral()
        c = self.BigPanel.axes2.pcolor(mat2plot.transpose(),vmin=-.1,vmax=1.1)
        self.BigPanel.axes2.set_ylim(0,18000)
        self.BigPanel.axes2.set_xlim(0,1)

        match=0.0
        for i,v in enumerate(mat2plot[0]):
            if mat2plot[0][i] == mat2plot1[0][i]:
                match+=1

        self.box3.Clear()
        self.box3.write(str(match/(1.0*len(mat2plot[0]))))

        
        

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
    return "BinComp"







        
