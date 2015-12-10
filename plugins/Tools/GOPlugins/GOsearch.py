import os
import sys
import wx
from xml.dom import minidom
import urllib
import urllib2
import re
import listControl as lc
import GOAncestorChartDialog as acd

class Plugin():
    def GetName(self):
        # Method to return name of tool
        return "Search"
    
    def GetBMP(self, dirH):
        # Method to return identifying image
        return dirH + r"\Utils\Icons\flashlight.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetChart(self,event):
        query = self.lynks[self.t2.GetSelected()[0]]
        GetChart(query)
        dialog = acd.acDialog(self.parent, query)
        dialog.ShowImage(r'.\Utils\goac.png')

    def GetExec(self,parent,query):
        self.parent = parent
        self.bPSize = parent.GetSize()
        self.total = []
        self.parent.textR.Show(False)
        self.t = lc.TestListCtrl(self.parent.panelR, -1, size = (75,10),
                                 style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                 pos = (self.bPSize[0] - 533,
                                        self.bPSize[1] - 250),
                                 numCols = 5)
        self.t.cols = ['Symbol','Full Name','Association','Type','Species']
        self.t.widths = [50,200,75,50,75]
        self.parent.windowBin.append(self.t)
        self.t2 = lc.TestListCtrl(self.parent.panelR, -1,
                                  style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                  pos = (self.bPSize[0]/2. - 100,
                                         self.bPSize[1] - 250),
                                  size = (self.bPSize[0] - 445,10),
                                  numCols = 3)
        self.t2.cols = ['GO ID','Term','Ontology']
        self.t2.widths = [75, 215, 100]
        self.parent.windowBin.append(self.t2)
        self.t.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.ListCntrlFill(self.t)
        self.ListCntrlFill(self.t2)
        t = GetExec(query)
        self.links = t[0]
        self.ld = t[1]
        self.t.Refill(t[1])
        
    def ListCntrlFill(self, lc):
        #Method to create list control column headers
        lc.Fill(lc.cols,lc.widths) 

    def OnSelect(self, event):
        #Respond to a selction (a.k.a. selection) of a search result
        #Associations are shown in self.lc2
        gPos1 = self.t.GetSelected()[0]
        t = GetAssoc(self.links[gPos1])
        self.lynks = t[0]
        data = t[1]
        self.t2.Refill(data)
        self.t2.Bind(wx.EVT_LIST_ITEM_SELECTED, self.GetChart)
                
def GetName():
    #Method to return name of tool
    return "Search"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\flashlight.bmp" 
            
def GetChart(query):
    u = 'http://amigo.geneontology.org/cgi-bin/amigo/visualize?inline=false'
    u += '&mode=quickgo&beta=0&term=' + query
    urllib.urlretrieve(u, r'.\Utils\goac.png')
    
def GetAMIGO(lines):
    links = []
    listData = dict()
    j = 0
    for i in lines:
        if ' title="View term associations"' in i:
            ln = re.split(' title="View term associations">',i)
            el = re.split('a href="',ln[0])
            links.append(el[1])
            l = re.split(' association',ln[1])
            assoc = l[0]
        elif 'title="View gene product details" class="symbol"' in i:
            ln = re.split('<em class="hilite">',i)
            l = re.split('</em',ln[1])
            symbol = l[0]
        elif 'title="View gene product details" class="full_name"' in i:
            if 'em class="hilite">' in i:
                ln = re.split('em class="hilite">',i)
            else:
                ln = re.split('class="full_name">',i)
            ln1 = re.sub('</em>','',ln[1])
            l = re.split('</a',ln1)
            name = l[0]
        elif '<span class="type"' in i:
            ln = re.split('<span class="type">',i)
            l = re.split('</span>',ln[1])
            typ = l[0]
        elif 'class="spp"' in i:
            ln = re.split('class="spp">',i)
            l = re.split('</i>',ln[1])
            species = l[0]
            listData[j] = symbol, name, assoc, typ, species
            j += 1
    return [links,listData]
            
def GetExec(query):
    data = urllib.urlencode({'action':             'new-search',
                             'search_constraint':  'gp',
                             'search_query':       query})
    terms = dict()
    terms['all'] = ['root','all','all']
    url='http://amigo.geneontology.org/cgi-bin/amigo/search.cgi'
    f = urllib2.urlopen(url,data)
    f = f.read()
    f = re.sub('DOCTYPE(.|\s)*?UniProtKB:E9PI80" id="UniProtKB:E9PI80','',f)
    lines = f.split('\n')
    return GetAMIGO(lines)
    
def GetAssoc(query):
    links = []
    data = dict()
    j = 0
    url = r'http://amigo.geneontology.org/cgi-bin/amigo/'
    url += query
    f = urllib2.urlopen(url)
    for line in f.read().split('\n'):
        if '<label for="term-' in line:
            ln = re.split('>',line)
            goId = ln[1][:10]
            links.append(goId)
            term = ln[3][:-3]
        if 'click to view documentation" class="type">' in line:
            ln = re.split('title="',line)
            l = re.split('; ',ln[1])
            ont = l[0]
            data[j] = goId,term,ont
            j += 1
    return [links,data]

