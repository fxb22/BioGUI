import wx   
from Bio.Emboss.Applications import WaterCommandline

class Plugin():
    def GetOutFile(self):
        # Method to return default outfile
        self.outfile = r".\Alignments\water.txt"
        return self.outfile

    def GetOutType(self):
        # Method to return default outtype
        self.outtype = "fasta"
        return self.outtype

    def DoWrite(self, inStr):
        # Method to write data to result box
        self.frame.paramBoxes['ResultOutput'].Clear()
        font = self.frame.paramBoxes['ResultOutput'].GetFont()
        newFont = wx.Font(font.PointSize, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.frame.paramBoxes['ResultOutput'].SetFont(newFont)
        maxIDlen = 0
        for record in inStr:
            if len(record.id) > maxIDlen:
                maxIDlen = len(record.id)
        for r,record in enumerate(inStr):
            if r > 0:
                spacer = 0
                while spacer < maxIDlen + 3:
                    self.frame.paramBoxes['ResultOutput'].write(' ')
                    spacer += 1
                for pos,letter in enumerate(record.seq):
                    if not letter == '.':
                        if letter == inStr[r -1].seq[pos]:
                            self.frame.paramBoxes['ResultOutput'].write(r'|')
                        else:
                            self.frame.paramBoxes['ResultOutput'].write(r' ')
                    else:
                        self.frame.paramBoxes['ResultOutput'].write(r' ')
                self.frame.paramBoxes['ResultOutput'].write('\n')
            self.frame.paramBoxes['ResultOutput'].write(str(record.id))
            addonlen = maxIDlen - len(record.id)
            while addonlen > 0:
                self.frame.paramBoxes['ResultOutput'].write(' ')
                addonlen -= 1
            self.frame.paramBoxes['ResultOutput'].write(' - ' + str(record.seq) + '\n')                    
        wx.CallAfter(self.frame.paramBoxes['ResultOutput'].SetInsertionPoint, 0)

    def Clear(self):
        # Method to clear parameter boxes
        for v in self.param.values():
            v.Show(False)

    def ShowReady(self):
        # Method to show default parameter boxes
        self.param['SimCheck'].Show(True)
        self.param['GapSpin'].Show(True)
        self.param['GapExtSpin'].Show(True)
        self.param['GapText'].Show(True)
        self.param['GapExtText'].Show(True)

    def ParamCheck(self): 
        # Create User Modifiable check boxes.
        self.param["SimCheck"]       = wx.CheckBox(self.frame, -1, label="Display Similarity?", pos=(5,68))
        
    def ParamText(self):
        # Create User Modifiable search check boxes.
        self.param['GapText']    = wx.StaticText(self.frame, -1, label="Gap\nPenalty:",        pos=(10,  8))
        self.param['GapExtText'] = wx.StaticText(self.frame, -1, label="Gap Extend\nPenalty:", pos=(200, 8))
        
    def ParamSpin(self):
        # Create User Modifiable check boxes.
        self.param['GapSpin']    = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75,  8))     
        self.param['GapExtSpin'] = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(275, 8))
        self.param['GapExtSpin'].SetValue(self.frame.gapext)
        self.param['GapSpin'].SetValue(self.frame.gap)

    def tbChange(self, tb):
        # Create User Modifiable search check boxes.
        if tb == 0:
            tb = -1
        self.tb = tb
        for p in self.param.values():
            t = p.GetPosition()
            p.SetPosition((t[0], t[1] + 35 * self.tb))
                          
    def Init(self, parent):
        # Create User Modifiable search check boxes.
        self.frame = parent
        self.S = parent.GetSize()
        self.param = dict()
        self.ParamCheck()
        self.ParamText()
        self.ParamSpin()
        self.frame.paramBoxes['SeqText'].Show(False)
        self.frame.paramBoxes['SeqText'] = wx.StaticText(self.frame.panelSQ, -1, "Sequence A: ", pos=(3,10))
        self.frame.paramBoxes['SeqText'].SetForegroundColour('WHITE')
        self.frame.paramBoxes['SeqInput'].SetSize((895,23))
        self.frame.paramBoxes['BSeqText'] = wx.StaticText(self.frame.panelSQ, -1, "Sequence B: ", pos=(3,37))
        self.frame.paramBoxes['BSeqText'].SetForegroundColour('WHITE')
        self.frame.paramBoxes['BSeqInput'] = wx.TextCtrl(self.frame.panelSQ, -1, "", size=(895, 23),
                 style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,37))
        wx.CallAfter(self.frame.paramBoxes['BSeqInput'].SetInsertionPoint, 0)
        
    def GetExec(self, optList, frame):
        # Respond to the "embossn" type command.
        self.frame = frame
        plugin_exe = r"C:/mEMBOSS/water.exe"
        self.outfile = r"C:\Users\francis\Documents\Monguis\BioGui\plugins\water.txt"
        self.outtype = "fasta"
        cline = WaterCommandline(plugin_exe, asequence=str(self.frame.paramBoxes[1].GetValue()), bsequence=str(self.frame.paramBoxes[3].GetValue()))
        cline.outfile = self.outfile
        cline.gapopen = self.param[7].GetValue()
        cline.gapextend = self.param[9].GetValue()
        if self.param[10].GetValue():
            cline.similarity = True
        else:
            cline.similarity = False

        if self.frame.abet=="AA":
            cline.snucleotide = True
            cline.sprotein = False
        elif self.frame.abet=="DNA" or self.frame.abet=="RNA":
            cline.snucleotide = True
            cline.sprotein = False
        if self.frame.options:
            t = self.boxList[3].GetValue()
            if t != '':
                cline.datafile = str(t)   
        return str(cline)

    def GetOpts(self,optBox,frame,abet):
        self.boxList = []
        self.optBox = optBox
        self.boxList.append(wx.StaticText(optBox, -1, "Select Matrix File", pos=(150,30)))
        temp = wx.TextCtrl(optBox, -1, "", size=(300, 20),
                     style=wx.TE_PROCESS_ENTER, pos=(150 , 60), name="MatText")
        self.boxList.append(temp)
        temp1 = wx.Button(optBox, -1, "Browse", pos=(460,60))
        optBox.Bind(wx.EVT_BUTTON, self.DoFileMatrix, temp1)
        self.boxList.append(temp1)
        return self.boxList

    def DoFileMatrix(self,event):
        self.dirname = ''
        dlg = wx.FileDialog(self.optBox, "Choose a file", self.dirname,"","*.*", wx.OPEN)
        dlg.ShowModal()

def GetExec(inF,outF):
    # Create User Modifiable search check boxes.
    plugin_exe = r"C:/mEMBOSS/water.exe"
    cline = WaterCommandline(plugin_exe,infile=inF, outfile=outF)
    p=subprocess.Popen(str(self.cline))
    p.wait()


def GetName():
    # Method to return name of tool
    return "EMBOSS WATER"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\embosswater1.bmp"
