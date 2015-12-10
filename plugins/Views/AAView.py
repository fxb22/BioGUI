import wx
from Bio.SeqUtils import ProtParam, ProtParamData
import getPlugins as gpi

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        self.seqText.Show(False)
        self.seqText.SetSize((self.bPSize[0] - 315, self.bPSize[1] - 16))
        self.seqText.Show(True)
        self.frame.Show(False)
        self.frame.SetPosition((self.bPSize[0] - 307, 0))
        self.frame.SetSize((200, self.bPSize[1] - 8))
        self.frame.Show(True)

    def Refresh(self,record):
        self.GetExec(record)

    def Clear(self):
        self.seqText.Show(False)
        self.frame.Show(False)

    def OnScale(self, event):
        num = self.scaleCombo.GetSelection()
        scaleDict = {'Kyte Doolittle phobicity': [ProtParamData.kd, 2, -2],
                     'Hopp Wood philicity': [ProtParamData.hw, .9, -1.2],
                     'Vihinen flexibility': [ProtParamData.Flex,  1.032, .976],
                     'Emini probability': [ProtParamData.em, 1.145, .794],
                     'Janin transfer energy': [ProtParamData.ja, .07, -.7],
                     }
        self.ppd = scaleDict[self.chose[num]][0]
        self.hlim = scaleDict[self.chose[num]][1]
        self.llim = scaleDict[self.chose[num]][2]
        self.DoPrint()

    def OnFrSize(self, event):
        self.DoPrint()

    def SelectColour(self, event):
        """display the colour dialog and select"""
        dlg = wx.ColourDialog(self.bigPanel)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            # gives red, green, blue tuple (r, g, b)
            # each rgb value has a range of 0 to 255
            rgb = data.GetColour().Get()
            evtobj = event.GetEventObject()
            eoID = evtobj.GetName()
            if eoID == 'h':
                self.hButton.SetBackgroundColour(rgb)
                if rgb[0] + rgb[1] + rgb[2] >= 450:
                    self.hButton.SetForegroundColour('BLACK')
                else:
                    self.hButton.SetForegroundColour('WHITE')
            elif eoID == 'l':
                self.lButton.SetBackgroundColour(rgb)
                if rgb[0] + rgb[1] + rgb[2] >= 450:
                    self.lButton.SetForegroundColour('BLACK')
                else:
                    self.lButton.SetForegroundColour('WHITE')
        dlg.Destroy()
        self.DoPrint()

    def FrameInit(self):
        self.frame = wx.Panel(self.bigPanel, -1, style = wx.RAISED_BORDER,
                              pos = (self.bPSize[0] - 307, 0),
                              size = (200, self.bPSize[1] - 8))
        self.frame.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        self.frame.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.frame.Show(False)

    def SliderInit(self):
        textFrameSize = wx.StaticText(self.frame, -1, pos = (15, 30),
                                      label = "Frame Size:")
        textFrameSize.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        textFrameSize.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])        
        self.frSize = wx.SpinCtrl(self.frame, -1, size = (75, -1),
                                  pos = (75, 25))
        self.frame.Bind(wx.EVT_SPINCTRL, self.OnFrSize)

    def ScaleInit(self):
        textScale = wx.StaticText(self.frame, -1, pos = (15, 55),
                                      label = "Scale:")
        textScale.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        textScale.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])
        self.chose = ['Kyte Doolittle phobicity',
                      'Hopp Wood philicity',
                      'Vihinen flexibility',
                      'Emini probability',
                      'Janin transfer energy',
                      ]
        self.scaleCombo = wx.ComboBox(self.frame, -1,
                                      choices = self.chose,
                                      pos = (50, 50), size = (132, -1),
                                      style = wx.CB_READONLY)
        textCol = wx.StaticText(self.frame, -1, pos = (15, 80),
                                      label = "Color:")
        textCol.SetBackgroundColour(
            self.colorList['ViewPanelGrayFrame']['Back'])
        textCol.SetForegroundColour(
            self.colorList['ViewPanelGrayFrame']['Fore'])      
        self.frame.Bind(wx.EVT_COMBOBOX, self.OnScale)
        self.ColButtonInit()

    def ColButtonInit(self):
        self.lButton = wx.Button(self.frame, -1, label = 'lower',
                         pos = (121, 75), size = (61, 20), name = 'l')
        self.lButton.SetBackgroundColour('BLUE')
        self.lButton.SetForegroundColour('WHITE')
        self.lButton.Bind(wx.EVT_BUTTON, self.SelectColour)
        self.hButton = wx.Button(self.frame, -1, label = 'upper',
                         pos = (50, 75), size = (61, 20), name = 'h')
        self.hButton.SetBackgroundColour('RED')
        self.hButton.SetForegroundColour('WHITE')
        self.hButton.Bind(wx.EVT_BUTTON, self.SelectColour)

    def SetText(self):
        self.seqText = wx.TextCtrl(self.bigPanel, -1, "", pos = (5, 5), 
                                   size = (self.bPSize[0] - 315,
                                           self.bPSize[1] - 16),
                                   style = wx.NO_BORDER|wx.TE_MULTILINE|
                                   wx.TE_RICH2|wx.TE_READONLY)
        font = self.seqText.GetFont()
        newFont = wx.Font(font.PointSize + 2, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.seqText.SetFont(newFont)
        self.seqText.SetDefaultStyle(
            wx.TextAttr(self.colorList['ViewPanelList']['Fore'],
                        self.colorList['ViewPanelList']['Back']))
        
    def TabButtonInit(self):
        self.views = gpi.GetPlugIns(r".\plugins\Views\AAViewPlugins")
        xPos = 10
        self.tabButtons = []
        for v in self.views.values():
            self.tabButtons.append(wx.Button(self.frame, -1,
                                             str(v.GetName()),
                                             pos = (xPos, 0), size = (60, 22),
                                             style = wx.NO_BORDER))
            self.tabButtons[-1].SetBackgroundColour(
                self.colorList['ViewPanelGrayFrame']['Back'])
            self.tabButtons[-1].SetForegroundColour(
                self.colorList['ViewPanelGrayFrame']['Fore'])
            xPos += 60
            self.curView = v
            self.frame.Bind(wx.EVT_BUTTON, self.DoView, self.tabButtons[-1])
        self.lastButton = self.tabButtons[2]

    def Init(self, parent, bigPanel, colorList):
        self.colorList = colorList
        self.bigPanel = bigPanel
        self.bPSize = bigPanel.GetSize()
        self.protParamList = []
        self.tabButtons = []
        self.FrameInit()
        self.SliderInit()
        self.ScaleInit()
        self.TabButtonInit()
        self.SetText()
        self.scaleCombo.SetSelection(0)
        self.frSize.SetValue(10)
        self.seqRec = ""
               
    def GetExec(self, seqRec):
        self.frame.Show(True)
        self.seqRec = seqRec[0][0].seq
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                self.lastButton.GetId())
        event.SetEventObject(self.lastButton)
        self.OnScale(wx.EVT_IDLE)
        self.DoView(event)
            
    def DoView(self, event):
        self.lastButton = event.GetEventObject()
        self.buttonLabel = self.lastButton.GetLabelText()
        for j in self.protParamList:
           j.Destroy()
        for v in self.views.values():
            if v.GetName() == self.buttonLabel:
                self.curView = v.Plugin()
        self.curView.GetExec(self.frame, self.bigPanel, self.seqRec,
                             self.frSize)
        self.protParamList = self.curView.GetParamList()
        
    def DoPrint(self):
        self.seqText.Show(False)
        self.seqText.Destroy()
        frVal = self.frSize.GetValue()
        self.SetText()
        maxLen = len(self.seqRec)
        ch = self.hButton.GetBackgroundColour()
        cl = self.lButton.GetBackgroundColour()
        fh = self.hButton.GetForegroundColour()
        fl = self.lButton.GetForegroundColour()
        vals = []   
        i = 0
        while i < maxLen - frVal:
            if frVal == 1:
                vals.append(self.ppd[str(self.seqRec[i])])
            else:
                protAnal = ProtParam.ProteinAnalysis(
                    str(self.seqRec[i:(i + frVal)]))    
                vals = protAnal.protein_scale(self.ppd, frVal)
            self.seqText.AppendText(str(self.seqRec[i:(i + frVal)]))
            if vals[0] < self.llim:
                self.seqText.SetStyle(i, (i + frVal),
                                      wx.TextAttr(fl, cl))
            elif vals[0] > self.hlim:
                self.seqText.SetStyle(i, (i + frVal),
                                      wx.TextAttr(fh, ch))
            i += frVal
        if i < maxLen - 1:
            self.seqText.AppendText(str(self.seqRec[i:maxLen]))

    def GetType(self):
        return "Amino Acids"

    def GetName(self):
        return "AAView"

def GetType():
    return "Amino Acids"

def GetName():
    return "AAView"
