import wx
import re
import urllib
import urllib2
import BusyNote as bn

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "PSSpred"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\PSSpred.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetBad(self):
        return self.Bad

    def Submit(self, query):        
        url='http://zhanglab.ccmb.med.umich.edu/cgi-bin/PSSpred.pl'
        data = urllib.urlencode({'SEQUENCE':query,
                                 'REPLY-E-MAIL':'biogui@biogui.com'})
        f = urllib2.urlopen(url,data)
        for l in f.read().split():
            if r'>http://zhanglab' in l:
                self.n = l.split(r'>')[1][:-3]
        if not self.parent == None:
            self.timer = wx.Timer(self.parent,-1)
            self.timer.Start(10000)
            self.parent.Bind(wx.EVT_TIMER, self.UrlRead, self.timer)
            self.busy = bn.BusyNote()
            self.busy.Show(self.parent)

    def UrlRead(self, event):
        try:
            f2 = urllib2.urlopen(str(self.n))
            reply = f2.read()
            self.reply = reply.split('\n')
            if not 'Your submitted sequence is' in self.reply[14]:
                self.Bad = True
        except:
            self.t += 1
        if not self.parent == None and self.t == 1:
            self.AdjustBoxes()
        if self.Bad:
            if not self.parent == None:
                self.timer.Stop()
                self.busy.Clear()
                for v in self.parent.resBoxes.values():
                    v.Show(True)
                self.WriteBoxes()

    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()

    def WriteBoxes(self):
        seq = ''
        ss = ''
        conf = ''
        count = ''
        i = 16
        while 'seq' in self.reply[i]:
            t = re.sub('seq: *\d\d? ', '', self.reply[i])
            seq += str(t.split(' ')[0])
            ss += str(self.reply[i+1].split(' ')[6])
            self.final = re.sub('C','.',ss)
            conf += str(self.reply[i+2].split(' ')[4])
            i += 4
        i = 0
        while i < len(seq):
            if i % 10 == 0:                
                count += '*'
            else:
                count += ' '
            i += 1        
        self.parent.resBoxes['top'].write('      '+count)
        self.parent.resBoxes['top'].write('\nseq:  '+seq)
        self.parent.resBoxes['top'].write('\nSS:   '+self.final)
        self.parent.resBoxes['top'].write('\nconf: '+conf)
        self.parent.SSEPlot(self.final)
            
    def GetExec(self, parent, query):
        self.parent = parent
        if not self.parent == None:
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.AdjustBoxes()
        self.t = 0
        self.Bad = False
        seq = '>'+query.id+'\n'+query.seq
        self.Submit(seq)
        
def GetExec(seq):
    a = Plugin()
    a.GetExec(None,seq)

def GetName():
    #Method to return name of tool
    return "PSSpred"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\PSSpred.bmp"
