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
from xml.dom import minidom

class GuiFrame(wx.Frame):
    def GetName(self):
        # Method to return name of tool
        return 'GO GUI'

    def GetBMP(self):
        # Method to return identifying image
        return r".\Utils\Icons\GOAstoplight.bmp"

    def Clear(self):
        i = 0
        while i < len(self.windowBin):
            self.windowBin[i].Show(False)
            self.windowBin.pop(i)
                
    def OnSize(self, event):
        # Method to respond to window sizing
        self.bPSize = self.GetSize()
        self.panelSQ.Show(False)
        self.panelR.Show(False)
        self.panelSQ.SetPosition((10, 30))
        self.panelR.SetPosition((10, 135))
        self.panelR.SetSize((self.bPSize[0] - 20,
                            self.bPSize[1] - 185 - 35 * self.tbOnOff))
        self.panelSQ.SetSize((self.bPSize[0] - 20, 105))
        self.textSQ.SetSize((self.bPSize[0]/2. - 200, 88))
        self.textSQ.SetPosition((self.bPSize[0]/2. + 5, 6))
        self.textR.SetSize((self.bPSize[0] - 108,
                            self.bPSize[1] - 240 - 35 * self.tbOnOff))
        self.toolButton.SetPosition((self.bPSize[0] - 165, 6))
        self.typeCombo.SetPosition((75, 6))
        self.stType.SetPosition((18, 10))
        self.panelSQ.Show(True)
        self.panelR.Show(True)

    def SetQuery(self,qseq):
        'Only used for Search'
        self.SeqRecs = qseq

