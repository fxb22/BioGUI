import wx
import urllib
import urllib2
import os

class customColorDialog(wx.Dialog):
    def DialogSetup(self):
        self.rows = []
        yPos = 25
        while yPos <= 155:
            temp = wx.TextCtrl(self, -1, "", size = (60, 20), pos=(20, yPos),
                               style = wx.TE_PROCESS_ENTER)
            button = wx.Button(self, -1, label = '', pos=(90,yPos),
                               size = (60, 20), style = wx.BORDER_RAISED)
            button.Bind(wx.EVT_BUTTON, self.selectColour)
            self.rows.append([temp, button])
            yPos += 30

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = 'Custom Color Dialog',
                           size = (170, 200))
        self.SetBackgroundColour('LIGHT GRAY')
        self.DialogSetup()
        bgText = wx.StaticText(self, -1, "Symbols", style=wx.NO_BORDER,
                               pos = (30, 5), size = (80,-1))
        fgText = wx.StaticText(self, -1, "Color", style=wx.NO_BORDER,
                               pos = (105,5), size = (80,-1))
        self.Bind(wx.EVT_CLOSE, self.doExit)
                
    def selectColour(self, event):
        # Display the colour dialog and allow user selection"""
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            rgb = data.GetColour().Get()
            evtObj = event.GetEventObject()
            eoId = evtObj.SetBackgroundColour(rgb)
            self.Refresh()
        dlg.Destroy()

    def doExit(self, event):
        self.Destroy()
        
    def GetReturn(self):
        ret = {}
        for i,r in enumerate(self.rows):
            ret['symbols' + str(i)] = str(r[0].GetValue())
            rgb = r[1].GetBackgroundColour()
            s = 'rgb('
            for c in rgb:
                s += str(c) + ','
            s = s[:-1] + ')'
            if s == 'rgb(212,208,200)':
                s = ''
            ret['color' + str(i)] = s
        return ret

