import wx

class MenuToolBarSetup():
    def GetIDs(self):
        # Create wx IDs for each menu item
        self.plugIds = {}
        self.menu_OPTIONS        = wx.NewId()     # File menu items
        self.menu_TOOL           = wx.NewId()     # ALIGN command
        self.menu_DNA            = wx.NewId()     # Alphabet menu options.
        self.menu_RNA            = wx.NewId()
        self.menu_PROTIEN        = wx.NewId()
        for p in self.plugins:                    # Tools menu options.
            self.plugIds[p]      = wx.NewId()   
        self.menu_About          = wx.NewId()     # Help menu items.
        self.menu_ToolbarV       = wx.NewId()
        self.menu_ColOpts        = wx.NewId()
        return self.plugIds

    def SetFileMenu(self, header, headerStr, optY):
        # Setup options in the file menu
        self.p.fileMenu = wx.Menu()
        self.p.fileMenu.Append(wx.ID_NEW,             "New\tCtrl-N",
                             "Create a new window",
                             kind = wx.ITEM_NORMAL)
        self.p.fileMenu.Append(wx.ID_OPEN,            "Load...",
                             "Load sequence(s)",
                             kind = wx.ITEM_NORMAL)
        if not header == '':
            self.p.fileMenu.Append(self.menu_TOOL,        header,
                                 headerStr,
                                 kind = wx.ITEM_NORMAL)
        if optY:
            self.p.fileMenu.Append(self.menu_OPTIONS,     "Options...",
                                 "Blast options...",
                                 kind = wx.ITEM_NORMAL)
        self.p.fileMenu.AppendSeparator()
        self.p.fileMenu.Append(wx.ID_SAVEAS,          "Save As...",
                             kind = wx.ITEM_NORMAL)
        self.p.fileMenu.AppendSeparator()
        self.p.fileMenu.Append(wx.ID_EXIT,            "Quit\tCtrl-Q",
                             kind = wx.ITEM_NORMAL)
        self.p.menuBar.Append(self.p.fileMenu,   "File")

    def SetAlphabetMenu(self, rnaY):
        # Setup options in the alphabet menu
        self.p.alphaMenu = wx.Menu()
        self.p.alphaMenu.Append(self.menu_DNA,        "DNA",
                              kind = wx.ITEM_RADIO)
        if rnaY:
            self.p.alphaMenu.Append(self.menu_RNA,    "RNA",
                              kind = wx.ITEM_RADIO)
        self.p.alphaMenu.Append(self.menu_PROTIEN,    "Peptide",
                              kind = wx.ITEM_RADIO)
        self.p.menuBar.Append(self.p.alphaMenu,  "Alphabet")

    def SetTypeMenu(self):
        # Setup the Program type menu options
        self.p.typeMenu = wx.Menu()
        for name in self.plugins.keys():
            self.p.typeMenu.Append(self.plugIds[name],name,
                                 kind = wx.ITEM_RADIO)
        self.p.menuBar.Append(self.p.typeMenu,   "Type")

    def SetHelpMenu(self, colY):
        # Set up the options menu options
        self.p.helpMenu = wx.Menu()
        self.p.helpMenu.Append(self.menu_ToolbarV,    "Toolbar on/off",
                             kind = wx.ITEM_NORMAL)
        if colY:
            self.p.helpMenu.Append(self.menu_ColOpts,     "Colors...",
                                   kind = wx.ITEM_NORMAL)
        self.p.helpMenu.Append(self.menu_About,       "About...",
                             kind = wx.ITEM_NORMAL)
        # Setup the option menu
        self.p.menuBar.Append(self.p.helpMenu,   "Help")

    def DoMenubar(self, header, headerStr, abetY, rnaY, optY, colY):
        # Setup menu bar
        self.SetFileMenu(header, headerStr, optY)
        if abetY:
            self.SetAlphabetMenu(rnaY)
        self.SetTypeMenu()
        self.SetHelpMenu(colY)
        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (wx.ID_NEW,             self.p.DoNew),
            (wx.ID_OPEN,            self.p.DoOpen),
            (wx.ID_EXIT,            self.p.DoExit),
            (wx.ID_SAVEAS,          self.p.DoSaveAs),
            (self.menu_About,       self.p.DoAbout),
            (self.menu_ToolbarV,    self.p.DoTBOnOff),
            ]
        if not header == '':
            self.menuHandlers.append((self.menu_TOOL, self.p.GetExec))
        if abetY:
            self.menuHandlers.append((self.menu_DNA, self.p.DoDNA))
            self.menuHandlers.append((self.menu_PROTIEN, self.p.DoProtien))
            if rnaY:
                self.menuHandlers.append((self.menu_RNA, self.p.DoRNA))
        if optY:
            self.menuHandlers.append((self.menu_OPTIONS, self.p.DoOptions))
        if colY:
            self.menuHandlers.append((self.menu_ColOpts, self.p.DoColDlg))
        for val in self.plugIds.values():       
            self.menuHandlers.append((val, self.p.HelpExec))
        # Update Menu Bar with User Input
        for combo in self.menuHandlers:
            id, handler = combo[:2]
            self.p.Bind(wx.EVT_MENU, handler, id = id)
            if len(combo)>2:
                self.p.Bind(wx.EVT_UPDATE_UI, combo[2], id = id)
        self.p.SetMenuBar(self.p.menuBar)

    def DoToolbar(self):
        # Create a toolbar.
        # toolbar image size = (15,15) pixels
        self.p.toolbar = self.p.CreateToolBar(wx.TB_HORIZONTAL
                                          | wx.NO_BORDER | wx.TB_FLAT)
        self.p.toolbar.AddSimpleTool(
            wx.ID_NEW, wx.Bitmap(self.hD + r"\Utils\Icons\Blank.bmp",
                                wx.BITMAP_TYPE_BMP), "New")
        self.p.toolbar.AddSimpleTool(
            wx.ID_OPEN, wx.Bitmap(self.hD + r"\Utils\Icons\openFolder.bmp",
                                wx.BITMAP_TYPE_BMP), "Open")
        self.p.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.hD + r"\Utils\Icons\Disk.bmp",
                                wx.BITMAP_TYPE_BMP), "Save As...")
        self.p.toolbar.AddSimpleTool(
            wx.ID_EXIT, wx.Bitmap(self.hD + r"\Utils\Icons\RedX.bmp",
                                wx.BITMAP_TYPE_BMP), "Exit")        
        self.p.toolbar.AddSeparator()
        for name in self.plugIds.keys():
            self.p.toolbar.AddSimpleTool(self.plugIds[name],
                      wx.Bitmap(self.plugins[name].GetBMP(),
                                wx.BITMAP_TYPE_BMP), name)
        # Cannot be changed through GUI
        self.p.toolbar.SetBackgroundColour('LIGHT GRAY')
        self.p.toolbar.Realize()
        
    def __init__(self, parent, plugins, hD):
        self.p = parent
        self.plugins = plugins
        self.hD = hD
