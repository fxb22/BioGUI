import wx
import getPlugins as gpi

class Plugin():
    def OnSize(self):
        # Respond to size change
        self.bPSize = self.bigPanel.GetSize()
        self.frame.Show(False)
        self.frame.SetPosition((self.bPSize[0] - 257, 0))
        self.frame.SetSize((150, self.bPSize[1] - 8))
        self.frame.Show(True)
        if hasattr(self, 'curView'):
            self.curView.OnSize()
        
    def Refresh(self,record):
        # Update view
        self.Clear()
        self.curView.Clear()
        self.frame.Show(True)
        self.rec = record
        self.GetExec(record)

    def Clear(self):
        # Erase view
        self.curView.Clear()
        self.frame.Show(False)

    def TabButtonInit(self):
        # Create buttons for plug-ins
        self.views = gpi.GetPlugIns(r".\plugins\Views\SSEViewPlugins")
        self.tabButtons = []
        self.selPos = -1
        yPos = 10
        xPos = 10
        for i,v in enumerate(self.views.values()):
            viewName = v.GetName()
            v = v.Plugin()
            self.tabButtons.append(wx.Button(
                self.frame, -1, str(viewName), pos = (xPos, yPos),
                size = (62, 22), style = wx.NO_BORDER))
            self.tabButtons[i].SetBackgroundColour(
                self.colorList['ViewPanelGrayFrame']['Back'])
            self.tabButtons[i].SetForegroundColour(
                self.colorList['ViewPanelGrayFrame']['Fore'])
            self.curView = v
            self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.tabButtons[i])
            xPos += 62
        self.lastButton = self.tabButtons[0]

    def FrameInit(self):
        # Create frame
        self.frame = wx.Panel(self.bigPanel, -1, 
                                  size = (150, self.bPSize[1] - 8),
                                  pos = (self.bPSize[0] - 257, 0),
                                  style = wx.RAISED_BORDER,)
        self.frame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.frame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.frame.Show(False) 

    def Init(self, parent, bigPanel, colorList):
        # Initialize contents of view
        self.bigPanel = bigPanel
        self.bPSize = self.bigPanel.GetSize()
        self.colorList = colorList
        self.tabButtons = []
        self.rec = []
        self.FrameInit()
        self.TabButtonInit()
        
    def GetExec(self, rec):
        # Execute view when called
        self.frame.Show(True)
        self.rec = rec[0]
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                self.lastButton.GetId())
        event.SetEventObject(self.lastButton)
        self.DoView(event)

    def DoView(self, event):
        self.curView.Clear()
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                self.curView = v.Plugin()
        self.curView.GetExec(self.bigPanel, self.frame, self.rec,self.colorList)

    def GetType(self):
        # Identify default record type.
        return "SSE"

    def GetName(self):
        # Name used by BioGui
        return "SSEView"

def GetType():
    # Identify default record type.
    return "SSE"

def GetName():
    # Name used by BioGui
    return "SSEView"