#--------------------------Menu Executables===-------------------
    def HelpExec(self,event):
        # Respond to a type selection
        self.Clear()
        name = self.typeMenu.GetLabel(event.GetId())
        self.typeCombo.SetValue(name)
        self.typeMenu.Check(self.plugIds[name], True)
        
    def HelpCombo(self,event):
        # Respond to a type selection
        self.Clear()
        name = self.typeCombo.GetValue()
        self.typeMenu.Check(self.plugIds[name], True)
        
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
        query = self.textSQ.GetValue()
        self.Clear()
        self.plugins[self.name].Plugin().GetExec(self,query)
                 
    def DoAbout(self,event):
        # Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription(
            "Interface to search GO\n"+
            "Capable of performing searches of the Gene Ontology Database\n\n" +
            "Intended for use with:\n" +
            "BioGui: Graphic User Interface for Biological Work\n" +
            "Developed by:\n" +
            "      The Ahmet Sacan Bioinformaticas Lab\n" +
            "\tSchool of Biomedical Engineering & Health Services\n" +
            "\tDrexel University, Philadelphia, Pennsylvania, 19104\n\n\n" +
            "Files are being checked for irrelevant variable names\n" +
            "If you find some, please keep comments to yourself\n\n" +
            "Copyright is waived until further notice. Nov. 6, 2013")
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
        self.menu_PROTIEN      = wx.NewId()                    
        for p in self.plugins:                   # Tools menu options.
            self.plugIds[p] = wx.NewId() 
        self.menu_About     = wx.NewId()         # Help menu items.
        self.menu_ToolbarV  = wx.NewId()
        self.menu_ColOpts   = wx.NewId()

    def SetFileMenu(self):
        # Setup options in the file menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_NEW,             "New\tCtrl-N",
                             "Create a new window",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(wx.ID_OPEN,            "Load...",
                             "Load sequence(s)",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(self.menu_TOOL,        "SEARCH",
                             "Perforn a SEARCH",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.Append(self.menu_OPTIONS,     "Options...",
                             "Search options...",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_SAVEAS,          "Save As...",
                             kind = wx.ITEM_NORMAL)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT,            "Quit\tCtrl-Q",
                             kind = wx.ITEM_NORMAL)
        self.menuBar.Append(self.fileMenu, "File")

    def SetTypeMenu(self):
        # Setup the Program type menu options
        self.typeMenu = wx.Menu()
        for name in self.plugins.keys():
            self.typeMenu.Append(self.plugIds[name],    name,
                                 kind = wx.ITEM_RADIO)
        self.menuBar.Append(self.typeMenu, "Type")

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
        self.SetTypeMenu()
        self.SetHelpMenu()
        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (self.menu_TOOL,        self.GetExec),
            (wx.ID_NEW,             self.DoNew),
            (wx.ID_OPEN,            self.DoOpen),
            (wx.ID_EXIT,            self.DoExit),
            (wx.ID_SAVEAS,          self.DoSaveAs),
            (self.menu_OPTIONS,     self.DoOptions),
            (self.menu_About,       self.DoAbout),
            (self.menu_ToolbarV,    self.DoTBOnOff),
            #s(self.menu_ColOpts,     self.DoColDlg),
            ]        
        for val in self.plugIds.values():       
            self.menuHandlers.append((val, self.HelpExec))
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
        self.name = "Search"
        self.ccmd = "Search"
        self.menuBar = wx.MenuBar()
        self.plugins = {}
        self.plugIds= {}
        self.bPSize = self.GetSize()
        self.tbOnOff = 1

    def GetPlugins(self):
        # Method to identify BLAST plugins
        dirt = self.hD+r"\plugins\tools\GOPlugins"
        self.plugins = gpi.GetPlugIns(dirt)

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def SetPanels(self):
        self.panelSQ = wx.Panel(self, -1, pos = (10,30),
                           size = (self.bPSize[0] - 20,105),
                           style = wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.panelR = wx.Panel(self, -1, pos = (10,135),
                             size=(self.bPSize[0] - 20,self.bPSize[1] - 185),
                             style=wx.BORDER_RAISED)
        self.panelR.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        
    def SetViewWindows(self):
        # Create user interface appearance
        self.SetPanels()
        self.stSQ = wx.StaticText(self.panelSQ, -1,
                                  "Query: ", pos=(self.bPSize[0]/2. - 40,10))
        self.stSQ.SetForegroundColour(
            self.colorList['ToolInterface']['Fore'])
        self.textSQ = wx.TextCtrl(self.panelSQ, -1, "",
                         pos = (self.bPSize[0]/2. + 5, 6),
                         size = (self.bPSize[0]/2. - 200, 88),
                         style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        wx.CallAfter(self.textSQ.SetInsertionPoint, 0)
        self.stRSLT = wx.StaticText(self.panelR, -1,
                                    "Results: ", pos=(25,10))
        self.stRSLT.SetForegroundColour(
            self.colorList['ToolInterface']['Fore'])
        self.textR = wx.TextCtrl(self.panelR, -1, "", pos = (75, 10),
                         size = (self.bPSize[0] - 108, self.bPSize[1] - 240),
                         style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        wx.CallAfter(self.textSQ.SetInsertionPoint, 0)
        #Create holder for tool specific windows
        self.windowBin = []
        
    def SetButtons(self):
        # Create action button
        self.toolButton = wx.Button(self.panelSQ, -1, "GO!", size=(75,25),
                                    pos=(self.bPSize[0] - 165, 6))
        self.toolButton.SetBackgroundColour(
            self.colorList['ToolButton']['Back'])
        self.toolButton.SetForegroundColour(
            self.colorList['ToolButton']['Fore'])
        self.Bind(wx.EVT_BUTTON, self.GetExec, self.toolButton)
        self.stType = wx.StaticText(self.panelSQ, -1, "Modality: ", pos=(18,10))
        self.stType.SetForegroundColour(
            self.colorList['ToolInterface']['Fore'])
        choices = self.plugins.keys()
        self.typeCombo = wx.ComboBox(self.panelSQ, -1, pos = (75,6),
                                     choices = choices, style = wx.CB_READONLY)
        self.typeCombo.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.HelpCombo, self.typeCombo)

    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title='Gene Ontology GUI')
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
    '''
    Method to return name of tool
    '''
    return 'GO GUI'

def GetBMP():
    '''
    Method to return identifying image
    '''
    return r".\Utils\Icons\GOAstoplight.bmp"        

"""
#----------------------------------------------------------------------------   

#Code to start gui
class MyApp(wx.App):
    def OnInit(self):
        frame = GuiFrame(None,-1,r'C:\Users\francis\Documents\Monguis\BioGui',[['#FBFFCF','BLACK'],                              #Main Frame Background
              ['RED','WHITE'],                                  #Tool Button Background,Foreground
              ['WHITE','BLACK'],                                #Directory Control Tree Background,Foreground
              ['WHITE','BLACK'],                                #View Panel Background,Foreground
              ['NAVY','WHITE'],                                 #View Button Background,Foreground
              ['WHITE','BLACK'],                                #List View Background,Foreground
              ['RED','WHITE'],                                  #View Panel Button Background,Foreground
              ['WHITE','BLACK'],                                #View Panel List Control Background,Foreground
              ['LIGHT GRAY','BLACK'],                           #View Panel 'Gray' Frame Background,Foreground
              ['#FBFFCF','BLACK'],                              #Tool Frame Background
              [(83, 114, 140, 255),(255, 255, 255, 255)],       #Tool Interface Panel Background,Foreground
              
              ])
        self.SetTopWindow(frame)
        frame.Show(True)
        return True  

global app        
app = MyApp(redirect=True)
app.MainLoop()"""

                

         
