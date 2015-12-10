import wx
import getPlugins as gpi

class Plugin():
    def OnSize(self):
        # Respond to size change
        self.bPSize = self.bigPanel.GetSize()
        self.frame.Show(False)
        self.frame.SetPosition((self.bPSize[0] - 267, 0))
        self.frame.SetSize((160, self.bPSize[1] - 8))
        self.frame.Show(True)
        
    def Refresh(self,record):
        # Update view
        self.Clear()
        self.GetExec(record)

    def Clear(self):
        # Erase view
        self.curView.Clear()
        self.frame.Show(False)

    def FrameInit(self):
        self.frame = wx.Panel(self.bigPanel, -1, style = wx.RAISED_BORDER,
                              pos = (self.bPSize[0] - 267, 0),
                              size = (160, self.bPSize[1] - 8))
        self.frame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.frame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.frame.Show(False)

    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\AlignViewPlugins")
        yPos = 10
        xPos = 5
        self.tabButtons = []
        for i,v in enumerate(self.views.values()):
            self.tabButtons.append(wx.Button(self.frame, -1,
                                             str(v.GetName()),
                                             pos = (xPos,yPos), size = (50,25),
                                             style = wx.NO_BORDER))
            self.tabButtons[-1].SetBackgroundColour(
                self.colorList['ViewPanelGrayFrame']['Back'])
            self.tabButtons[-1].SetForegroundColour(
                self.colorList['ViewPanelGrayFrame']['Fore'])
            xPos += 50
            if (i + 1) % 3 == 0:
                yPos += 35
                xPos = 5
            self.curView = v.Plugin()
            self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.tabButtons[-1])

    def Init(self, parent, bigPanel, colorList):
        # Initialize contents of view
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.colorList = colorList
        self.tabButtons = []
        self.rec = []
        self.FrameInit()
        self.TabButtonInit()
        self.lastButton = self.tabButtons[0]
        
    def GetExec(self, rec):
        # Execute view when called
        self.frame.Show(True)
        self.rec = rec[0][0]
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                self.lastButton.GetId())
        event.SetEventObject(self.lastButton)
        self.DoView(event)

    def DoView(self, event):
        t = self.lastButton
        self.lastButton = event.GetEventObject()
        self.curView.Clear()
        for v in self.views.values():
            if v.GetName() == self.lastButton.GetLabelText():
                self.curView = v.Plugin()
        self.curView.GetExec(self.frame,self.bigPanel,self.rec,self.colorList)

    def GetType(self):
        # Identify default record type.
        return "Alignments"

    def GetName(self):
        # Name used by BioGui
        return "AlignView"

def GetType():
    # Identify default record type.
    return "Alignments"

def GetName():
    # Name used by BioGui
    return "AlignView"
