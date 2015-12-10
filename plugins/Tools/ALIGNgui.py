'''Side note to self- ALIGNGUI WILL BE MUCH HARDER THAN BLASTGUI.
EACH ALIGNMENT PROGRAM REQUIRES DIFFERENT INPUTS.
NEEDS A LOT OF IF STATEMENTS AND A VAGUE SUPROCESS(CLINE) STATEMENT.
OPTIONS MENU BAR POP_UP NEEDS TO GIVE A FAIR DEAL OF FREEDOM.
COMMON INPUT TYPES INCLUDE:
    ALPHABET
    SEQUENCE LENGTH LIMIT
    MATRIX TO USE (BLOSUM62 IS USUALLY STANDARD)
    DIAGNALS
    PERCENT SCORE
    TREE INFO(look up nand read)
    GAP PENALTY
    GAP EXTEND PENALTY
    NUMBER OF ITERATIONS
    SECONDARY STRUCTURE GAP PENALTY
    PROFILES?
LEARN/COPY HOW TO MAKE CHECK BOXES.
GOOD DOCUMENTATION IS NEEDED IN CASE ANYONE WANTS TO MODIFY
THE CODE FOR THEIR OWN SPECIFICS.'''

# Import packages that will be used
# GUI generation Packages
import wx
#Operational Packages
import SysUpdate
import subprocess
import os
import re
import getPlugins as gpi
import MenuToolBarSetup as mtbs
#Packages to handle aligned sequences
from Bio import AlignIO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import AlignOptionsDialog as aod

#----------------------------------------------------------------------------

