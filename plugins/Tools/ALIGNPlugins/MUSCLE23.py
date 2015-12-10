import wx
from Bio.Align.Applications import MuscleCommandline

class Plugin():
    def GetOutFile(self):
        # Method to return default outfile
        self.outfile = r".\Alignments\muscle1.txt"
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
        self.param['DiagCheck'].Show(True)
        self.param['ProfileCheck'].Show(True)
        self.param['GapSpin'].Show(True)
        self.param['GapText'].Show(True)

    def PanelWrite(self):
        # Replace standard panelSQ objects
        self.frame.paramBoxes['SeqText'].Destroy()
        self.frame.paramBoxes['SeqText'] = wx.StaticText(self.frame.panelSQ, -1, "Profile 1:", pos=(3,10))
        self.frame.paramBoxes['SeqText'].SetForegroundColour('WHITE')
        self.frame.paramBoxes['SeqInput'].Destroy()
        self.frame.paramBoxes['SeqInput'] = wx.TextCtrl(self.frame.panelSQ, -1, "", size=(self.S[0] - 105, 23),
                     style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10))
        self.frame.paramBoxes['Profile2Input'].Destroy()
        self.frame.paramBoxes['Profile2Text'].Destroy()
        self.frame.paramBoxes['Profile2Text'] = wx.StaticText(self.frame.panelSQ, -1, "Profile 2:", pos=(3,37))
        self.frame.paramBoxes['Profile2Text'].SetForegroundColour('WHITE')
        self.frame.paramBoxes['Profile2Input'] = wx.TextCtrl(self.frame.panelSQ, -1, "", size=(self.S[0] - 105, 23),
                     style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,37))
        wx.CallAfter(self.frame.paramBoxes['Profile2Input'].SetInsertionPoint, 0)

    def DoDiag(self, event):
        # Respond to selection of diagnals checkbox
        if self.param['DiagCheck'].GetValue():
            self.param['TopText'].Show(True)
            self.param['WinText'].Show(True)
            self.param['TopSpin'].Show(True)
            self.param['WinSpin'].Show(True)
        else:
            self.param['TopText'].Show(False)
            self.param['WinText'].Show(False)
            self.param['TopSpin'].Show(False)
            self.param['WinSpin'].Show(False)
            
    def DoProf(self,event):
        # Respond to selection of profile checkbox
        if self.param['ProfileCheck'].GetValue():
            self.frame.paramBoxes['SeqText'].Show(False)
            self.frame.paramBoxes['SeqInput'].Show(False)
            self.PanelWrite()
        else:
            self.Clear()    
            self.ShowReady()        
            self.frame.paramBoxes['SeqText'].Show(False)
            self.frame.paramBoxes['SeqInput'].Show(False)
            self.frame.paramBoxes['SeqText'] = wx.StaticText(self.frame.panelSQ, -1, "Sequences:", pos=(3,10))
            self.frame.paramBoxes['SeqText'].SetForegroundColour('WHITE')
            self.frame.paramBoxes['SeqInput'] = wx.TextCtrl(self.frame.panelSQ, -1, "", size=(self.S[0] - 105, 50),
                                                            style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10))
            self.frame.paramBoxes['Profile2Text'].Show(False)
            self.frame.paramBoxes['Profile2Input'].Show(False)
            
    def DoDiag(self, event):
        # Respond to selection of diagnals checkbox
        if self.param['DiagCheck'].GetValue():
            self.param['LenText'].Show(True)
            self.param['MargText'].Show(True)
            self.param['BreakText'].Show(True)
            self.param['LenSpin'].Show(True)
            self.param['MargSpin'].Show(True)
            self.param['BreakSpin'].Show(True)
        else:
            self.param['LenText'].Show(False)
            self.param['MargText'].Show(False)
            self.param['BreakText'].Show(False)
            self.param['LenSpin'].Show(False)
            self.param['MargSpin'].Show(False)
            self.param['BreakSpin'].Show(False)


    def ParamCheck(self):        
        # Create User Modifiable search check boxes.
        self.param['ProfileCheck'] = wx.CheckBox(self.frame, -1, label="Profile?",  pos=(5,  68))
        self.param['DiagCheck']    = wx.CheckBox(self.frame, -1, label="Diagnals?", pos=(75, 68))   
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoDiag, self.param['DiagCheck'])
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoProf, self.param['ProfileCheck'])

    def ParamText(self):
        # Create User Modifiable search check boxes.
        self.param['GapText']   = wx.StaticText(self.frame, -1, "Gap\nPenalty:",        pos=(10,  8))
        self.param['LenText']   = wx.StaticText(self.frame, -1, "Diagnal\nLength:",     pos=(10, 33))
        self.param['MargText']  = wx.StaticText(self.frame, -1, "Diagnal Margin:",      pos=(200,40))
        self.param['BreakText'] = wx.StaticText(self.frame, -1, "Max. Diagnal\nBreak:", pos=(400,33))
        self.param['LenText'].Show(False)
        self.param['MargText'].Show(False)
        self.param['BreakText'].Show(False)

    def ParamSpin(self):
        # Create User Modifiable check boxes.
        self.param['GapSpin']   = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75,  8))     
        self.param['LenSpin']   = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75, 38))
        self.param['MargSpin']  = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(275,38))
        self.param['BreakSpin'] = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(475,38))
        self.param['GapSpin'].SetValue(self.frame.gap)
        self.param['LenSpin'].SetValue(24)                    
        self.param['MargSpin'].SetValue(5)
        self.param['BreakSpin'].SetValue(1)
        self.param['LenSpin'].Show(False)
        self.param['MargSpin'].Show(False)
        self.param['BreakSpin'].Show(False)

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
        
    def GetExec(self, optList, frame):
        # Respond to the "muscle" command.
        self.frame = frame
        plugin_exe = r"C:/Program Files (x86)/py27/Lib/site-packages/Muscle.exe"
        self.outfile=r".\plugins\muscle.txt"
        self.outtype="fasta"
        cline = MuscleCommandline(plugin_exe,out=self.outfile)
        if '1ProfileCheck' in self.frame.paramBoxes:
            if self.frame.paramBoxes['1ProfileCheck'].GetValue():
                cline.profile = True
                cline.in1 = r"C:\Users\francis\Documents\Monguis\BioGui\plugins\my_seq.fasta"
                cline.in2 = r"C:\Users\francis\Documents\Monguis\BioGui\plugins\my_seq.fasta"
            else:
                cline.input = r"C:\Users\francis\Documents\Monguis\BioGui\plugins\my_seq.fasta"
        if '1DiagCheck' in self.frame.paramBoxes:
            if self.frame.paramBoxes['1DiagCheck'].GetValue():
                cline.diags=True
                if "DiagLenSpin" in self.frame.paramBoxes:
                    cline.diaglength=int(self.frame.paramBoxes["DiagLenSpin"])
                if "DiagMargSpin" in self.frame.paramBoxes:
                    cline.diaglength=int(self.frame.paramBoxes["DiagMargSpin"])
                if "DiagBreakSpin" in self.frame.paramBoxes:
                    cline.diaglength=int(self.frame.paramBoxes["DiagBreakSpin"])
            elif "GapPenSpin" in self.frame.paramBoxes:
                cline.gapopen=float(self.frame.paramBoxes["GapPenSpin"].GetValue())
            else:
                cline.input=r"C:\Users\francis\Documents\Monguis\BioGui\plugins\my_seq.fasta"
        if self.frame.abet=="AA":
            cline.seqtype="protein"
        elif self.frame.abet=="DNA" or self.frame.abet=="RNA":
            cline.seqtype="nucleo"
        else:
            cline.seqtype="auto"
        
        
        if self.frame.options:
            cline.objscore=str(self.boxList[9].GetValue())
            cline.weight1=str(self.boxList[13].GetValue())
            cline.weight2=str(self.boxList[15].GetValue())
            cline.anchorspacing=int(self.boxList[17].GetValue())
            cline.center=float(self.boxList[19].GetValue())
            cline.hydro=int(self.boxList[21].GetValue())
            cline.hydrofactor=float(self.boxList[23].GetValue())
            cline.maxhours=float(self.boxList[25].GetValue())
            cline.maxiters=int(self.boxList[27].GetValue())
            cline.maxtrees=int(self.boxList[29].GetValue())
            cline.minbestcolscore=float(self.boxList[31].GetValue())
            cline.minsmoothscore=float(self.boxList[33].GetValue())
            cline.smoothscoreceil=float(self.boxList[35].GetValue())
            cline.smoothwindow=int(self.boxList[37].GetValue())
            cline.sueff=float(self.boxList[39].GetValue())
        
        return str(cline)

    def GetOpts(self,optBox,frame,abet):
        self.boxList = []
        
        self.boxList.append(wx.StaticText(optBox, -1, "Clustering Algorithm\n1st Iteration", pos=(150,30)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,70), choices=["upgma","upgmb","neighborjoining"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Clustering Algorithm\n2nd Iteration", pos=(150,100)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,140), choices=["upgma","upgmb","neighborjoining"], style=wx.CB_READONLY)
        temp.SetSelection(1)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Distance Measure 1", pos=(150,170)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,200), choices=["kmer6_6","kmer20_3", "kmer20_4", "kbit20_3", "kmer4_6"], style=wx.CB_READONLY)
        if abet=="AA":
            temp.SetSelection(0)
            self.boxList.append(temp)
        else:
            temp.SetSelection(4)
            self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Distance Measures 2", pos=(150,225)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,250), choices=["kmer6_6","kmer20_3", "kmer20_4", "kbit20_3","pctid_kimura","pctid_log"], style=wx.CB_READONLY)
        temp.SetSelection(4)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Objective Scores", pos=(150,280)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,300), choices=["sp","ps","dp","xp","spf","spm"], style=wx.CB_READONLY)
        temp.SetSelection(5)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Tree Root Methods", pos=(150,330)))
        self.boxList.append(wx.ComboBox(parent=optBox, id=-1, pos=(150,350), choices=["psuedo","midlongestspan","minavgleafdist"], style=wx.CB_READONLY))    

        self.boxList.append(wx.StaticText(optBox, -1, "1st Weighting Scheme", pos=(300,140)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(300,160), choices=["none", "clustalw", "henikoff", "henikoffpb","gsc", "threeway"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "2nd Weighting Scheme", pos=(300,180)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(300,200), choices=["none", "clustalw", "henikoff", "henikoffpb","gsc", "threeway"], style=wx.CB_READONLY)
        temp.SetSelection(1)
        self.boxList.append(temp)

        self.boxList.append(wx.StaticText(optBox, -1, "Anchor Spacing", pos=(300,30)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "32", size=(75,-1), pos=(300,50)))
        self.boxList.append(wx.StaticText(optBox, -1, "Center", pos=(300,80)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1.0", size=(75,-1), pos=(300,100)))

        self.boxList.append(wx.StaticText(optBox, -1, "Hydrophobic Window", pos=(500,30)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "5", size=(75,-1), pos=(500,50)))
        self.boxList.append(wx.StaticText(optBox, -1, "Hydrophobic Gap Penalty", pos=(500,80)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1.2", size=(75,-1), pos=(500,100)))

        self.boxList.append(wx.StaticText(optBox, -1, "Max. Hours to Run", pos=(500,130)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "0.0", size=(75,-1), pos=(500,150)))
        self.boxList.append(wx.StaticText(optBox, -1, "Max. Iterations", pos=(500,180)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "16", size=(75,-1), pos=(500,200)))

        self.boxList.append(wx.StaticText(optBox, -1, "Max. Trees", pos=(500,230)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1", size=(75,-1), pos=(500,250)))

        self.boxList.append(wx.StaticText(optBox, -1, "Min. Best Column Score", pos=(650,30)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1.0", size=(75,-1), pos=(650,50)))
        self.boxList.append(wx.StaticText(optBox, -1, "Min. Smooth Score", pos=(650,80)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1.0", size=(75,-1), pos=(650,100)))
        self.boxList.append(wx.StaticText(optBox, -1, "Smooth Score Ceiling", pos=(650,130)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "1.0", size=(75,-1), pos=(650,150)))
        self.boxList.append(wx.StaticText(optBox, -1, "Smooth Window", pos=(650,180)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "7", size=(75,-1), pos=(650,200)))

        self.boxList.append(wx.StaticText(optBox, -1, "SUEFF Value", pos=(650,230)))
        self.boxList.append(wx.TextCtrl(optBox, -1, "0.1", size=(75,-1), pos=(650,250)))

        return self.boxList

def GetExec(inF,outF):
    # Create User Modifiable search check boxes.
    plugin_exe = r"C:/Program Files (x86)/py27/Lib/site-packages/Muscle.exe"
    cline = MuscleCommandline(plugin_exe,infile=inF, outfile=outF)
    p=subprocess.Popen(str(self.cline))
    p.wait()


def GetName():
    # Method to return name of tool
    return "MUSCLE"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\muscle1.bmp"

