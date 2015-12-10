import os
import sys
import wx
from xml.dom import minidom
import urllib
import urllib2
import re

class Plugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "Browse"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\Magnify.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def getOBO(self):
        self.terms = {}
        self.terms['all'] = ['root','all','all']
        #print self.terms
        self.url='http://amigo.geneontology.org/cgi-bin/amigo/browse.cgi'
        f = urllib2.urlopen(self.url,self.data)
        lines = f.read().split('\n')
        i = 0
        while i < len(lines):
            if lines[i] == '[Term]':
                termId = re.split(': ',lines[i + 1])[1]
                termName = re.split(': ',lines[i + 2])[1]
                if not termId == 'all':
                    while len(lines[i]) > 1 and not lines[i][0] == 'x':
                        if lines[i][:3] == 'def':
                            termDef = re.split(': ',lines[i])[1]
                        elif lines[i][:4] == 'is_a':
                            termParent = re.split(': ',lines[i])[1]
                        i += 1
                    while len(lines[i]) > 1 and lines[i][0] == 'x':
                        i += 1
                
                
                if not self.terms.has_key(termId):
                    self.terms[termId] = [termParent,termName,termDef]
            i += 1
            

    def fillTree(self):
        
        keys = self.terms.keys()
        for k in keys:
            a = str(k)
            arrow = self.terms[a]
            nodes = []
            while not arrow[0] == 'root':
                if not a in self.total:
                    self.total.append(a)
                    nodes.append(a)
                    
                    a = arrow[0]
                    arrow = self.terms[a]
                    
                else:
                    arrow[0] = 'root'
            while len(nodes) > 0:
                a = nodes[-1]
                arrow = self.terms[a]
                self.items[a] = self.GOtree.AppendItem(self.items[arrow[0]],a + ' [' + arrow[1] + ']')
                #print self.items[a]
                self.GOtree.SetItemHasChildren(self.items[arrow[0]],True)
                self.GOtree.SetItemHasChildren(self.items[a],True)
                del nodes[-1]
        
        


                

    def OnExpandItem(self, event):
        targ = re.split(r' ',str(self.GOtree.GetItemText(event.GetItem())))[0]
        url=r'http://amigo.geneontology.org/cgi-bin/amigo/browse.cgi'
        self.data = urllib.urlencode({'action':'plus_node',
                                     'target':targ,
                                     'open_1':self.open1,
                                     'format':'obo'
                                     })
        self.open1 += ',' + targ
        self.getOBO()
        self.fillTree()
        
            

    def OnCollapseItem(self, event):
        # Be prepared, self.CollapseAndReset below may cause
        # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
        if self.__collapsing:
            event.Veto()
        else:
            item = event.GetItem()
            self.CollapseAndReset(item)
            self.SetItemHasChildren(item)
            self.__collapsing = False


    
    def GetExec(self,parent,query):
        self.total = []
        parent.panelSQ.Show(False)
        parent.panelRSLT.SetPosition((7,15))
        winSize = parent.GetSize()
        parent.panelRSLT.SetSize((winSize[0] - 24,winSize[1] - 110))
        parent.text2.SetSize((winSize[0] - 158,winSize[1] - 130))
        parent.text2.Show(True)
        parent.l2.Show(True)

        self.data = urllib.urlencode({
                                 'format':'obo'
                                 })
        self.getOBO()

        self.GOtree = wx.TreeCtrl(parent.text2,-1,pos=(5,5), size = (winSize[0] - 178,winSize[1] - 150),
                                  style = wx.HSCROLL|wx.VSCROLL|wx.TR_HAS_BUTTONS )
        
        self.GOtree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
        self.GOtree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)

        self.items = {}
        self.items['all'] = self.GOtree.AddRoot('all')
        self.GOtree.SetItemHasChildren(self.items['all'],True)
        self.fillTree()
        self.open1 = 'all'
        
        



        
        


        
            
                

        
def GetName():
    '''
    Method to return name of tool
    '''
    return "Browse"

def GetBMP():
    '''
    Method to return identifying image
    '''
    return r".\Utils\Icons\Magnify.bmp"


        
        
            

def GetExec(dbName,idName):
    return Entrez.efetch(db=dbName,id=idName,tool='BioGUI')
