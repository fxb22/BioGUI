import wx
import re
import urllib
import urllib2
import BusyNote as bn

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "HHpred"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\HHPred.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetBad(self):
        return self.Bad

    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()

    def Submit(self):        
        ur='http://toolkit.lmb.uni-muenchen.de/hhpred#/run/hhpred'
        dat = urllib.urlencode({'sequence_input':self.query,
                                 'submitform':'Submit job',
                                 'jobid':'7308946'})
        req = urllib2.Request(url=ur,data=dat)
        
        req.add_header('Host', 'http://toolkit.tuebingen.mpg.de')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Language', 'en-US,en;q=0.5')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Referer', 'http://toolkit.tuebingen.mpg.de/hhpred')
        req.add_header('Connection', 'keep-alive')
        
        f = urllib2.urlopen(req)
        f = urllib2.urlopen('http://toolkit.tuebingen.mpg.de/hhpred/waiting/7308946')
        for l in f.read().split('\n'):
            print l
            """if 'URL=' in l:
                qname = l[-11:-1]
        for line in f.read().split('\n'):
            a = 'Your job is in the queue under '
            a += 'the name: hellofrombiogui with the job ID: '
            if a in line:
                l = line.split(a)
                self.newURL = l[1][:6]
        if not self.parent == None:
            self.timer = wx.Timer(self.parent,-1)
            self.timer.Start(60000)
            self.parent.Bind(wx.EVT_TIMER, self.UrlRead, self.timer)
            self.busy = bn.BusyNote()
            self.busy.Show(self.parent)
            
    def WriteBoxes(self):
        self.parent.resBoxes['top'].write('Query:\n'+self.query)
        self.parent.resBoxes['low'].write('Prediction:\n'+self.final)
        self.parent.SSEPlot(self.final)

    def UrlRead(self, event):        
        try:
            a = r'http://bioinf.cs.ucl.ac.uk:80/psipred/result/' + self.newURL
            f2 = urllib2.urlopen(a)
            reply = f2.read()
            lines = reply.split('\n')
            i = 100
            while i < len(lines):
                if 'resTip' in lines[i]:
                    if 'Strand' in lines[i]:
                        self.final += 'E'
                    elif 'Helix' in lines[i]:
                        self.final += 'H'
                    else:
                        self.final += '.'
                elif '>Key<' in lines[i]:
                    i = len(lines)
                i += 1
            self.Bad = True
        except:
            2
        if self.Bad:
            if not self.parent == None:
                self.timer.Stop()
                self.busy.Clear()
                for v in self.parent.resBoxes.values():
                    v.Show(True)
                self.WriteBoxes()"""

    def GetExec(self,parent,query):
        self.parent = parent
        self.query = '>'+query.id+'\n'+query.seq
        if not self.parent == None:
            for v in self.parent.resBoxes.values():
                v.Show(False)
            self.AdjustBoxes()
        self.Bad = False
        self.Submit()
            
        
            

def GetExec(dbName,idName):
    return Entrez.efetch(db=dbName,id=idName,tool='BioGUI')


def GetName():
    #Method to return name of tool
    return "HHpred"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\HHPred.bmp"
