import wx
import listControl as lc
   
class Plugin():     
    def GetMeth(self):
        2

    def SetMeth(self,meth):
        2
        
    def OnSize(self):
        # Respond to size change
        self.bPSize = self.bigPanel.GetSize()
        self.list.SetSize((self.bPSize[0] - 118, self.bPSize[1] - 40))
        
    def frChange(self,frSize):
        2

    def Refresh(self,rec,pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.ListCtrlFill()

    def GetName(self):
        return "PDB Table"

    def GetColors(self):
        # Acquire coloring options
        try:
            import userColors as uc
            self.colorList = uc.getColors()
        except:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def GetExec(self, rec, frame, coverPanel, frSize, pdbMat):
        self.rec = rec
        self.frame = frame
        self.coverPanel = coverPanel
        self.pdbMat = pdbMat
        self.frSize = frSize
        self.bPSize = self.coverPanel.GetSize()
        self.list = lc.TestListCtrl(self.coverPanel, -1, size = (0,0),
                                     pos = (self.bPSize[0],
                                            self.bPSize[1]),
                                     style = wx.LC_REPORT|wx.LC_VIRTUAL,
                                     numCols = 7)
        self.GetColors()
        self.list.SetBackgroundColour(
            self.colorList['ViewPanelList']['Back'])
        self.list.SetForegroundColour(
            self.colorList['ViewPanelList']['Fore'])
        #self.OnSelect(wx.EVT_IDLE)
        self.ListCtrlFill()
        self.list.Show(True)

    def ListCtrlFill(self):
        cols = ['Chain', 'Res. #', 'Residue', 'X Coord',
                'Y Coord', 'Z Coord', 'Atom']
        colWidths = [40, 60, 60, 65, 65, 65, 50]
        self.list.Fill(cols, colWidths)
        self.ListRefill()

    def ListRefill(self):
        listData = dict()
        j = 0
        for chain in self.pdbMat.get_list():
            for residue in chain.get_list():
                full_id = residue.get_full_id()
                chain = full_id[2]
                res = full_id[3][1]
                aa = residue.get_resname()
                for atom in residue.get_list():
                    coords= atom.get_coord()
                    xc = coords[0]
                    yc = coords[1]
                    zc = coords[2]
                    name = atom.get_name()
                    listData[j] = (str(chain), str(res), str(aa),
                                   xc, yc, zc, str(name))
                    j += 1
        self.list.Refill(listData)

def GetName():
    return "PDB Table"








#    Rainer Wolfcastle: Up and at them. 
#    Dialogue coach: No, "Up and atom". 
#    Rainer Wolfcastle: Up and at them. 
#    Dialogue coach: Up and *atom*. 
#    Rainer Wolfcastle: Up and at 'hem. 
#    Dialogue coach: Better. 
#
#
#    From:   The Simpsons: Season 7, Episode 2 
#            Radioactive Man (24 Sep. 1995) 
#            http://www.imdb.com/title/tt0701201/
