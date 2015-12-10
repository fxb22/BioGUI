import wx

class changeColorDialog(wx.Dialog):
    # A dialog window allowing the change the color scheme of BioGUI
    def DialogSetup(self):
        self.textDict = {}
        self.textNames = self.cL.keys()
        xPos = 30
        yPos = 50
        for text in self.textNames:
            temp = wx.StaticText(self, -1, text, pos = (xPos,yPos+3), 
                                 size = (120,-1), style = wx.SUNKEN_BORDER |
                                 wx.ALIGN_CENTRE_HORIZONTAL)
            temp.SetBackgroundColour(self.cL[text]['Back'])
            temp.SetForegroundColour(self.cL[text]['Fore'])
            self.textDict[text] = temp
            button = wx.Button(self, -1, label = 'change...',
                               pos=(xPos + 130,yPos),
                               name = text + r' Back')
            button.Bind(wx.EVT_BUTTON, self.selectColour)
            button = wx.Button(self, -1, label = 'change...',
                               pos=(xPos + 210,yPos),
                               name = text + r' Fore')
            button.Bind(wx.EVT_BUTTON, self.selectColour)
            yPos += 45

    def __init__(self, parent, cL, hD):
        wx.Dialog.__init__(self, parent, title = 'Color Change Dialog',
                           size = (350, len(cL)*45+80))
        self.saveDir = hD + r"\Utils"
        self.SetBackgroundColour('LIGHT GRAY')
        self.cL = cL
        self.DialogSetup()
        bgText = wx.StaticText(self, -1, "Background", style=wx.NO_BORDER,
                               pos = (170,20), size = (80,25))
        fgText = wx.StaticText(self, -1, "Foreground", style=wx.NO_BORDER,
                               pos = (250,20), size = (80,25))
        self.Bind(wx.EVT_CLOSE, self.doExit)
                
    def selectColour(self, event):
        # Display the colour dialog and allow user selection"""
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            rgb = data.GetColour().Get()
            h = '#'
            l = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F']
            for c in rgb:
                t = c / 16
                u = c % 16
                h += l[t]+l[u]
            evtObj = event.GetEventObject()
            eoId = evtObj.GetName()
            self.cL[eoId[:-5]][eoId[-4:]] = h
            if eoId[-4] == 'B':
                self.textDict[eoId[:-5]].SetBackgroundColour(h)
            else:
                self.textDict[eoId[:-5]].SetForegroundColour(h)
            self.Refresh()
        dlg.Destroy()

    def doExit(self, event):
        f = open(self.saveDir+r"\userColors.py",'w')
        a = 'def getColors():\n    '
        a += '# An object to return a dict of  color schemes\n    '
        a += 'colors = {\n'
        for text in self.textNames:
            a += '        # ' + text + ' Background,Foreground\n        '
            a += "'" + text + "':"
            num = len(text)
            while num < 24:
                a += ' '
                num += 1
            a += "{'Back': '"+str(self.cL[text]['Back'])+"'"
            a += ", 'Fore': '"+str(self.cL[text]['Fore'])+"'},\n"
        a += '    }\n    return colors'
        f.write(a)
        f.close()
        self.Destroy()
        return self.cL
