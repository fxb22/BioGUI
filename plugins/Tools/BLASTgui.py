# Import packages that will be used
# GUI generation Packages
import wx
from wx.lib.buttons import GenBitmapButton,GenBitmapToggleButton
#Operational Packages
import SysUpdate
import subprocess
import os
import getPlugins as gpi
import listControl as lc
#BLAST specific packages
from Bio.Blast import NCBIXML
import BLASTView as bv
from Bio.Blast import NCBIXML
import BlastOptionsDialog as bod

class GuiFrame(wx.Frame):
    def GetName(self):
        # Method to return name of tool
        return 'BLAST'

    def GetBMP(self):
        # Method to return identifying image
        return r".\Utils\Icons\BLASTstar.bmp"
                
    def OnSize(self, event):
        # Method to respond to window sizing
        self.bPSize = self.GetSize()
        self.panelSQ.Show(False)
        self.panelR.Show(False)
        self.pRSLT.Show(False)
        self.eValSpin.Show(False)
        self.panelSQ.SetSize((self.bPSize[0] - 20,70))
        self.textSQ.SetSize((self.bPSize[0] - 100, 50))
        self.panelR.SetSize((self.bPSize[0] - 20,
                            self.bPSize[1] - 200 - 35 * self.tbOnOff))
        self.pRSLT.SetSize((self.bPSize[0] + 19,
                            self.bPSize[1] - 240 - 35 * self.tbOnOff))
        self.lcRSLT.OnSize()
        self.lcRSLT.Clear()
        self.toolButton.SetPosition((300,25))
        self.stSpin.SetPosition((25,25))
        self.eValSpin.SetPosition((75,25))
        self.lcRSLT.Refresh(self.BlastRec)
        self.panelSQ.Show(True)
        self.panelR.Show(True)
        self.pRSLT.Show(True)
        self.eValSpin.Show(True)

    def SetQuery(self,qseq):
        # Method to load sequence from BioGUI
        for q in qseq:
            s = ">" + str(q[0].id) + "\n" + str(q[0].seq)+"\n"
            self.textSQ.write(s)

