import os
import sys
import wx
import urllib

import wx.lib.mixins.listctrl as listmix

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, ID, style, size, colNum, pos=(0,0)):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, colNum)

    def GetListCtrl(self):
        return self

    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        
        # redraw the list
        self.Refresh()

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s
        
class Plugin():
    def GetName(self):
        '''
        Method to return name of tool
        '''
        return "Search"
    
    def GetBMP(self, dirH):
        '''
        Method to return identifying image
        '''
        return dirH + r"\Utils\Icons\flashlight.bmp"
    
    def GetOutFile(self):
        self.outfile=dirH + r"\plugins\clustal.aln"
        return self.outfile

    def GetExec(self,parent,dbName,query):
        cols = ''
        for cn in parent.colSet:
            cols += cn + ','
        #print cols
        #print parent.dbCB.GetValue()
        #print parent.dbCB.GetSelection()
        #print r"http://www.uniprot.org/" + str(parent.dbCB.GetValue())+ r"/?query=" + parent.text1.GetValue()+ r"&format=tab&columns=" + cols[:-1]
            
        handle = urllib.urlopen(r"http://www.uniprot.org/" + parent.dbCB.GetValue()
                                  + r"/?query=" + parent.text1.GetValue()
                                  + r"&format=tab&columns=" + cols[:-1])
        self.res = handle.read().split('\n')
        idk = 0
        #while idk < len(parent.windowBin):
            #parent.windowBin[idk].Show(False)
            #parent.windowBin.pop(idk)
        self.colTitles = []
        self.colNum = 0
        temp = self.res[0].split('\t')
        ttab = len(temp)
        while ttab > 0:
            self.colTitles.append(temp[ttab - 1])
            self.colNum += 1
            ttab -= 1
        self.dbList = TestListCtrl(parent.panelRSLT, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL, size = (892, 370), colNum = self.colNum + 1, pos=(74, 10))
        self.dbList.SetForegroundColour('BLACK')
        
        self.listRefill()
                
    def helpEXE(self,parent):
        parent.l1.Show(True)
        parent.text1.Show(True)
        parent.l2.Show(True)
        parent.l3.Show(True)
        
        #tempVal = parent.dbCB.GetValue()

    def ListCntrlFill(self):
        self.dbList.ClearAll()
        self.dbList.InsertColumn(0, "#")
        self.dbList.SetColumnWidth(0, 50)
        iters = self.colNum 
        while iters  > 0:
            self.dbList.InsertColumn(self.colNum - iters+1, self.colTitles[iters - 1])
            self.dbList.SetColumnWidth(self.colNum - iters+1, 832. / self.colNum)
            iters -= 1
        

    def listRefill(self):
        #self.dbList.Show(False)
        self.ListCntrlFill()
        musicdata = dict()
        j = 0
        while j < len(self.res[1:-1]):
            rHo = [j]
            for col in self.res[j+1].split('\t'):
                rHo.append(unicode(col))
            musicdata[j] = rHo
            j += 1
        self.dbList.itemIndexMap = musicdata.keys()
        self.dbList.itemDataMap = musicdata
        self.data = musicdata
        self.dbList.SetItemCount(len(musicdata))
        #self.dbList.Show(True)
        
        #self.dbList.Refresh()
    
#Method to allow non-GUI based usage
def GetExec(dbName,query):
    handle = Entrez.esearch(db=dbName,term=query)
    erl = Entrez.read(handle)
    return erl