class GuiFrame(wx.Frame):
    def GetName(self):
        #Method to return name of tool
        return 'Align'

    def GetBMP(self):
        #Method to return identifying image
        return r".\Utils\Icons\alignPuzzle.bmp"

    def OnSize(self, event):
        # Method to respond to window sizing
        self.bPSize = self.GetSize()
        self.panelSQ.Show(False)
        self.panelR.Show(False)
        for b in self.paramBoxes.values():
            b.Show(False)
        self.toolButton.Show(False)
        self.toolButton.SetPosition((self.bPSize[0] - 200,20))
        self.panelSQ.SetSize((self.bPSize[0] - 25,70))
        self.panelSQ.SetPosition((7, 85))
        self.panelR.SetSize((self.bPSize[0] - 25,
                            self.bPSize[1] - 205 - 35 * self.tbOnOff))
        self.paramBoxes['ResultOutput'].SetSize((self.bPSize[0] - 105,
                            self.bPSize[1] - 240 - 35 * self.tbOnOff))
        self.panelR.SetPosition((7, 155))
        for b in self.paramBoxes.values():
            b.Show(True)
        self.toolButton.Show(True)
        self.panelSQ.Show(True)
        self.panelR.Show(True)

    def SetQuery(self, seq):
        for tonto in seq:
            silver = r">" + str(tonto[0].id)+" "+str(tonto[0].seq) + "\n"
            self.paramBoxes['SeqInput'].write(str(silver))

    #----------------------Frame Initialization-----------------
    def HelpExec(self,event):
        # Respond to a type selection
        self.name = self.menuBar.GetLabel(event.GetId())
        self.curPlugin.Clear()
        self.curPlugin = self.plugins[self.name].Plugin()
        if self.tbOnOff == 1:
            self.toolbar.Show(False)
            self.tbOnOff = 0
            self.ccmd = self.curPlugin.Init(self)
            self.DoTBOnOff(wx.EVT_IDLE)
        else:
            self.ccmd = self.curPlugin.Init(self)
        self.typeMenu.Check(event.GetId(), True)
        
    def DoProtien (self, event):
        # Respond to the "Peptide" alphabet command.
        self.abet = "AA"

    def DoRNA (self, event):
        # Respond to the "RNA" alphabet command.
        self.abet = "RNA"

    def DoDNA (self, event):
        # Respond to the "DNA" alphabet command.
        self.abet = "DNA"

    def DoSaveAs(self, event):
        # Respond to the "Save As" menu command.
        if self.fileName == None:
            self.fileName = ""
        fileName = wx.FileSelector("Save File As", "Saving",
                                  default_filename = self.fileName,
                                  default_extension = "xml",
                                  wildcard = "*.xml",
                                  flags = wx.SAVE | wx.OVERWRITE_PROMPT)
        if fileName == "": return # User cancelled.
        fileName = os.path.join(os.getcwd(), fileName)
        self.SetTitle(os.path.basename(fileName))
        self.fileName = fileName
        self.SaveContents()
        
    def DoExit(self, event):
        # Respond to the "Quit" menu command.
        if self.AskIfUserWantsToSave("closing"):
            self.Destroy()

    def SetType(self, name):
        # Method allowing outside programs to set alignment type
        self.name = name
        self.typeMenu.Check(self.plugIds[name], True)

    def SetAbet(self, name):
        # Method allowing outside programs to set alphabet
        self.abet = name
        if name == 'AA':
            self.alphaMenu.Check(self.menu_PROTIEN, True)
        elif name == 'RNA':
            self.alphaMenu.Check(self.menu_RNA, True)
        else:
            self.alphaMenu.Check(self.menu_DNA, True)
        
    def SetOptions(self, opts):
        # Respond to the options dialog closing
        self.options = opts        

    def DoOptions(self, event):
        # Respond to the "Options" menu command.
        self.optBox = aod.optDialog(self, 'Options Menu', self.typeMenu, -1)
        self.optBox.GetOpts(self.abet, self.name)
        self.optBox.ShowModal()
        
    def DoOpen(self, event):
        """ Respond to the "Load" menu command.
        """
        
        self.rec = []
        curDir = os.getcwd()
        fileName = wx.FileSelector("Load File", default_extension=".fasta",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)
        burro = SeqIO.parse(fileName,"fasta")
        for i in burro:
            self.rec.append(i)
        self.curPlugin = self.plugins[self.name].Plugin()
        self.curPlugin.Init(self)
        self.SetParamShape()
        

    def DoNew(self, event):
        """ Respond to the "New" menu command.
        """
        newFrame = GuiFrame(None, -1)
        newFrame.Show(True)

    def SaveContents(self):
        """ Save the contents of our document to disk.
        """
        # SWIG-wrapped native wx contents cannot be pickled, so 
        # we have to convert our data to something pickle-friendly.
        
        try:
            objData = []
            for obj in self.contents:
                objData.append([obj.__class__, obj.getData()])

            f = open(self.fileName, "wb")
            cPickle.dump(objData, f)
            f.close()

            self.dirty = False
            self._adjustMenus()
        except:
            response = wx.MessageBox("Unable to load " + self.fileName + ".",
                                     "Error", wx.OK|wx.ICON_ERROR, self)

    def AskIfUserWantsToSave(self, action):
        """ Give the user the opportunity to save the current document.

            'action' is a string describing the action about to be taken.  If
            the user wants to save the document, it is saved immediately.  If
            the user cancels, we return False.
        """
        
        response = wx.MessageBox("Save changes before " + action + "?",
                                "Confirm", wx.YES_NO | wx.CANCEL, self)

        if response == wx.YES:
            if self.fileName == None:
                fileName = wx.FileSelector("Save File As", "Saving",
                                          default_extension="psk",
                                          wildcard="*.psk",
                                          flags = wx.SAVE | wx.OVERWRITE_PROMPT)
                if fileName == "": return False # User cancelled.
                self.fileName = fileName
            #self.SaveContents()
            return True
        elif response == wx.NO:
            return True # User doesn't want changes saved.
        elif response == wx.CANCEL:
            return False # User cancelled.

    def GetExec(self, event):
        #Tool Executable
        if self.rec == []:
            query = self.paramBoxes['SeqInput'].GetValue()
            if not query == "":
                try:
                    q = query.split('>')
                    for seq in q:
                        s = seq.split('\n')
                        seqID = s[0]
                        st = ''
                        for l in s[1:]:
                            st += l                
                        self.rec.append(SeqRecord(st,id=seqID,name=seqID,description=seqID))
                except:
                    self.paramBoxes['SeqInput'].clear()
                    self.paramBoxes['SeqInput'].write('Incorrect Formatting')
            else:
                self.paramBoxes['SeqInput'].write('enter alignment!')
        SeqIO.write(self.rec,self.homeDir + r"\plugins\my_seq.fasta","fasta")      
        self.cline = self.curPlugin.GetExec(self.optList, self)
        p=subprocess.Popen(str(self.cline))
        p.wait()
        self.outfile = self.curPlugin.GetOutFile()
        self.outtype = self.curPlugin.GetOutType()        
        aligned = AlignIO.read(self.outfile,self.outtype)
        self.curPlugin.DoWrite(aligned)
        self.tempRec = self.rec
        self.rec = []
                 
    def DoAbout(self,event):
        # Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription(
            "Interface to perform Basic Local Alignment Search Tools (BLAST)\n"+
            "Capable of performing searches locally or from NCBI\n\n" +
            "Intended for use with:\n" +
            "BioGui: Graphic User Interface for Biological Work\n" +
            "Developed by:\n" +
            "      The Ahmet Sacan Bioinformaticas Lab\n" +
            "\tSchool of Biomedical Engineering & Health Services\n" +
            "\tDrexel University, Philadelphia, Pennsylvania, 19104\n\n\n" +
            "Files are being checked for irrelevant variable names\n" +
            "If you find some, please keep comments to yourself\n\n" +
            "Copyright is waived until further notice. Aug. 14, 2013")
        wx.AboutBox(info)

    def DoTBOnOff(self,event):
        # Respond to the "Tollbar On/Off" menu command
        self.tbOnOff = abs(self.tbOnOff-1)
        if self.tbOnOff:
            self.toolbar.Show(True)
        else:
            self.toolbar.Show(False)
        self.OnSize(wx.EVT_IDLE)
        self.curPlugin.tbChange(self.tbOnOff)
        
    #----------------------Frame Initialization-----------------
    def VarInit(self):
        # Initialize variables
        self.fileName = ""
        self.name = "CLUSTALW"
        self.abet = "DNA"
        self.gap = 0
        self.gapext = 0
        self.ccmd = 'clustalw'
        self.menuBar = wx.MenuBar()
        self.cline = ''
        self.MaxLen = False
        self.DGLY = False
        self.l4exist = True
        self.rec = []
        self.options = False
        self.optList = []
        self.qseqstr = ''
        self.paramBoxes = {}
        self.plugins = {}
        self.plugIds= {}
        self.bPSize = self.GetSize()
        self.tbOnOff = 1
        #I'm sure more things will go here

    def GetPlugins(self):
        # Method to identify BLAST plugins
        dirt = self.hD+r"\plugins\tools\ALIGNPlugins"
        self.plugins = gpi.GetPlugIns(dirt)
        self.curPlugin = self.plugins[self.name].Plugin()
        self.curPlugin.Init(self)
        self.curPlugin.Clear()
        #self.curPlugin.tbChange(self.tbOnOff)

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def SetPanels(self):
        self.panelSQ = wx.Panel(self, -1, pos=(7,85),
                           size=(self.bPSize[0] - 25,70),
                           style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.panelR = wx.Panel(self, -1, pos = (7,155),
                             size=(self.bPSize[0] - 25,self.bPSize[1] - 225),
                             style=wx.BORDER_RAISED)
        self.panelR.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
                
    def SetViewWindows(self):
        # Create user interface appearance
        self.SetPanels()
        for p in self.paramBoxes.keys():
            self.paramBoxes[p].Show(False)
        #Create sequence input box and label. Allow input to be modified.
        self.paramBoxes['SeqText'] = wx.StaticText(self.panelSQ, -1,
                                                   "Sequences: ", pos=(3,10))
        self.paramBoxes['SeqText'].SetForegroundColour('WHITE')
        self.paramBoxes['SeqInput'] = wx.TextCtrl(self.panelSQ, -1,
                         "", size=(895, 50),pos=(75,10),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        for s in self.rec:
            self.paramBoxes['SeqInput'].write(
                ">" + str(s.id) + ' ' + str(s.seq) + '\n')
            wx.CallAfter(self.paramBoxes['SeqInput'].SetInsertionPoint, 0)
        #Create results outbox and lable. The box is able to be modified.
        self.paramBoxes['ResultText'] = wx.StaticText(self.panelR, -1,
                                                      "Results: ", pos=(3,10))
        self.paramBoxes['ResultText'].SetForegroundColour('WHITE')
        self.paramBoxes['ResultOutput'] = wx.TextCtrl(self.panelR, -1,
                        "", size=(895, 325), pos=(75,10),
                        style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL)
        wx.CallAfter(self.paramBoxes['ResultOutput'].SetInsertionPoint, 0)
        
    def SetButtons(self):
        # Create action button
        self.toolButton = wx.Button(self, -1, "ALIGN", pos=(800,55))
        self.toolButton.SetBackgroundColour(
            self.colorList['ToolButton']['Back'])
        self.toolButton.SetForegroundColour(
            self.colorList['ToolButton']['Fore'])
        self.Bind(wx.EVT_BUTTON, self.GetExec, self.toolButton)
        
    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title='Multiple Alignment Interface')
        #self.parent = parent
        if 'homeDir' in kwargs.keys():
            self.hD = kwargs['homeDir']
        else:
            self.hD = os.getcwd()
        self.VarInit()
        self.GetColors()
        self.SetBackgroundColour(self.colorList['Tool']['Back'])
        self.SetViewWindows()
        self.GetPlugins()
        mts = mtbs.MenuToolBarSetup(self, self.plugins, self.hD)
        self.plugIds = mts.GetIDs()
        mts.DoMenubar("ALIGN!","Perform an Alignment",True,True, False, False)
        mts.DoToolbar()
        self.SetButtons()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.DoExit)
        self.toolbar.Show(False)
        self.tbOnOff = 0
        self.ccmd = self.curPlugin.Init(self)
        self.DoTBOnOff(wx.EVT_IDLE)    

def GetName():
    # Method to return name of tool
    return 'Align'

def GetBMP():
    # Method to return identifying image
    return r".\Utils\Icons\alignPuzzle.bmp"
"""
#----------------------------------------------------------------------------   

#Code to start gui
class MyApp(wx.App):
    def OnInit(self):
        os.chdir(r'C:\Users\francis\Documents\Monguis\BioGui')
        frame = GuiFrame(None,-1,
                         homeDir = r'C:\Users\francis\Documents\Monguis\BioGui')
        self.SetTopWindow(frame)
        frame.Show(True)
        return True            
global app        
app = MyApp(redirect=True)
app.MainLoop()"""




#    Lone Ranger: Hi ho Silver, away! 
#    Tonto:       Never do that again. 
#    Lone Ranger: Sorry. 
#
#
#    From:   The Lone Ranger (2013)
#            http://www.imdb.com/title/tt1210819/