#--------------------------Menu Executables===-------------------
    def HelpDB(self,event):
        # Respond to a database selection
        self.dbsel = self.menuBar.GetLabel(event.GetId())
        self.dbaseMenu.Check(event.GetId(), True)
        
    def HelpExec(self,event):
        # Respond to a type selection
        self.name = self.menuBar.GetLabel(event.GetId())
        self.ccmd = self.plugins[self.name].Plugin().GetExec()
        self.typeMenu.Check(event.GetId(), True)
        
    def DoProtien (self, event):
        # Respond to the "Peptide" alphabet command.
        self.abet = "AA"
        self.alphaMenu.Check(event.GetId(), True)

    def DoDNA (self, event):
        # Respond to the "Nucleotide" alphabet command.
        self.abet = "DNA"
        self.alphaMenu.Check(event.GetId(), True)
        
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
        else:
            self.alphaMenu.Check(self.menu_DNA, True)
        
    def SetOptions(self, opts):
        # Respond to the options dialog closing
        self.options = opts        

    def DoOptions(self, event):
        # Respond to the "Options" menu command.
        self.optBox = bod.optDialog(self, 'Options Menu', self.typeMenu, -1)
        self.optBox.GetOpts(self.abet, self.name)
        self.optBox.ShowModal()
        
    def DoOpen(self, event):
        # Respond to the "Open" menu command.
        fileName = wx.FileSelector("Load File", default_extension=".fasta",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return
        fileName = os.path.join(os.getcwd(), fileName)
        self.textSQ.write(open(fileName).read())

    def DoNew(self, event):
        # Respond to the "New" menu command.
        newFrame = GuiFrame(self.parent, -1)
        newFrame.Show(True)

    def DoCreateDB(self, event):
        # Respond to the "New Database" menu command.
        bD = __import__("BlastDBCreateDiaolog")
        newDBDialog = bD.BlastDBCreateDiaolog(self,'Create a new database',-1)
        newDBDialog.getDB(self)
        newDBDialog.ShowModal()

    def SaveContents(self):
        # Save the contents of our document to disk.
        try:
            objData = []
            for obj in self.contents:
                objData.append([obj.__class__, obj.getData()])
            f = open(self.fileName, "wb")
            e = open("my_blast.xml")
            te = e.read()
            f.write(te)
            e.close()
            f.close()
        except:
            response = wx.MessageBox("Unable to save " + self.fileName + ".",
                                     "Error", wx.OK|wx.ICON_ERROR, self)

    def AskIfUserWantsToSave(self, action):
        # Give the user the opportunity to save the current document.
        response = wx.MessageBox("Save changes before " + action + "?",
                                "Confirm", wx.YES_NO | wx.CANCEL, self)
        if response == wx.YES:
            if self.fileName == None:
                fileName = wx.FileSelector("Save File As", "Saving",
                                      default_extension = ".xml",
                                      wildcard = "*.xml",
                                      flags = wx.SAVE | wx.OVERWRITE_PROMPT)
                if fileName == "": return False # User cancelled.
                self.fileName = fileName
            self.SaveContents()
            return True
        elif response == wx.NO:
            return True # User doesn't want changes saved.
        elif response == wx.CANCEL:
            return False # User cancelled.
        
    def GetExec(self, event):
        #Tool Executable
        self.lcRSLT.Clear()
        f = open(r".\Records\Blast Results\my_blast.xml", "w")
        f.write(str(self.textSQ.GetValue()))
        f.close()
        f = ".\Records\Blast Results\my_blast.xml"
        strA = self.ccmd+" -query my_seq.fasta -db "+self.dbsel+" -evalue "
        strB = " -outfmt 5 -out "+f+" -remote=True"
        aclu = strA + str(self.eValSpin.GetValue()) + strB
        p = subprocess.Popen(aclu)
        p.wait()
        self.BlastRec = list(NCBIXML.parse(open(f)))
        self.lcRSLT.Refresh(self.BlastRec)
                 
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

    #----------------------Menubar/Toolbar Initialization-----------------
    def GetIDs(self):
        # Create wx IDs for each menu item
        self.menu_OPTIONS      = wx.NewId()      # File menu items
        self.menu_TOOL         = wx.NewId()      # TOOL command
        self.menu_BLASTDB      = wx.NewId()      # New Database command
        self.menu_DNA          = wx.NewId()      # Alphabet menu options.
        self.menu_PROTIEN      = wx.NewId()                    
        for p in self.plugins:                   # Tools menu options.
            self.plugIds[p] = wx.NewId()                     
        for b in self.blastDbs.BDB().BlastDBS(): # Database menu options. 
            self.dbMenuIds[b] = wx.NewId() 
        self.menu_About     = wx.NewId()         # Help menu items.
        self.menu_ToolbarV  = wx.NewId()
        self.menu_ColOpts   = wx.NewId()

    def SetFileMenu(self):
        # Setup options in the file menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_NEW,             "New\tCtrl-N",
                             "Create a new window",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(self.menu_BLASTDB,     "New Db\tCtrl-N",
                             "Create a new Blast Database",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(wx.ID_OPEN,            "Load...",
                             "Load sequence(s)",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(self.menu_TOOL,        "BLAST",
                             "Run BLAST",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(self.menu_OPTIONS,     "Options...",
                             "Blast options...",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_SAVEAS,          "Save As...",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT,            "Quit\tCtrl-Q",
                             kind = wx.ITEM_NORMAL)
        self.menuBar.Append(self.fileMenu, "File")

    def SetAlphabetMenu(self):
        # Setup options in the alphabet menu
        self.alphaMenu = wx.Menu()
        self.alphaMenu.Append(self.menu_DNA,        "Nucleotide",
                              kind = wx.ITEM_RADIO)
        self.alphaMenu.Append(self.menu_PROTIEN,    "Peptide",
                              kind = wx.ITEM_RADIO)
        self.menuBar.Append(self.alphaMenu,"Alphabet")

    def SetTypeMenu(self):
        # Setup the Program type menu options
        self.typeMenu = wx.Menu()
        for name in self.plugins.keys():
            self.typeMenu.Append(self.plugIds[name],    name,
                                 kind = wx.ITEM_RADIO)
        self.menuBar.Append(self.typeMenu, "Type")

    def SetDatabaseMenu(self):
        # Setup the database menu options
        self.dbaseMenu = wx.Menu()
        for db in self.blastDbs.BDB().BlastDBS():
            self.dbaseMenu.Append(self.dbMenuIds[db], db, kind = wx.ITEM_RADIO)
        # Setup the database menu
        self.menuBar.Append(self.dbaseMenu, "Database")

    def SetHelpMenu(self):
        # Set up the options menu options
        self.helpMenu = wx.Menu()
        self.helpMenu.Append(self.menu_ToolbarV,    "Toolbar on/off",
                             kind = wx.ITEM_NORMAL)
        #self.helpMenu.Append(self.menu_ColOpts,     "Colors...",
                             #kind = wx.ITEM_NORMAL)
        self.helpMenu.Append(self.menu_About,       "About...",
                             kind = wx.ITEM_NORMAL)
        # Setup the option menu
        self.menuBar.Append(self.helpMenu, "Help")

    def DoMenubar(self):
        # Setup menu bar
        self.SetFileMenu()
        self.SetAlphabetMenu()
        self.SetTypeMenu()
        self.SetDatabaseMenu()
        self.SetHelpMenu()
        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (self.menu_TOOL,        self.GetExec),
            (wx.ID_NEW,             self.DoNew),
            (wx.ID_OPEN,            self.DoOpen),
            (wx.ID_EXIT,            self.DoExit),
            (wx.ID_SAVEAS,          self.DoSaveAs),
            (self.menu_OPTIONS,     self.DoOptions),
            (self.menu_BLASTDB,     self.DoCreateDB),
            (self.menu_DNA,         self.DoDNA),
            (self.menu_PROTIEN,     self.DoProtien),
            (self.menu_About,       self.DoAbout),
            (self.menu_ToolbarV,    self.DoTBOnOff),
            #s(self.menu_ColOpts,     self.DoColDlg),
            ]        
        for val in self.plugIds.values():       
            self.menuHandlers.append((val, self.HelpExec))
        for val in self.dbMenuIds.values():       
            self.menuHandlers.append((val, self.HelpDB))
        # Update Menu Bar with User Input
        for combo in self.menuHandlers:
            id, handler = combo[:2]
            self.Bind(wx.EVT_MENU, handler, id = id)
            if len(combo)>2:
                self.Bind(wx.EVT_UPDATE_UI, combo[2], id = id)
        self.SetMenuBar(self.menuBar)

    def DoToolbar(self):
        # Create the toolbar.
        # toolbar image size = (15,15) pixels
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL
                                          | wx.NO_BORDER | wx.TB_FLAT)
        self.toolbar.AddSimpleTool(
            wx.ID_NEW, wx.Bitmap(self.hD + r"\Utils\Icons\Blank.bmp",
                                wx.BITMAP_TYPE_BMP), "New")
        self.toolbar.AddSimpleTool(
            self.menu_BLASTDB, wx.Bitmap(self.hD + r"\Utils\Icons\Record.bmp",
                                wx.BITMAP_TYPE_BMP), "New Database")
        self.toolbar.AddSimpleTool(
            wx.ID_OPEN, wx.Bitmap(self.hD + r"\Utils\Icons\openFolder.bmp",
                                wx.BITMAP_TYPE_BMP), "Open")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.hD + r"\Utils\Icons\Disk.bmp",
                                wx.BITMAP_TYPE_BMP), "Save")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.hD + r"\Utils\Icons\diskCopied.bmp",
                                wx.BITMAP_TYPE_BMP), "Save As...")
        self.toolbar.AddSimpleTool(
            wx.ID_EXIT, wx.Bitmap(self.hD + r"\Utils\Icons\RedX.bmp",
                                wx.BITMAP_TYPE_BMP), "Exit")        
        self.toolbar.AddSeparator()
        for name in self.plugins.keys():
            BMP = self.plugins[name].GetBMP()
            self.toolbar.AddSimpleTool(self.plugIds[name],
                                       wx.Bitmap(BMP,wx.BITMAP_TYPE_BMP),name)
        # Cannot be changed through GUI
        self.toolbar.SetBackgroundColour('LIGHT GRAY')
        self.toolbar.Realize()

    #----------------------Frame Initialization-----------------
    def VarInit(self):
        # Initialize variables
        self.fileName = ""
        self.name = "BLASTN"
        self.abet = "DNA"
        self.dbsel = "nr"
        self.ccmd = "blastn"
        self.menuBar = wx.MenuBar()
        self.plugins = {}
        self.plugIds= {}
        self.dbMenuIds= {}
        self.bPSize = self.GetSize()
        self.tbOnOff = 1

    def GetPlugins(self):
        # Method to identify BLAST plugins
        dirt = self.hD+r"\plugins\tools\BLASTPlugins"
        self.plugins = gpi.GetPlugIns(dirt)
        # Obtain list of available databases
        self.blastDbs = __import__("BlastDataBases")

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def SetPanels(self):
        self.panelSQ = wx.Panel(self, -1, pos=(10,70),
                           size=(self.bPSize[0] - 20,70),
                           style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.panelR = wx.Panel(self, -1, pos = (10,150),
                             size=(self.bPSize[0] - 40,self.bPSize[1] - 225),
                             style=wx.BORDER_RAISED)
        self.panelR.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.pRSLT = wx.Panel(self.panelR, -1, pos = (75,25),
                             size=(self.bPSize[0] + 20, self.bPSize[1] - 240),
                             style=wx.BORDER_NONE)
        self.pRSLT.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        
    def SetViewWindows(self):
        # Create user interface appearance
        self.SetPanels()
        self.stSQ = wx.StaticText(self.panelSQ, -1,
                                  "Sequence(s): ", pos=(3,10))
        self.stSQ.SetForegroundColour(
            self.colorList['ToolInterface']['Fore'])
        self.textSQ = wx.TextCtrl(self.panelSQ, -1, "", pos=(75,8),
                         size=(self.bPSize[0] - 100, 50),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        wx.CallAfter(self.textSQ.SetInsertionPoint, 0)
        self.stRSLT = wx.StaticText(self.panelR, -1,
                                    "Results: ", pos=(25,10))
        self.stRSLT.SetForegroundColour(
            self.colorList['ToolInterface']['Fore'])
        self.lcRSLT = bv.Plugin()
        self.lcRSLT.Init(self.pRSLT, self.pRSLT, self.colorList)
        a = r"C:\Users\francis\Documents\Monguis\BioGui"
        b = r"\Records\Blast Results\my_blast1.xml"
        self.BlastRec = list(NCBIXML.parse(open(a+b)))
        self.lcRSLT.Refresh(self.BlastRec)
        self.lcRSLT.Clear()
        
    def SetButtons(self):
        # Create action button
        self.toolButton = wx.Button(self, -1, "BLAST!", pos=(300,25))
        self.toolButton.SetBackgroundColour(
            self.colorList['ToolButton']['Back'])
        self.toolButton.SetForegroundColour(
            self.colorList['ToolButton']['Fore'])
        self.Bind(wx.EVT_BUTTON, self.GetExec, self.toolButton)
        #Create User Modifiable search parameters.
        self.stSpin = wx.StaticText(self, -1, "E Value: ", pos=(25,25))
        self.eValSpin = wx.SpinCtrl(self, -1, size=(75, -1), pos=(75,62),
                                    name="EvalueSpinCTRL")
        self.eValSpin.SetValue(10)

    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title='Basic Local Alignment Search Tool Interface')
        #self.parent = parent
        if 'homeDir' in kwargs.keys():
            self.hD = kwargs['homeDir']
        else:
            self.hD = os.getcwd()
        self.VarInit()
        self.GetPlugins()
        self.GetIDs()
        self.GetColors()
        self.SetBackgroundColour(self.colorList['Tool']['Back'])
        self.DoMenubar()
        self.DoToolbar()
        self.SetViewWindows()
        self.SetButtons()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.DoExit)


def GetName():
    # Method to return name of tool
    return 'BLAST'

def GetBMP():
    # Method to return identifying image
    return r".\Utils\Icons\BLASTstar.bmp"

               
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





#   Lisa: My card here says "ACLU," 
#         Now look what I'm going to do.
#   (burns card)
#
#
#    From:   The Simpsons: Season 15, Episode 21
#            Bat-Mangled Banner (16 May 2004)
#            http://www.imdb.com/title/tt0763027/
