import wx
import urllib
import urllib2
import re
import listControl as lc
import BusyNote as bn

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "GOR V"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\gorV.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetBad(self):
        return self.Bad

    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()
        self.parent.resBoxes['top'].Show(True)
        # I don't understand the size/pos switch in lc
        self.ps = self.parent.panelR.GetSize()
        self.parent.resBoxes['low'] = lc.TestListCtrl(self.parent.panelR, -1,
                                        style=wx.LC_REPORT|wx.LC_VIRTUAL,
                                        pos = (self.ps[0]-83, self.ps[1]/3.-32),
                                        size = (75,self.ps[1]/3.+8), numCols = 6)
        
    def ListCntrlFill(self):
        cols = ['Index', 'Amino Acid', 'Helix Probability', 'Sheet Probability',
                'Coil Probability', 'Prediction']
        x = self.ps[0] - 108
        colWidths = [x/10., x/10., x/6., x/6., x/6., x/10.]
        self.parent.resBoxes['low'].Fill(cols, colWidths)
            
    def listFill(self):
        #Fill and update list control
        listData = dict()
        for i,l in enumerate(self.valueList):
            listData[i] = l[1],l[2],l[3],l[4],l[5],l[6]
        self.parent.resBoxes['low'].Refill(listData)

    def WriteBoxes(self):
        self.parent.resBoxes['top'].Show(True)
        self.parent.resBoxes['top'].write('Query:\n'+str(self.query.seq)+'\n')
        a = 'This is the secondary structure prediction: </H2>'
        l1 = self.lines[0].split(a)
        self.final = re.sub('C','.',str(l1[1]))
        self.final = re.sub(' ','',self.final)
        self.parent.resBoxes['top'].write('Result:\n'+self.final+'\n')
        self.ListCntrlFill()
        self.parent.resBoxes['low'].Show(True)
        self.valueList = []
        reply = self.lines[9:-2]
        for r in reply:
            r = re.sub('\s+','\t',r)
            if len(r) >= 5:
                self.valueList.append(r.split('\t'))
        self.listFill()
        self.parent.SSEPlot(self.final)

    def UrlRead(self, event):
        self.lines = self.f.read().split('\n')
        self.Bad = True
        if self.Bad:
            if not self.parent == None:
                self.timer.Stop()
                self.busy.Clear()
                for v in self.parent.resBoxes.values():
                    v.Show(True)
                self.WriteBoxes()
            else:
                return True

    def Submit(self):        
        url='http://gor.bb.iastate.edu/cgi-bin/gorv/process.cgi'
        data = urllib.urlencode({'address':'something@biogui.com',
                                 'sequence':str(self.query.seq)})
        if not self.parent == None:
            self.timer = wx.Timer(self.parent,-1)
            self.timer.Start(30000)
            self.parent.Bind(wx.EVT_TIMER, self.UrlRead, self.timer)
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.busy = bn.BusyNote()
            self.busy.Show(self.parent)
            self.f = urllib2.urlopen(url,data)
        else:
            go = True
            while go:
                try:
                    self.f = urllib2.urlopen(url,data)
                    self.reply = self.f.read()
                    go = self.UrlRead(wx.EVT_IDLE)
                except:
                    2

    def GetExec(self, parent, query):
        self.parent = parent
        if not self.parent == None:
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.AdjustBoxes()
        self.Bad = False
        self.query = query
        self.Submit()

def GetExec(dbName,idName):
    return Entrez.efetch(db=dbName,id=idName,tool='BioGUI')


def GetName():
    #Method to return name of tool
    return "GOR V"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\gorV.bmp"
