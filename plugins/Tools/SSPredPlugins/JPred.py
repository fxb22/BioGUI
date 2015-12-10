import wx
import os
import re
import urllib
import urllib2
import BusyNote as bn
import listControl as lc

class Plugin():

    def GetBad(self):
        return self.Bad

    def ButtonClicked(self, event):
        button = event.GetEventObject()
        if 'Al' in button.GetLabel():
            dirt = os.getcwd() + '/Records/Alignments'
        else:
            dirt = os.getcwd() + '/Records/Amino Acids'
        dlg = wx.FileDialog(self.parent, "Choose a file", dirt,
                            ".fasta", "*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = os.path.join(self.dirname, self.filename)
            self.SaveFile(f)
        dlg.Destroy()

    def SetButtons(self):
        p = self.parent.resBoxes['low'].GetPosition()
        s = self.parent.resBoxes['low'].GetSize()
        xPos = p[0] + s[0] - 90
        yPos = p[1] + s[1]/2.
        self.parent.resBoxes['btop'] = wx.Button(self.parent.panelR, -1,
                                        'Save\nSequence', pos=(xPos,yPos-50),
                                        size = (80, 40), style=wx.NO_BORDER)
        self.parent.resBoxes['btop'].SetBackgroundColour('RED')
        self.parent.resBoxes['btop'].SetForegroundColour('WHITE')
        self.parent.Bind(wx.EVT_BUTTON,self.ButtonClicked,
                         self.parent.resBoxes['btop'])
        self.parent.resBoxes['blow'] = wx.Button(self.parent.panelR, -1,
                                        'Save\nAlignment', pos=(xPos,yPos+10),
                                        size = (80, 40), style=wx.NO_BORDER)
        self.parent.resBoxes['blow'].SetBackgroundColour('RED')
        self.parent.resBoxes['blow'].SetForegroundColour('WHITE')
        self.parent.Bind(wx.EVT_BUTTON, self.ButtonClicked,
                         self.parent.resBoxes['blow'])

    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()
        for v in self.parent.resBoxes.values():
            v.Show(True)
        self.parent.resBoxes['low'].Show(False)
        s = self.parent.resBoxes['low'].GetSize()
        self.parent.resBoxes['list'] = lc.TestListCtrl(self.parent.panelR, -1,
                                size=self.parent.resBoxes['low'].GetPosition(),
                                pos=(s[0] - 100, s[1]),
                                style=wx.LC_REPORT|wx.LC_VIRTUAL, numCols = 2)
        for v in self.parent.resBoxes.values():
            v.Show(True)
        self.parent.resBoxes['low'].Show(False)
        self.SetButtons()

    def ListRefill(self, recs):
        self.listData = dict()
        j = 0
        for r in recs:
            self.listData[j] = (r[0], r[1])
            j += 1
        self.parent.resBoxes['list'].Refill(self.listData)
        
    def ListCntrlFill(self):
        cols = ['Title', 'Sequence']
        colWidths = [75, self.parent.resBoxes['low'].GetSize()[1] - 100]
        self.parent.resBoxes['list'].Fill(cols, colWidths)

    def OnSelect(self, event):                    
        self.ListCntrlFill()
        self.ListRefill()

    def SaveFile(self, f):
        f = open(f, 'w')
        f.write(r'>'+str(self.query.id)+'\n'+str(self.query.seq)+'\n')
        pos = self.parent.resBoxes['list'].GetSelected()
        for p in pos:
            rec = self.listData[self.parent.resBoxes['list'].itemIndexMap[p]]
            f.write(r'>'+str(rec[0])+'\n'+str(rec[1])+'\n')
        f.close()

    def Submit(self, query):        
        url='http://www.compbio.dundee.ac.uk/www-jpred/cgi-bin/jpred_form'
        data = urllib.urlencode({'seq':query,'input':'seq','pdb':'no'})
        f = urllib2.urlopen(url,data)
        for l in f.read().split():
            if 'URL=' in l:
                self.n = l[-11:-1]
        if not self.parent == None:
            self.timer = wx.Timer(self.parent,-1)
            self.timer.Start(10000)
            self.parent.Bind(wx.EVT_TIMER, self.UrlRead, self.timer)
            self.busy = bn.BusyNote()
            self.busy.Show(self.parent)

    def UrlRead(self, event):        
        u = r'http://www.compbio.dundee.ac.uk/www-jpred/results/'
        try:
            f2 = urllib2.urlopen(u+str(self.n)+r'/'+str(self.n)+r'.html')
            reply = f2.read()
            self.reply = re.sub('<.*?>','',reply)
            self.Bad = True
        except:
            2
        if self.Bad:
            if not self.parent == None:
                self.timer.Stop()
                self.busy.Clear()
                """for v in self.parent.resBoxes.values():
                    v.Show(True)"""
                self.WriteBoxes()

    def Normalize(self):
        self.final = ''
        i = 0
        while i < len(self.preds[0]):
            if self.preds[0][i] == self.preds[1][i]:
                self.final += self.preds[0][i]
            elif self.preds[0][i] == self.preds[2][i]:
                self.final += self.preds[0][i]
            elif self.preds[1][i] == self.preds[2][i]:
                self.final += self.preds[0][i]
            else:
                self.final += '.'
            i += 1
        self.parent.SSEPlot(self.final)

    def WriteBoxes(self):
        self.parent.resBoxes['top'].Show(True)
        lines = self.reply.split('\n')
        blastRecs = []
        i = 1
        while not lines[i+1][:4] == 'Orig':
            split = lines[i].split(': ')
            if len(split) >= 3:
                blastRecs.append([split[2], split[1][:-1]])
            i += 1
        self.ListCntrlFill()
        self.ListRefill(blastRecs)
        j = 0
        while not lines[i] == 'Notes':
            line = re.sub('                ','  ',lines[i])
            if j in [3,4,5]:
                l = line.split(':')[1][1:-1]
                l = re.sub('-','.',l)
                self.preds.append(l)
            elif j in [7,8,9,14]:
                line = re.sub('               ',' ',lines[i])
            j += 1
            self.parent.resBoxes['top'].write(line)
            self.parent.resBoxes['top'].write('\n')
            i += 1
        self.Normalize()
            
    def GetExec(self, parent, query):
        self.query = query
        self.parent = parent
        if not self.parent == None:
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.AdjustBoxes()
        self.t = 0
        self.Bad = False
        seq = '>'+query.id+'\n'+query.seq
        self.preds = []
        self.Submit(seq)
        
def GetExec(seq):
    a = Plugin()
    a.GetExec(None,seq)


def GetName():
    #Method to return name of tool
    return "JPred"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\jpred.bmp"
