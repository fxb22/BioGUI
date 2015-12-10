import wx
import wx.lib.mixins.listctrl as listmix

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin,
                   listmix.ColumnSorterMixin):
    def __init__(self, parent, ID, pos, size, style, numCols):
        wx.ListCtrl.__init__(self, parent, ID, size, pos, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, numCols)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
        self.sortVar = 1
        self.colSort = 0
        self.col2Sort = 0

    def GetListCtrl(self):
        return self

    def GetDataMap(self):
        return self.itemDataMap

    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        self.Refresh()
        
    def OnGetItemText(self, item, col):
        index = self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s

    def GetSelected(self):
        gPos = []
        if not self.GetFirstSelected() == (-1):
            gPos.append(self.GetFirstSelected())
            while not self.GetNextSelected(gPos[-1]) == (-1):
                gPos.append(self.GetNextSelected(gPos[-1]))
        else:
            gPos.append(0)
        return gPos

    def Fill(self, cols, widths):
        self.ClearAll()
        for i,k in enumerate(cols):
            self.InsertColumn(i,k)
            self.SetColumnWidth(i, widths[i])
        self.Show(True)

    def Refill(self, listData):
        self.itemIndexMap = listData.keys()
        self.itemDataMap = listData
        self.SetItemCount(len(listData))

    def OnColClick(self, event):
        self.col2Sort = event.GetColumn()
        if self.col2Sort == self.colSort:
            self.sortVar = abs(self.sortVar - 1)
        else:
            self.sortVar = 1
        self.colSort = self.col2Sort
        self.SortListItems(self.col2Sort, ascending = self.sortVar)
