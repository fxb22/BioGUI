import wx
import getPlugins as gpi

class Plugin():
    def OnSize(self):
        bP = self.bPSize
        self.bPSize = self.bigPanel.GetSize()
        self.frame.SetPosition((self.bPSize[0]-307,0),-1)
        self.frame.SetSize((200,self.bPSize[1]-3))
        self.coverPanel.SetSize((self.bPSize[0]-307,self.bPSize[1]-3))
        self.coverPanel.SetBackgroundColour('GRAY')
        ss = (self.frame.GetSize()[0]-20, self.frame.GetSize()[1] - 100)
        self.scrolled.SetSize(ss)
        self.scrolled.SetScrollbars(0, (len(self.features)/2),
                                     0, self.frame.GetSize()[1]*0.2)
        self.scrolled.SetScrollRate(0,self.frame.GetSize()[1] * 0.4)
        yPos = 0
        yIt = self.frame.GetSize()[1]*0.1
        for f in self.features:
            self.frameObjs[f][0].SetPosition((3,yPos + 5))
            self.frameObjs[f][1].SetPosition((100,yPos))
            yPos += yIt
        if self.timesCalled > 1:
            self.curView.OnSize()
        
    def Refresh(self,record):
        self.rec = record
        if self.timesCalled < 1:
            self.timesCalled += 1
            self.Clear()
        self.GetExec(record)

    def Clear(self):
        self.frame.Show(False)
        self.coverPanel.Show(False)

    def DefineColors(self):
        cL = []
        vals = range(0,255,63)
        for r in vals:
            for g in vals:
                for b in vals:
                    cL.append((r,g,b))
        return cL[1:]

    def GetFeatures(self):
        return ["gene","CDS","sig_peptide","misc_feature","rRNA",
                "tRNA","RBS","repeat_region","mobile_element","misc_RNA",
                "terminator","gap","promoter","-10_signal","ncRNA",
                "misc_binding","-35_signal","operon","misc_recomb",
                "variation","mat_peptide","protein_bind","stem_loop",
                "primer_bind","intron","tmRNA","misc_difference","mRNA",
                "rep_origin","unsure","misc_signal","5'UTR","exon",
                "TATA_signal","oriT","misc_structure","modified_base",
                "attenuator","precursor_RNA","LTR","prim_transcript",
                "old_sequence","3'UTR","conflict","enhancer",
                "polyA_signal","transit_peptide","CAAT_signal","D-loop"]

    def FeaturesInit(self):
        cL = self.DefineColors()
        yPos = 6
        yIt = self.frame.GetSize()[1] * 0.1
        for num,f in enumerate(self.features):
            self.frameObjs[f] = [wx.CheckBox(self.scrolled, -1, label = f,
                                             pos = (3, yPos))]
            button = wx.Button(self.scrolled, -1, label='color',
                               pos = (100, yPos - 5), size = (50, 20),
                               name = f)
            button.SetBackgroundColour(cL[num])
            button.Bind(wx.EVT_BUTTON, self.SelectColour)
            
            self.frameObjs[f].append(button)
            yPos += yIt

    def ScrollInit(self, yPos):
        yPos += 35
        xPos = 10
        self.scrolled = wx.ScrolledWindow(self.frame, -1, pos = (xPos, yPos),
                                          style = wx.SUNKEN_BORDER|wx.VSCROLL)
        self.scrolled.SetBackgroundColour('WHITE')
        ss = (self.frame.GetSize()[0]-20, self.frame.GetSize()[1] - 100)
        self.scrolled.SetSize(ss)
        self.scrolled.SetScrollbars(0, .5*(len(self.GetFeatures())-(ss[1]/45.)),
                                     0, self.frame.GetSize()[1]*0.2)
        self.scrolled.SetScrollRate(0, 2*(len(self.GetFeatures())-(ss[1]/45.))-2)
        self.scrolled.Show(True) 

    def FrameInit(self):
        self.frame = wx.Panel(self.bigPanel, -1, style = wx.RAISED_BORDER,
                              pos = (self.bPSize[0]-307,0),
                              size = (200, self.bPSize[1] - 3))
        self.frame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.frame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.frame.Show(False)

    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\GenomeViewPlugins")
        xPos = 10
        yPos = 10
        for v in self.views.values():
            if xPos > 150:
                xPos = 10
                yPos += 22
            viewName = v.GetName()
            self.tabButtons.append(wx.Button(self.frame, -1, str(viewName),
                                             pos=(xPos, yPos), size=(60, 22),
                                             style = wx.NO_BORDER))
            self.tabButtons[-1].SetBackgroundColour(
                self.colorList['ViewPanelGrayFrame']['Back'])
            self.tabButtons[-1].SetForegroundColour(
                self.colorList['ViewPanelGrayFrame']['Fore'])
            xPos+=60
            self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.tabButtons[-1])
        self.lastButton = self.tabButtons[0]
        self.curView = self.views.values()[0].Plugin()
        return yPos

    def Init(self, parent, bigPanel, colorList):
        self.Par = parent
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.colorList = colorList
        self.features = self.GetFeatures()
        self.timesCalled = 0
        self.curView = []
        self.buttonLabel = []
        self.frameObjs = {}
        self.tabButtons = []
        self.FrameInit()
        yP = self.TabButtonInit()
        self.ScrollInit(yP)
        self.FeaturesInit()
        self.coverPanel = wx.Panel(self.bigPanel, -1,
                                   style = wx.NO_BORDER, pos = (0, 0),
                                   size = (self.bPSize[0]-300,
                                           self.bPSize[1]))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.Show(False)
               
    def GetExec(self, rec):
        self.frame.Show(True)
        self.coverPanel.Show(True)
        self.rec = rec
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                self.lastButton.GetId())
        event.SetEventObject(self.lastButton)
        self.DoView(event)

    def DoView(self, event):
        for c in self.coverPanel.GetChildren():
            c.Destroy()
        for c in self.frame.GetChildren():
            temp = c.GetName()
            if len(temp) > 2:
                if temp[:2] == 'go':
                    c.Show(False)
                    c.Destroy()
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                self.curView = v.Plugin()
        self.curView.GetExec(self.frame, self.coverPanel,
                                   self.rec, self.frameObjs)
        self.timesCalled += 1
        
    def SelectColour(self, event):
        """display the colour dialog and select"""
        dlg = wx.ColourDialog(self.coverPanel)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            # gives red, green, blue tuple (r, g, b)
            # each rgb value has a range of 0 to 255
            rgb = data.GetColour().Get()
            evtobj = event.GetEventObject()
            eoID = evtobj.GetName()
            self.frameObjs[eoID][1].SetBackgroundColour(rgb)
        dlg.Destroy()

    def GetType(self):
        return "Chromosomes"

    def GetName(self):
        return "GenomeView"

def GetType():
    return "Chromosomes"

def GetName():
    return "GenomeView"
