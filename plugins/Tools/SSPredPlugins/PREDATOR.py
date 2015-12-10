import wx
import re
import urllib
import urllib2
import BusyNote as bn

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "PREDATOR"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\predator.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetBad(self):
        return self.Bad

    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()
        for v in self.parent.resBoxes.values():
            v.Show(True)

    def Normalize(self):
        self.final = ''
        self.reply = re.sub('c','.',self.reply)
        self.reply = re.sub('e','E',self.reply)
        self.final = re.sub('h','H',self.reply)

    def WriteBoxes(self):
        self.Normalize()
        self.parent.resBoxes['top'].Show(True)
        self.parent.resBoxes['low'].Show(True)
        self.parent.resBoxes['top'].write('Query:\n'+str(self.query.seq)+'\n')
        self.parent.resBoxes['top'].write('Result:\n'+self.reply+'\n')
        i = 0
        while i < len(self.lines):
            if self.lines[i][:10] == 'PREDATOR :':
                j = 0
                while j < 10:
                    write = re.sub('<.*?>','',self.lines[i + j])
                    self.parent.resBoxes['low'].write(write+'\n')
                    j += 1
            i += 1
        self.parent.SSEPlot(self.final)

    def UrlRead(self, event):
        self.lines = self.reply.split('\n')
        i = 0
        while i < len(self.lines):
            l = self.lines[i]
            if '        10' in l:
                self.reply = self.lines[i+3]
                while self.lines[i+2][:5] == '<FONT':
                    self.reply += re.sub('<.*?>','',self.lines[i + 2])
                    i += 2
                i = len(self.lines)
            i += 1
        self.reply = re.sub('<.*?>','',self.reply)
        self.Bad = True
        if self.Bad:
            if not self.parent == None:
                self.timer.Stop()
                self.busy.Clear()
                for v in self.parent.resBoxes.values():
                    v.Show(True)
                self.WriteBoxes()

    def Submit(self):        
        url = 'http://npsa-pbil.ibcp.fr/cgi-bin/secpred_preda.pl'
        data = urllib.urlencode({'title':self.query.id,
                                 'notice':self.query.seq})
        if not self.parent == None:
            self.timer = wx.Timer(self.parent,-1)
            self.timer.Start(10000)
            self.parent.Bind(wx.EVT_TIMER, self.UrlRead, self.timer)
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.busy = bn.BusyNote()
            self.busy.Show(self.parent)
            self.f = urllib2.urlopen(url,data)
            self.reply = self.f.read()
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
        self.t = 0
        self.Bad = False
        self.query = query
        self.preds = []
        self.Submit()
        
def GetExec(seq):
    a = Plugin()
    a.GetExec(None,seq)


def GetName():
    #Method to return name of tool
    return "PREDATOR"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\predator.bmp"