class Plugin():
    def Clear(self):
        if hasattr(self, 'coverPanel'):
            self.coverPanel.Show(False)
            self.frameBox.Show(False)
            self.createButton.Show(False)

    def SaveImg(self, event):
        fname = 'WebLogo'
        #curDir = os.getcwd()
        fileName = wx.FileSelector("Save File As", "Saving",
                                   default_filename = fname,
                                   default_extension = "png",
                                   wildcard = "*.png",
                                   flags = wx.SAVE | wx.OVERWRITE_PROMPT)
        if not fileName == "":
            self.wl.SaveFile(fileName, wx.BITMAP_TYPE_PNG)
        #os.chdir(curDir)

    def CoverInit(self):
        self.coverPanel = wx.Panel(self.bigPanel, -1, pos = (0, 0),
                                   size = (self.bPSize[0] - 277,
                                           self.bPSize[1] - 8))
        self.coverPanel.Show(True)
        fs = self.frame.GetSize()
        self.frameBox = wx.ScrolledWindow(self.frame, -1, pos = (2, 80),
                                          size = (fs[0] - 10, fs[1] - 120),
                                          style = wx.VSCROLL|wx.BORDER_SUNKEN)
        self.frameBox.SetBackgroundColour('WHITE')
        self.frameBox.Show(True)

    def FrameBoxFill(self):
        yPos = 5
        for opt in self.options:
            if '\n' in opt[1]:
                yp = yPos - 3
            else:
                yp = yPos + 3
            dummy = wx.StaticText(self.frameBox, -1, opt[1], pos=(3,yp))
            opt[2].SetSize((self.frameBox.GetSize()[0] - 80, -1))
            osi = opt[2].GetSize()
            if not osi[1] == 21:
                opt[2].SetPosition((57, yPos + (21-osi[1])/2))
            else:                
                opt[2].SetPosition((57, yPos))
            opt[2].SetValue(opt[3])
            yPos += 30

    def OptionsInit(self):
        ta = ['alphabet_auto','alphabet_protein','alphabet_dna','alphabet_rna']
        tb = ['probability','bits','nats','kT','kJ/mol','kcal/mol']
        tc = ['comp_none','comp_auto','comp_equiprobable','comp_CG',
              'comp_Celegans','comp_Dmelanogaster','comp_Ecoli',
              'comp_Hsapiens','comp_Mmusculus','comp_Scerevisiae']
        td = ['color_auto','color_monochrome','color_base_pairing',
              'color_classic','color_hydrophobicity','color_chemistry',
              'color_charge','color_custom']
        self.options = [['stacks_per_line','Residues\nper line:',
                         wx.SpinCtrl(self.frameBox, -1),40],
                        ['alphabet','Sequence\ntype:',
                         wx.ComboBox(self.frameBox,-1,choices=ta,
                                     style=wx.CB_READONLY),ta[0]],
                        ['unit_name','Units:',
                         wx.ComboBox(self.frameBox,-1,choices=tb,
                                     style=wx.CB_READONLY),tb[1]],
                        ['logo_start','Start res.:',
                         wx.TextCtrl(self.frameBox, -1, "",),'1'],
                        ['logo_end','Final res.:',
                         wx.TextCtrl(self.frameBox, -1, "",),
                         str(len(self.rec[0].seq))],
                        ['composition','Comp.:',
                         wx.ComboBox(self.frameBox,-1,choices=tc,
                                     style=wx.CB_READONLY),tc[1]],
                        ['show_errorbars','Error\nbars?',
                         wx.CheckBox(self.frameBox, -1, label=""),True],
                        ['logo_title','Title:',
                         wx.TextCtrl(self.frameBox, -1, ""),''],
                        ['logo_label','Label:',
                         wx.TextCtrl(self.frameBox, -1, ""),''],
                        ['show_xaxis','X-axis?',
                         wx.CheckBox(self.frameBox, -1, label=""),True],
                        ['show_yaxis','Y-axis?',
                         wx.CheckBox(self.frameBox, -1, label=""),True],
                        ['show_ends','Seq.\nends?',
                         wx.CheckBox(self.frameBox, -1, label=""),True],
                        ['show_fineprint','Fine\nprint?',
                         wx.CheckBox(self.frameBox, -1, label=""),True],
                        ['color_scheme','Coloring:',
                         wx.ComboBox(self.frameBox,-1,choices=td,
                                     style=wx.CB_READONLY),td[0]]]
        self.FrameBoxFill()

    def MessageDia(self, string):
        dialog = wx.MessageDialog(self.frame, string, 'Error', style=wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def SanitizeChecks(self):
        if not self.para['show_errorbars']:
            del self.para['show_errorbars']
        if not self.para['show_ends']:
            del self.para['show_ends']
        if not self.para['show_fineprint']:
            del self.para['show_fineprint']
        if not self.para['show_xaxis']:
            del self.para['show_xaxis']
        else:
            dialog = wx.TextEntryDialog(self.frame,
                                        "Enter X-axis label.",
                                        "X-axis label", "",
                                        style=wx.OK|wx.CANCEL)
            if dialog.ShowModal() == wx.ID_OK:
                dV = dialog.GetValue()
            else:
                dV = ''
            self.para['xaxis_label'] = str(dV)
            dialog.Destroy()
        if not self.para['show_yaxis']:
            del self.para['show_yaxis']
        else:
            dialog = wx.TextEntryDialog(self.frame,
                                        "Enter Y-axis label.",
                                        "Y-axis label", "",
                                        style=wx.OK|wx.CANCEL)
            if dialog.ShowModal() == wx.ID_OK:
                dV = dialog.GetValue()
            else:
                dV = ''
            self.para['yaxis_label'] = str(dV)
            dialog.Destroy()

    def SanitizeNucleo(self):
        i = 0
        lines = self.para['sequences']
        while i < len(lines) and lines[i] in 'ATGCU -\n':
            i += 1
        if i == len(lines) and self.para['composition'] == 'comp_CG':
            dialog = wx.TextEntryDialog(self.frame,
                                        "Enter expected CG content.",
                                        "CG Content", "",
                                        style=wx.OK|wx.CANCEL)
            if dialog.ShowModal() == wx.ID_OK:
                dV = dialog.GetValue()
                if dV.isdigit() and int(dV) < 100:
                    self.para['percentCG'] = str(dV)
                else:
                    self.para['composition'] = 'comp_auto'
                    s = 'Value entered was incorrect.\n'
                    s += 'Automatic composition used instead.'
                    self.MessageDia(s)
            else:
                self.para['composition'] = 'comp_auto'
                s = 'User cancelled before entering a valid composition.\n'
                s += 'Automatic composition used instead.'
                self.MessageDia(s)
            dialog.Destroy()
        else:
            self.para['composition'] = 'comp_auto'
            s = 'The supplied sequences contained characters\n'
            s += 'not in the set of standard nucleotides, [A,T,G,C,U].\n'
            s += 'Automatic composition was used instead.'
            self.MessageDia(s)
                
    def ShowImage(self, event):
        if hasattr(self, 'display'):
            self.display.Show(False)
        u = 'http://weblogo.threeplusone.com/create.cgi'
        lines = ''
        for r in self.rec:
            lines += r.seq + '\n'
        self.para = {}
        self.para['sequences']=lines
        for opt in self.options:
            self.para[opt[0]] = opt[2].GetValue()
        self.SanitizeChecks()
        if not self.para['composition'] in ['comp_none','comp_auto']:
            self.SanitizeNucleo()
        if self.para['color_scheme'] == 'color_custom':
            cCD = customColorDialog(self.frame)
            cCD.ShowModal()
            cols = cCD.GetReturn()
            for k in cols.keys():
                self.para[k] = cols[k]
        params = urllib.urlencode(self.para)
        imgpage = urllib.urlopen(u, params)
        iFile = './Plugins/weblogo.png'
        img = open(iFile,'wb')
        img.write(imgpage.read())
        img.close()
        self.wl = wx.Image(iFile, wx.BITMAP_TYPE_ANY)
        self.wl = self.wl.Rescale(self.bPSize[0] - 267,self.bPSize[1]-5)
        self.display = wx.StaticBitmap(self.coverPanel, -1, pos = (0, 0),
                                  bitmap = self.wl.ConvertToBitmap(),
                                  size=(self.bPSize[0]-267,self.bPSize[1]-5))
        self.display.Bind(wx.EVT_RIGHT_DOWN, self.SaveImg)

    def GetExec(self, fr, bp, rec, cL):
        self.frame = fr
        self.bigPanel = bp
        self.bPSize = bp.GetSize()
        self.colorList = cL
        self.rec = rec
        self.CoverInit()
        self.OptionsInit()
        self.createButton = wx.Button(self.frame, -1, "CREATE",
                                      pos = (5,self.frame.GetSize()[1] - 35),
                                      size = (self.frame.GetSize()[0] - 10,25))
        self.frame.Bind(wx.EVT_BUTTON, self.ShowImage, self.createButton)
        self.frameBox.SetScrollbars(0, 1, 0, len(self.options)*30+13)
        self.frameBox.SetScrollRate(15, 35)

def GetName():
    return "WebLogo"
