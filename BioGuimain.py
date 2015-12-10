import wx
import os
import sys
sys.path.append(r".\Utils")
sys.path.append(r".\Plugins\Lists")
import ListView as lv
import getPlugins as gpi
import MenuToolBarSetup as mtbs

class GuiFrame(wx.Frame):
    """ A frame showing the central frame of a BioGui program with directory,
        folders, and viewing plugin panels."""
    #--------------------------File Menu Executables---------------------
    """def DoSave(self):
        # Save the contents of our document to disk.
        # Really? What are we saving?
        # Curent View?
        try:
            objData = []
            for obj in self.contents:
                objData.append([obj.__class__, obj.getData()])
            #f = open(self.fileName, "wb")
            #Have not imported CPickle
            #cPickle.dump(objData, f)
            #f.close()
            #self._adjustMenus()
        except:
            response = wx.MessageBox("Unable to load " + self.fileName + ".",
                                     "Error", wx.OK|wx.ICON_ERROR, self)"""

    def AskIfUserWantsToQuit(self, event):
        # Prompt in case unintentional exit
        response = wx.MessageBox("Are you sure you want to quit?",
                                 "Confirm", wx.YES_NO , self)
        if response == wx.YES:
            return True
        elif response == wx.NO:
            return False 
        
    #Please see above
    def DoSaveAs(self, event):
        # Respond to the "Save As" menu command.
        if self.fileName == None:
            default = ""
        else:
            default = self.fileName
        curDir = os.getcwd()
        fileName = wx.FileSelector("Save File As", "Saving",
                                   default_filename=default,
                                   default_extension="psk",
                                   wildcard="*.psk",
                                   flags = wx.SAVE | wx.OVERWRITE_PROMPT)
        if fileName == "": return # User cancelled.
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)
        title = os.path.basename(fileName)
        self.SetTitle(title)
        self.fileName = fileName
        self.SaveContents()

    def DoExit(self, event):
        # Respond to the "Quit" menu command or closing of the window.
        if self.AskIfUserWantsToQuit(wx.EVT_IDLE):
            self.Show(False)
            self.tree.Destroy()
            self.dirCtrl.Destroy()
            self.horz.Destroy()
            self.vert.Destroy()
            self.Destroy()
            #return "True"
        
    #Much more work is needed here
    def DoOpen(self, event):
        # Respond to the "Load" menu command.
        curDir = os.getcwd()
        fileName = wx.FileSelector("Load File", default_extension=".fasta",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)
        fasta_string = open(fileName).read()
        self.text1.write(fasta_string)

    def DoNew(self, event):
        # Respond to the "New" menu command.
        import NewRecord as nr
        rec = nr.newRecord(self, 'Options Menu', -1)
        rec.DisplayPrompt()
        rec.ShowModal()
        rec.Destroy()
        
    #--------------------------Help Menu Executables---------------------
    def DoAbout(self,event):
        # Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription(
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
        # Respond to the "Toolbar On/Off" menu command
        self.tbOnOff = abs(self.tbOnOff - 1)
        if self.tbOnOff:
            self.toolbar.Show(True)
        else:
            self.toolbar.Show(False)
        self.OnSize(wx.EVT_IDLE)

    def DoColDlg(self,event):
        # Open color dialog window
        import changeColorDialog as ccd
        dlg = ccd.changeColorDialog(self, self.colorList, self.hD)
        dlg.ShowModal()

    #-----------Tool Menu/toolbar/button Executables---------------
    def DoViewPlugin(self, event):
        # Update current view to respond to user selection
        os.chdir(self.hD)
        self.curView.Clear()
        buttonLabel = event.GetEventObject().GetLabel()
        if not buttonLabel == self.curView.GetName():
            self.curView = self.views[buttonLabel].Plugin()
        record = self.listView.GetRec()
        self.curView.Init(self, self.bottom, self.colorList)
        os.chdir(self.dirCtrl.GetPath())
        self.curView.GetExec(record)
        os.chdir(self.hD)
        
    def HelpExec(self,event):
        # Execute button click for a tools menu selection
        name = self.menuBar.GetLabel(event.GetId())
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                self.buttonList[name].GetId())
        event.SetEventObject(self.buttonList[name])
        self.buttonList[name].Command(event)
        
    def GetExec(self,event):
        # Respond to a tool button click by opening tool gui
        buttonLabel = event.GetEventObject().GetLabelText()
        frame = self.tools[buttonLabel].GuiFrame(self, homeDir = self.hD)
        sentList = self.listView.GetRec()
        if sentList[0] > 0:
            frame.SetQuery(sentList)
        frame.Show(True)

    """Not complete
    def DoAddTool(self, event):
        #Respond to a new tool button click
        sys.path.append(self.hD + r"\Utils")
        import addToolDialog as aTD
        godia = aTD.addToolDialog(self, 'New Tool Menu', self.hD, -1)
        godia.Show(True)"""

    #--------------------------Initializations Functions---------------------
    def VarInit(self):
        # Class variables and lists
        self.fSize        = self.GetSize()
        self.hD           = os.getcwd()
        self.menuBar      = wx.MenuBar()
        self.fileMenu     = wx.Menu()
        self.toolMenu     = wx.Menu()        
        self.helpMenu     = wx.Menu()
        self.tbOnOff      = 1
        self.buttonList   = {}
        self.viewButtons  = {}
        self.viewTypes    = {}
        self.rec          = ''
        self.listView     = ''
        self.curView      = ''

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def SetButtons(self):
        # Create user interface buttons for available tools
        yPos=25
        for name in self.tools.keys():
            self.buttonList[name] = wx.Button(self, -1, str(name),
                                              pos=(self.fSize[0] - 100, yPos))
            self.buttonList[name].SetBackgroundColour(
                self.colorList['ToolButton']['Back'])
            self.buttonList[name].SetForegroundColour(
                self.colorList['ToolButton']['Fore'])
            yPos += (self.fSize[1] - 100) / (len(self.tools.keys()) + 1)
            self.Bind(wx.EVT_BUTTON, self.GetExec, self.buttonList[name])

    def SetViewWindows(self):
        # Create windows for Main Panels 
        self.vert = wx.SplitterWindow(self, -1, pos = (0,0),
            size = (self.fSize[0] * 1000/1125,self.fSize[1] * 500/600),
            style = wx.SP_NO_XP_THEME)
        self.horz = wx.SplitterWindow(self.vert, -1,
            size = (self.fSize[0] * 1000/1125,self.fSize[1] * 500/600),
            style = wx.SP_NO_XP_THEME)        
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.SashMoved, self.vert)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.SashMoved, self.horz)
        self.dirCtrl = wx.GenericDirCtrl(self.vert, -1,
                                         style = wx.DIRCTRL_DIR_ONLY)
        self.dirCtrl.SetPath(self.hD + r"\Records\Amino Acids")

    def SetMainPanels(self):
        # Create Viewing Panels 
        self.top = wx.Panel(self.horz, -1, style = wx.SUNKEN_BORDER,
                            size = (self.fSize[0] - 150,
                                    self.vert.GetSize()[1] / 2.))
        self.bottom = wx.Panel(self.horz, -1, style = wx.SUNKEN_BORDER,
                            size = (self.fSize[0] - 150,
                                    self.vert.GetSize()[1] / 2.))
        self.bottom.SetBackgroundColour(self.colorList['ViewPanel']['Back'])
        self.horz.SplitHorizontally(self.top, self.bottom)
        self.horz.SetSashPosition(
            self.vert.GetSize()[1] / 2., redraw=True)
        # Create Directory tree
        self.tree = self.dirCtrl.GetTreeCtrl()
        self.tree.style = wx.TR_HAS_BUTTONS
        self.tree.SetBackgroundColour(self.colorList['DirCtrl']['Back'])
        self.tree.SetForegroundColour(self.colorList['DirCtrl']['Fore'])
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)
        self.vert.SplitVertically(self.dirCtrl, self.horz)
        self.vert.SetSashPosition(self.fSize[0] * 250 / 1125, redraw=True)

    def SetViewTypes(self):
        # Dictionary of view types available for record types
        #NTS: make sure is auto updated on pre-load
        self.viewTypes = {
            "Alignments":         ["AlignView"],
            "Amino Acids":        ["AAView","DotPlotView","NAView",
                                   "AlignView"],
            "Blast Results":      ["BLASTView"],
            "Chromosomes":        ["GenomeView"],
            "Gene Expressions":   ["GEView"],
            "Images":             ["ImageView"],
            "Nucleic Acids":      ["NAView","DotPlotView","AAView",
                                   "AlignView"],
            "PDB":                ["PDBView"],
            "Phylogenetic Trees": ["PhyloTreeView"],
            "SSE":                ["SSEView"],
            "Unknown":            ["UnknownView"],
            }
    
    #--------------------------Window Management---------------------
    def OnSize(self, event):
        # Method to respond to sizing of window
        self.size = self.GetSize()
        self.vert.SetSize((self.size[0] - 125, self.size[1] - 100))
        self.horz.SetSize((self.size[0] - 125, self.size[1] - 100))
        yPos = 25
        for val in self.buttonList.values():
            val.SetPosition((self.size[0] - 100, yPos))
            yPos += (self.size[1] - 100) / (len(self.tools) + 1)
        self.SashMoved(event)

    def SashMoved(self, event):
        # Method to respond to sash movement
        self.top.SetSize(
            (self.vert.GetSize()[0] - self.vert.GetSashPosition(),
             self.horz.GetSashPosition()))
        self.bottom.SetSize(
            (self.vert.GetSize()[0] - self.vert.GetSashPosition(),
             self.vert.GetSize()[1] - self.horz.GetSashPosition()))
        self.curView.OnSize()
        self.listView.OnSize()
        self.MoveViewButtons()

    def MoveViewButtons(self):
        # Method to relocate view buttons when needed
        yPos = 2
        for val in self.viewButtons.values():
            val.SetPosition((self.bottom.GetSize()[0]-107, yPos))
            yPos += 27

    def OnSelect(self, event):
        # Method to respond to tree selection. match views to folder options
        os.chdir(self.hD)
        try:
            f = open(self.dirCtrl.GetPath() + r'\folderText.txt','r')
            ftype = f.readline()
        except:
            ftype = "Unknown"
        self.curView.Clear()
        self.curView = self.views[self.viewTypes[ftype][0]].Plugin()
        self.curView.Init(self, self.bottom, self.colorList)
        self.listView.Clear()
        self.listView.GetExec(ftype, self.dirCtrl.GetPath())
        self.MakeViewButtons(ftype)

    def MakeViewButtons(self, ftype):
        # Create buttons for available views
        yPos = 2
        for v in self.viewButtons.values():
            v.Show(False)
        self.viewButtons = {}
        for view in self.viewTypes[ftype]:
            self.viewButtons[view] = wx.Button(self.bottom, -1, str(view),
                                        style = wx.NO_BORDER, pos = (0, yPos),
                                        size = (100 , 22))
            self.viewButtons[view].SetBackgroundColour(
                self.colorList['ViewButton']['Back'])
            self.viewButtons[view].SetForegroundColour(
                self.colorList['ViewButton']['Fore'])
            yPos += 27
            self.Bind(wx.EVT_BUTTON, self.DoViewPlugin, self.viewButtons[view])
        self.SashMoved(wx.EVT_IDLE)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                            self.viewButtons[self.viewTypes[ftype][0]].GetId())
        event.SetEventObject(self.viewButtons[self.viewTypes[ftype][0]])
        self.viewButtons[self.viewTypes[ftype][0]].Command(event)
                    
    def Refresh(self, record):
        # Update current view to respond to plugin action
        self.curView.Refresh(record)
        os.chdir(self.hD)

    #--------------------------Initialzation Method---------------------
    def __init__(self, parent, title, fileName = None):
        # Initialize frame
        wx.Frame.__init__(self, parent,
                          title = 'complex BIO gui in development',
                          size = (1125, 600))
        self.VarInit()
        self.tools = gpi.GetPlugIns(self.hD + r"\Plugins\Tools")
        self.views = gpi.GetPlugIns(self.hD + r"\Plugins\Views")
        self.GetColors()
        self.SetBackgroundColour(self.colorList['Main']['Back'])
        mts = mtbs.MenuToolBarSetup(self, self.tools, self.hD)
        self.toolIDs = mts.GetIDs()
        mts.DoMenubar("","",False,False,False,True)
        mts.DoToolbar()
        self.SetButtons()
        self.SetViewWindows()
        self.SetMainPanels()
        self.SetViewTypes()
        self.listView = lv.ListView()
        self.listView.Init(self, self.top, self.hD, self.colorList)
        self.curView = self.views[self.viewTypes['Amino Acids'][0]].Plugin()
        self.curView.Init(self, self.bottom, self.colorList)
        self.OnSelect(wx.EVT_IDLE)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.DoExit) # Prompt user before closing frame
        """Leave untouched until ready
        self.addToolButton = wx.Button(self, -1, "ADDTOOL", pos=(self.fSize[0] * 1025 / 1125,yPos))
        self.addToolButton.SetBackgroundColour(self.colorList[1][0])
        self.addToolButton.SetForegroundColour(self.colorList[1][1])
        self.Bind(wx.EVT_BUTTON, self.DoAddTool, self.addToolButton)"""

#------------------------Code for Splash Scrren-------------------------
class MySplashScreen(wx.SplashScreen):
    def __init__(self, parent = None):
        # Initialize a splash screen to display BioGui startup image
        bitmap = wx.Bitmap(r".\Utils\Icons\BguiPoss.bmp")
        wx.SplashScreen.__init__(
            self, bitmap, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
            1500, None, size = (350, 187))
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()

    def OnExit(self, evt):
        # MyFrame is the main frame.
        self.Hide()
        self.Destroy()
        MyFrame = GuiFrame(None, -1, "")
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        evt.Skip()

#---------------------------Code to start gui-----------------------
class MyApp(wx.App):
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()
        return True

global app        
app = MyApp(redirect = True)
app.MainLoop()






# 'And remember: MUD spelled backwards is DUM!'
#   - B. Bunny
# "Operation: Rabbit". IMDb.
#      http://www.imdb.com/title/tt0045000
