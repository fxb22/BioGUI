import wx

class Plugin():
    def Clear(self):
        # Erase view
        if hasattr(self, 'coverPanel'):
            self.coverPanel.Show(False)

    def CoverInit(self):
        self.coverPanel = wx.ScrolledWindow(self.bigPanel, -1,
                                            style = wx.VSCROLL,
                                            pos = (0, 0),
                                            size = (self.bPSize[0] - 270,
                                                    self.bPSize[1] - 8))
        self.coverPanel.SetScrollbars(0, 1, 0, len(self.rec)*34+13)
        self.coverPanel.SetScrollRate(15, 35)
        self.coverPanel.Show(True)

    def SetSeqText(self):
        # Create textctrl
        self.seqText = wx.TextCtrl(self.coverPanel, -1, "", pos = (10, 10),
                             size = (self.bPSize[0]-368, len(self.rec)*34+20),
                             style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_RICH2|
                                   wx.TE_READONLY|wx.HSCROLL|wx.TE_NO_VSCROLL)
        font = self.seqText.GetFont()
        newFont = wx.Font(font.PointSize + 2, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.seqText.SetFont(newFont)
        self.seqText.SetDefaultStyle(wx.TextAttr(
            self.colorList['ViewPanelList']['Fore'],
            self.colorList['ViewPanelList']['Back']))
        self.seqCount = wx.TextCtrl(self.coverPanel, -1, "",
                             pos = (self.bPSize[0] - 350, 10),
                             size = (90, len(self.rec)*34+20),
                             style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_RICH2|
                                   wx.TE_READONLY|wx.TE_NO_VSCROLL)
        self.seqCount.SetFont(newFont)
        self.seqCount.SetDefaultStyle(wx.TextAttr(
            self.colorList['ViewPanelList']['Fore'],
            self.colorList['ViewPanelList']['Back']))

    def TextUpdate(self):
        maxLen = 0
        for record in self.rec:
            if len(record.id) > maxLen:
                maxLen = len(record.id)
        self.seqCount.write('Idents.\n')
        for r,record in enumerate(self.rec):
            if r > 0:
                spacer = 0
                count = 0
                while spacer < maxLen + 3:
                    self.seqText.write(' ')
                    spacer += 1
                for pos,letter in enumerate(record.seq):
                    if not letter == '.':
                        if letter == self.rec[0].seq[pos]:
                            self.seqText.write(r'.')
                            count += 1
                        else:
                            self.seqText.write(r' ')
                    else:
                        self.seqText.write(r' ')
                self.seqText.write('\n')
                self.seqCount.write('\n')
                self.seqCount.write(str(count) + ' \n')
            else:
                self.seqText.write('\n')
                self.seqCount.write(str(len(record.seq)) + '\n')
            self.seqText.write(str(record.id))
            addonlen = maxLen - len(record.id)
            while addonlen > 0:
                self.seqText.write(' ')
                addonlen -= 1
            self.seqText.write(' - ' + str(record.seq) + '\n')

    def GetExec(self, fr, bp, rec, cL):
        self.frame = fr
        self.bigPanel = bp
        self.bPSize = bp.GetSize()
        self.colorList = cL
        self.rec = rec
        self.CoverInit()
        self.SetSeqText()
        self.TextUpdate()                    
        self.seqText.Show(True)
        self.seqText.ShowPosition(0)
        self.seqCount.Show(True)
        self.seqCount.ShowPosition(0)

def GetName():
    return "Alignment"
