import wx
from Bio.Align.Applications import ClustalwCommandline

class Plugin():    
    def GetOutFile(self):
        # Method to return default outfile
        self.outfile = r".\Alignments\clustal.aln"
        return self.outfile

    def GetOutType(self):
        # Method to return default outtype
        self.outtype = "clustal"
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
        self.param['FastCheck'].SetValue(False)
        self.param['DiagCheck'].SetValue(False)
        self.param['SlowCheck'].SetValue(False)

    def ShowReady(self):
        # Method to show default parameter boxes
        self.param['PairCheck'].Show(True)
        self.param['ProfileCheck'].Show(True)
        self.param['GapSpin'].Show(True)
        self.param['GapExtSpin'].Show(True)
        self.param['GapText'].Show(True)
        self.param['GapExtText'].Show(True)

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
            
    def DoFast(self,event):
        # Respond to selection of fast checkbox
        if self.param['FastCheck'].GetValue():
            self.param['DiagCheck'].Show(True)
            self.param['SlowCheck'].SetValue(False)
            self.param['GapExtText'].Show(False)
            self.param['KTupleText'].Show(True)
            self.DoSlow(event)
        else:
            self.param['DiagCheck'].SetValue(False)            
            self.param['DiagCheck'].Show(False)
            self.param['SlowCheck'].SetValue(True)
            self.param['GapExtText'].Show(True)
            self.param['KTupleText'].Show(False)

    def DoSlow(self,event):
        # Respond to selection of slow checkbox
        if self.param['SlowCheck'].GetValue():
            self.param['FastCheck'].SetValue(False)
            self.param['GapText'].Show(False)
            self.param['SGapText'].Show(True)  
            self.param['DiagCheck'].SetValue(False)
            self.DoDiag(event)
            self.DoFast(event)
        else:
            self.param['FastCheck'].SetValue(True)
            self.param['DiagCheck'].SetValue(False)
            self.param['DiagCheck'].Show(True)
            self.param['GapText'].Show(True)
            self.param['SGapText'].Show(False)  
            self.DoDiag(event)
            
    def DoProf(self,event):
        # Respond to selection of profile checkbox
        if self.param['ProfileCheck'].GetValue():
            if self.param['PairCheck'].GetValue():
                self.param['PairCheck'].SetValue(False)
            self.DoPair(event)
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

    def DoPair (self, event):
        # Respond to selection of pairwise checkbox
        if self.param['PairCheck'].GetValue():
            self.param['ProfileCheck'].SetValue(False)
            self.DoProf(event)
            self.param['FastCheck'].Show(True)
            self.param['SlowCheck'].Show(True)
            self.param['FastCheck'].SetValue(True)
            self.frame.paramBoxes['Profile2Text'].Show(False)
            self.frame.paramBoxes['Profile2Input'].Show(False)
            self.DoFast(event)
        else:
            self.Clear()
            self.ShowReady()

    def ParamCheck(self):        
        # Create User Modifiable search check boxes.
        self.param['PairCheck']      = wx.CheckBox(self.frame, -1, label="Pairwise?", pos=(75, 68))
        self.param['ProfileCheck']   = wx.CheckBox(self.frame, -1, label="Profile?",  pos=(5,  68))
        self.param['FastCheck']      = wx.CheckBox(self.frame, -1, label="Fast?",     pos=(145,68))
        self.param['DiagCheck']      = wx.CheckBox(self.frame, -1, label="Diagnals?", pos=(245,68))
        self.param['SlowCheck']      = wx.CheckBox(self.frame, -1, label="Slow?",     pos=(195,68))     
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoDiag,      self.param['DiagCheck'])
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoFast,      self.param['FastCheck'])
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoSlow,      self.param['SlowCheck'])
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoPair,      self.param['PairCheck'])
        self.frame.Bind(wx.EVT_CHECKBOX, self.DoProf,      self.param['ProfileCheck'])
        self.param['FastCheck'].Show(False)
        self.param['DiagCheck'].Show(False)
        self.param['SlowCheck'].Show(False)

    def ParamText(self):
        # Create User Modifiable search check boxes.
        self.param['GapText']    = wx.StaticText(self.frame, -1, label="Gap\nPenalty:",        pos=(10,  8))
        self.param['GapExtText'] = wx.StaticText(self.frame, -1, label="Gap Extend\nPenalty:", pos=(200, 8))
        self.param['TopText']    = wx.StaticText(self.frame, -1, label="# Diagonals:",         pos=(10, 40))
        self.param['WinText']    = wx.StaticText(self.frame, -1, label="Window Size:",         pos=(200,40))
        self.param['SGapText']   = wx.StaticText(self.frame, -1, label="PW Gap\nPenalty:",     pos=(10,  8))
        self.param['KTupleText'] = wx.StaticText(self.frame, -1, label="Word Size:",           pos=(200, 8))
        self.frame.paramBoxes['Profile2Text'] = wx.StaticText(self.frame.panelSQ, -1, "", pos=(3,37))
        self.frame.paramBoxes['Profile2Text'].Show(False)
        self.frame.paramBoxes['Profile2Input'] = wx.TextCtrl(self.frame.panelSQ, -1, "", size=(self.S[0] - 105, 23),
                     style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,37))
        self.frame.paramBoxes['Profile2Input'].Show(False)
        self.param['TopText'].Show(False)
        self.param['WinText'].Show(False)
        self.param['SGapText'].Show(False)
        self.param['KTupleText'].Show(False)

    def ParamSpin(self):
        # Create User Modifiable check boxes.
        self.param['GapSpin']    = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75,  8))     
        self.param['GapExtSpin'] = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(275, 8))
        self.param['TopSpin']    = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75, 40))
        self.param['WinSpin']    = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(275,40))
        self.param['WinSpin'].SetValue(0)
        self.param['TopSpin'].SetValue(0)
        self.param['GapExtSpin'].SetValue(self.frame.gapext)
        self.param['GapSpin'].SetValue(self.frame.gap)
        self.param['TopSpin'].Show(False)
        self.param['WinSpin'].Show(False)

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
        # Respond to the "clustalw" type command.
        self.frame = frame
        self.boxList = optList
        plugin_exe = r"C:/Program Files (x86)/ClustalW2/clustalw2.exe"
        dummy = self.GetOutFile()
        dummy = self.GetOutType()
        cline = ClustalwCommandline(plugin_exe,infile=r".\plugins\my_seq.fasta", outfile=self.outfile)
        if self.frame.abet=="AA":
            cline.type="protein"
        else:
            cline.type="dna"
        if '1PairCheck' in self.frame.paramBoxes:
            if self.frame.paramBoxes['1PairCheck'].GetValue():
                if '1PairwFastCheck' in sfbd:
                    if self.frame.paramBoxes['1PairwFastCheck'].GetValue():
                        if 'FastPairGapPenSpin' in self.frame.paramBoxes:
                            cline.pairgap = int(self.frame.paramBoxes['FastPairGapPenSpin'].GetValue())
                        if 'FastKTupleSpin' in self.frame.paramBoxes:
                            cline.ktuple = int(self.frame.paramBoxes['FastKTupleSpin'].GetValue())
                        if '1DiagCheck' in self.frame.paramBoxes:
                            if self.frame.paramBoxes['1DiagCheck'].GetValue:
                                if 'DFastTopDiagsSpin' in self.frame.paramBoxes:
                                    cline.topdiags = int(self.frame.paramBoxes['DFastTopDiagsSpin'].GetValue())
                                if 'DFastDiagWinSpin' in self.frame.paramBoxes:
                                    cline.window = int(self.frame.paramBoxes['DFastDiagWinSpin'].GetValue())
                    else:
                        if 'SlowPairGapPenSpin' in self.frame.paramBoxes:
                            cline.pwgapopen = int(self.frame.paramBoxes['SlowPairGapPenSpin'].GetValue())
                        if 'SlowPairGapExtPenSpin' in self.frame.paramBoxes:
                            cline.pwgapext = int(self.frame.paramBoxes['SlowPairGapExtPenSpin'].GetValue())
                else:
                    if '1ProfileCheck' in self.frame.paramBoxes:
                        if not self.frame.paramBoxes['1ProfileCheck'].GetValue():
                            if 'SlowPairGapPenSpin' in self.frame.paramBoxes:
                                cline.gapopen = int(self.frame.paramBoxes['SlowPairGapPenSpin'].GetValue())
                            if 'SlowPairGapExtPenSpin' in self.frame.paramBoxes:
                                cline.gapext = int(self.frame.paramBoxes['SlowPairGapExtPenSpin'].GetValue())                                
        if self.frame.options:
            cline.output = str(self.boxList[1].GetValue())
            cline.outorder = str(self.boxList[3].GetValue())
            if '1PairCheck' in self.frame.paramBoxes:
                if self.frame.paramBoxes['1PairCheck'].GetValue():
                    if '1PairwFastCheck' in self.frame.paramBoxes:
                        if self.frame.paramBoxes['1PairwFastCheck'].GetValue():
                            cline.score = str(self.boxList[5].GetValue())
                        elif self.frame.abet=="AA":
                            cline.pwmatrix = str(self.boxList[5].GetValue())
                        else:
                            cline.pwdnamatrix = str(self.boxList[5].GetValue())
                    else:
                        if '1ProfileCheck' in self.frame.paramBoxes:
                            if not self.frame.paramBoxes['1ProfileCheck'].GetValue():
                                if self.frame.abet=="AA":
                                    cline.matrix = str(self.boxList[5].GetValue())
                                else:
                                    cline.dnamatrix = str(self.boxList[5].GetValue())
                                cline.nopgap = str(self.boxList[7].GetValue())
                                cline.nohgap = str(self.boxList[9].GetValue())
                                cline.maxdiv = int(self.boxList[11].GetValue())
                                cline.transweight = int(self.boxList[13].GetValue())
                                cline.iteration = str(self.boxList[17].GetValue())
                                cline.numiter = int(self.boxList[15].GetValue())
        return cline
                                    
                                    
    def GetOpts(self, optBox, frame, abet):
        # Create User Modifiable search check boxes.
        self.boxList = []
        self.optBox = optBox
        self.frame = frame
        self.boxList.append(wx.StaticText(optBox, -1, "Output Format", pos=(150,30), name="output"))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,70), choices=["GCG", "GDE", "PHYLIP", "PIR", "NEXUS"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(optBox, -1, "Order of Sequences", pos=(150,100)))
        temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,140), choices=["INPUT", "ALIGNED"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        if '1PairCheck' in self.frame.paramBoxes:
                if self.frame.paramBoxes['1PairCheck'].GetValue():
                    if '1PairwFastCheck' in self.frame.paramBoxes:
                            if self.frame.paramBoxes['1PairwFastCheck'].GetValue():
                                self.boxList.append(wx.StaticText(optBox, -1, "Score", pos=(150,170)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,210), choices=["PERCENT","ABSOLUTE"], style=wx.CB_READONLY)
                                temp.SetSelection(0)
                                self.boxList.append(temp)
                            elif abet=="AA":
                                self.boxList.append(wx.StaticText(optBox, -1, "Protein Weight Matrix", pos=(150,170)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,210), choices=["BLOSUM", "PAM", "GONNET", "ID", "file..."], style=wx.CB_READONLY)
                                temp.SetSelection(0)
                                optBox.Bind(wx.EVT_COMBOBOX, self.DoFileMatrix, temp)
                                self.boxList.append(temp)
                            else:
                                self.boxList.append(wx.StaticText(optBox, -1, "DNA Weight Matrix", pos=(150,170)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,210), choices=["IUB", "CLUSTALW", "file..."], style=wx.CB_READONLY)
                                temp.SetSelection(0)
                                optBox.Bind(wx.EVT_COMBOBOX, self.DoFileMatrix, temp)
                                self.boxList.append(temp)
                else:
                    if '1ProfileCheck' in self.frame.paramBoxes:
                        if not self.frame.paramBoxes['1ProfileCheck'].GetValue():
                                if abet=="AA":
                                    self.boxList.append(wx.StaticText(optBox, -1, "Protein Weight Matrix", pos=(150,170)))
                                    temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,210), choices=["BLOSUM", "PAM", "GONNET", "ID", "file..."], style=wx.CB_READONLY)
                                    temp.SetSelection(0)
                                    optBox.Bind(wx.EVT_COMBOBOX, self.DoFileMatrix, temp)
                                    self.boxList.append(temp)
                                else:
                                    self.boxList.append(wx.StaticText(optBox, -1, "DNA Weight Matrix", pos=(150,170)))
                                    temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,210), choices=["IUB", "CLUSTALW", "file..."], style=wx.CB_READONLY)
                                    temp.SetSelection(0)
                                    optBox.Bind(wx.EVT_COMBOBOX, self.DoFileMatrix, temp)
                                    self.boxList.append(temp)
                                self.boxList.append(wx.StaticText(optBox, -1, "Residue Specific\nGaps", pos=(150,240)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,280), choices=["True","False"], style=wx.CB_READONLY)
                                temp.SetSelection(1)
                                self.boxList.append(temp)
                                self.boxList.append(wx.StaticText(optBox, -1, "Hydrophilic Gaps", pos=(150,240)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(150,280), choices=["True","False"], style=wx.CB_READONLY)
                                temp.SetSelection(1)
                                self.boxList.append(temp)
                                self.boxList.append(wx.StaticText(optBox, -1, "% ident. for delay", pos=(300,30)))
                                self.boxList.append(wx.TextCtrl(optBox, -1, "0", size=(75,-1), pos=(300,50)))
                                self.boxList.append(wx.StaticText(optBox, -1, "Transitions weighting", pos=(300,70)))
                                self.boxList.append(wx.TextCtrl(optBox, -1, "0", size=(75,-1), pos=(300,90)))

                                self.boxList.append(wx.StaticText(optBox, -1, "Max. Iterations", pos=(300,130)))
                                self.boxList.append(wx.TextCtrl(optBox, -1, "1", size=(75,-1), pos=(300,160)))
                                self.boxList.append(wx.StaticText(optBox, -1, "Iteration Focus", pos=(300,200)))
                                temp=wx.ComboBox(parent=optBox, id=-1, pos=(300,230), choices=["NONE", "TREE", "ALIGNMENT"], style=wx.CB_READONLY)
                                temp.SetSelection(1)
                                self.boxList.append(temp)
        self.checkPos = 50
        temp = wx.CheckBox(self.optBox, -1, label="", pos=(450,self.checkPos), name="UserBox")
        self.boxList.append(temp)
        self.optBox.Bind(wx.EVT_CHECKBOX, self.addUserBoxes, temp)
        return self.boxList

    def DoFileMatrix(self, event):
        # Create User Modifiable search check boxes.
        boxer = event.GetEventObject()
        namer = boxer.GetValue()
        if namer == "file...":
            self.dirname = ''
            dlg = wx.FileDialog(self.optBox, "Choose a file", self.dirname,"","*.*", wx.OPEN)
            dlg.ShowModal()

    def addUserBoxes(self,event):
        # Create User Modifiable search check boxes.
        obj = event.GetEventObject()
        if obj.GetValue():
            self.boxList.append(wx.TextCtrl(self.optBox, -1, "", size=(90, 20),
                             style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(500,self.checkPos), name="userBox"))
            self.boxList.append(wx.TextCtrl(self.optBox, -1, "", size=(90, 20),
                             style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(600,self.checkPos), name="userBox"))
            self.checkPos += 30
            temp = wx.CheckBox(self.optBox, -1, label="", pos=(450,self.checkPos), name="UserBoxi")
            self.boxList.append(temp)
            self.optBox.Bind(wx.EVT_CHECKBOX, self.addUserBoxes, temp)
        else:
            j = 0
            while j < 3:
                self.boxList[len(self.boxList)-1].Show(False)
                del self.boxList[len(self.boxList)-1]
                j +=1
            self.checkPos -=30

def GetExec(inF,outF):
    # Create User Modifiable search check boxes.
    plugin_exe = r"C:/Program Files (x86)/ClustalW2/clustalw2.exe"
    cline = ClustalwCommandline(plugin_exe,infile=inF, outfile=outF)
    p=subprocess.Popen(str(self.cline))
    p.wait()

def GetName():
    # Method to return name of tool
    return "CLUSTALW"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\clustalw.bmp"
