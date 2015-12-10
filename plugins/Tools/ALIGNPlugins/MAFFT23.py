import wx
from Bio.Align.Applications import MafftCommandline

class Plugin():
    """ A frame showing the contents of a single document. """

    # ==========================================
    # ===== Methods for Plug-in Management =====
    # ==========================================
    
    

    def GetOutFile(self):
        return r"C:\Users\francis\Documents\Monguis\BioGui\plugins\mafft.fasta"

    def GetOutType(self):
        return "fasta"

    def DoWrite(self, inStr):
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
        for v in self.param.values():
            v.Show(True)

    def ParamCheck(self):        
        # Create User Modifiable search check boxes.
        self.param['FFTCheck'] = wx.CheckBox(self.frame, -1, label='Use FFT?', pos=(5,68))
        self.param['FFTCheck'].SetValue(True)
        self.param['ReOCheck'] = wx.CheckBox(self.frame, -1, label='Reorder?', pos=(75,68)) 

    def ParamText(self):
        # Create User Modifiable search check boxes.
        self.param['StrategyText'] = wx.StaticText(self.frame, -1, 'Strategy:', pos=(10,8))
        self.param['GapText'] = wx.StaticText(self.frame, -1, label='Gap \nPenalty:', pos=(10,30))
        self.param['GapExtText'] = wx.StaticText(self.frame, -1, label='Gap Extend\nPenalty:', pos=(200,30))

    def ParamSpin(self):
        self.param['StrategyCombo'] = wx.ComboBox(parent=self.frame, id=-1, pos=(75,8), choices=['AUTO', 'FFT-NS-1   (Fast)', 'FFT-NS-2   (Accurate)', 'G-INS-i    (Global)', 'L-INS-i    (Local)', 'E-INS-i    (Generic)'], style=wx.CB_READONLY)
        self.param['StrategyCombo'].SetSelection(0)
        self.param['GapSpin'] = wx.SpinCtrl(self.frame, -1, size=(75, -1), pos=(75,38))
        self.param['GapSpin'].SetValue(0.153)
        self.param['GapExtSpin'] = wx.SpinCtrl(self.frame, -1, pos=(275,38))
        self.param['GapExtSpin'].SetValue(0.123)
        
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
        # Respond to the 'Mafft' command.
        self.frame = frame
        plugin_exe = r"C:/Program Files (x86)/Mafft/mafft-win/Mafft.bat"
        self.outfile = r"C:\Users\francis\Documents\Monguis\BioGui\plugins\mafft.fasta"
        self.outtype = "fasta"
        self.strategy = self.frame.paramBoxes[5].GetCurrentSelection()
        if self.strategy < 1:
            self.Sstr = " --auto"
        elif self.strategy <2:
            self.Sstr = " --retree 1"
        elif self.strategy < 3:
            self.Sstr = " --retree 2"
        elif self.strategy < 4:
            self.Sstr = " --globalpair --maxiterate 1000"
        elif self.strategy < 5:
            self.Sstr = " --localpair --maxiterate 1000"
        elif self.strategy < 4:
            self.Sstr = " --genafpair --maxiterate 1000"
        #r'"C:\Program Files (x86)\Mafft\mafft-win\mafft.bat"  --auto  --reorder "C:\Users\francis\Documents\Monguis\plugins\my_seq.fasta"  > "C:\Users\francis\Documents\Monguis\plugins\mafft.fasta"'

        self.gapopen = self.frame.paramBoxes["GapPenSpin"].GetValue()
        self.gapextend = self.frame.paramBoxes["GapExtPenSpin"].GetValue()

        if self.frame.abet=="AA":
            self.betStr = "--amino "
        elif self.frame.abet=="DNA" or self.frame.abet=="RNA":
            self.betStr = "--nuc "

        self.cline = str(plugin_exe)+str(self.Sstr)+str(self.betStr)+r"C:\Users\francis\Documents\Monguis\BioGui\plugins\my_seq.fasta" +r" > "+str(self.outfile)

        print self.cline
        '''if self.frame.options:
            t = self.boxList[3].GetValue()
            if t != '':
                cline.datafile = str(t)'''
            
        
        return self.cline

    def GetOpts(self,optBox,frame,abet):
        self.boxList = []
        self.optBox = optBox
        
        self.boxList.append(wx.StaticText(optBox, -1, "Select Matrix File", pos=(150,30)))
        temp = wx.TextCtrl(optBox, -1, "", size=(300, 20),
                     style=wx.TE_PROCESS_ENTER, pos=(150 , 60), name="MatText")
        self.boxList.append(temp)
        temp1 = wx.Button(optBox, -1, "Browse", pos=(460,60))
        optBox.Bind(wx.EVT_BUTTON, self.getMatFile, temp1)
        self.boxList.append(temp1)

        return self.boxList

    def getMatFile(self,event):
        self.dirname = ''
        dlg = wx.FileDialog(self.optBox, "Choose a file", self.dirname,"","*.*", wx.OPEN)
        dlg.ShowModal()



def GetExec(inF,outF):
    # Create User Modifiable search check boxes.
    plugin_exe = r"C:/Program Files (x86)/Mafft/mafft-win/Mafft.bat"
    cline = MafftCommandline(plugin_exe,infile=inF, outfile=outF)
    p=subprocess.Popen(str(self.cline))
    p.wait()

def GetName():
    '''
    Method to return name of tool
    '''
    return "MAFFT"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\71.bmp"
