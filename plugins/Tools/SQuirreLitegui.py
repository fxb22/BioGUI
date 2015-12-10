import sys
'''Test to rread'''
import wx
import os
from wx.lib.buttons import GenBitmapButton,GenBitmapToggleButton
import wx.lib.mixins.listctrl as listmix
import traceback
import types
import subprocess
import sqlite3


class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, ID, style, size, colNum, pos=(0,0)):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, colNum)

    def GetListCtrl(self):
        return self

    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        
        # redraw the list
        self.Refresh()


        

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s




#----------------------------------------------------------------------------
#                            System Constants                                
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------

class GuiFrame(wx.Frame):
    """ A frame showing the contents of a single document. """
    

    # ==========================================
    # ===== Methods for Plug-in Management =====
    # ==========================================

    def GetName(self):
        '''
        Method to return name of tool
    '''
        return 'SQuirreL'

    def GetBMP(self):
        return r".\Utils\Icons\SQuirreL.bmp"

    def GetPlugIns(self):
        '''
        Method to identify Blast plug-ins 
        '''
        self.PIlist = os.listdir(self.hD + r"\plugins\tools\SQuirreLPlugins")
        sys.path.append(self.hD + r"\plugins\tools\SQuirreLPlugins")
        self.toolPlugins=[]
        for filePI in self.PIlist:
            (self.PIname, self.PIext) = os.path.splitext(filePI)
            if self.PIext == '.py':
                self.toolPlugins.append(__import__(str(self.PIname)))
        self.PIlist = os.listdir(self.hD + r"\plugins")
        sys.path.append(self.hD + r"\plugins")
                
    def SetQuery(self,qseq):
        2+2
        

    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================

    def __init__(self, parent, *args, **kwargs):
        """
        Standard constructor.
        'parent', 'id' and 'title' are all passed to the standard wx.Frame
        constructor.  'fileName' is the name and path of a saved file to
        load into this frame, if any.
        """
        wx.Frame.__init__(self, parent, title='SQuirreL: a GUI for visualizing SQLite Databases', size=(1000, 595))
        if 'homeDir' in kwargs.keys():
            self.hD = kwargs['homeDir']
        else:
            import os
            self.hD = os.getcwd()
        self.SetBackgroundColour('#FBFFCF')
        #wx.Colour(247,199,147))
        self.GetPlugIns()

        # Menu item IDs:
        
        menu_OPTIONS      = wx.NewId()     # File menu items
        menu_SEARCH       = wx.NewId()     # SEARCH command
        
        self.toolGoMenu=[]                 # Tools menu options.
        for dummy in self.toolPlugins:     # Iterate through all available tools
            self.toolGoMenu.append(wx.NewId())

        #menu_ABOUT        = wx.NewId()                 # Help menu items.
        
        # Setup our menu bar.
        self.menuBar = wx.MenuBar()

        #Setup options for the file menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_NEW,    "New\tCtrl-N",    "Create a new Database")
        self.fileMenu.Append(wx.ID_OPEN,   "Load...",        "Load an existing Database")
        self.fileMenu.Append(menu_SEARCH,  "Search",         "Perform a Database search")
        self.fileMenu.Append(menu_OPTIONS, "Options...",     "Options...")
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_SAVEAS, "Save As...")
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT,   "Quit\tCtrl-Q")
        #Setup the file menu
        self.menuBar.Append(self.fileMenu, "File")

        #Set up the options menu options
        #self.helpMenu = wx.Menu()
        #self.helpMenu.Append(menu_CONFIGURE,  "Configure...")
        #self.helpMenu.Append(menu_ABOUT,      "About...")
        #Setup the option menu
        #self.menuBar.Append(self.helpMenu,         "Help")

        # Create our toolbar.

        tsize = (15,15)
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

        self.toolbar.AddSimpleTool(
            wx.ID_NEW, wx.Bitmap(self.hD + r"\Utils\Icons\Blank.bmp", wx.BITMAP_TYPE_BMP), "New")
        self.toolbar.AddSimpleTool(
            wx.ID_OPEN, wx.Bitmap(self.hD + r"\Utils\Icons\openFolder.bmp", wx.BITMAP_TYPE_BMP), "Open")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.hD + r"\Utils\Icons\Disk.bmp", wx.BITMAP_TYPE_BMP), "Save")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.hD + r"\Utils\Icons\diskCopied.bmp", wx.BITMAP_TYPE_BMP), "Save As...")
        self.toolbar.AddSimpleTool(
            wx.ID_EXIT, wx.Bitmap(self.hD + r"\Utils\Icons\RedX.bmp", wx.BITMAP_TYPE_BMP), "Exit")
        

        self.toolbar.AddSeparator()

        self.toolbar.SetBackgroundColour('LIGHT GRAY')
        self.toolbar.Realize()
        
        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (menu_SEARCH,      self.toolEXE),
            (wx.ID_NEW,        self.doNew),
            (wx.ID_OPEN,       self.doOpen),
            (wx.ID_EXIT,       self.doExit),
            (wx.ID_SAVEAS,     self.doSaveAs),
            (menu_OPTIONS,     self.doOptions),
            ]
        tempIdNum = len(self.menuHandlers)
        
        for itnum,tool in enumerate(self.toolPlugins):       
            self.menuHandlers.append((self.toolGoMenu[itnum],     self.helpEXE))

        #self.lowID,dummy = self.menuHandlers[tempIdNum]

        #Update Menu Bar with User Input
        for combo in self.menuHandlers:
            id, handler = combo[:2]
            self.Bind(wx.EVT_MENU, handler, id = id)
            if len(combo)>2:
                self.Bind(wx.EVT_UPDATE_UI, combo[2], id = id)
        #Set the menu bar
        self.SetMenuBar(self.menuBar)

        # Install our own method to handle closing the window.  This allows us
        # to ask the user if he/she wants to save before closing the window.

        #self.Bind(wx.EVT_CLOSE, self.doExit(wx.EVT_IDLE))

        #Create user interface appearance       
        self.panelSQ = wx.Panel(self, -1, pos=(7,7), size=(150,500), style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour('#53728c')

        self.panelRSLT = wx.Panel(self, -1, pos=(175,7), size=(776,500), style=wx.BORDER_RAISED)
        self.panelRSLT.SetBackgroundColour('#53728c')

        
        #Create user interface text boxes
        #Create sequence input box and label. Allow input to be modified.
        #self.l1 = wx.StaticText(self.panelSQ, -1, "Table(s)", pos=(55,3))
        #self.l1.SetForegroundColour('WHITE')
        self.text1 = wx.TreeCtrl(self.panelSQ, -1, pos=(5,5), size=(133, 483), style=wx.TR_HAS_BUTTONS|wx.TR_SINGLE )
        self.root = self.text1.AddRoot('Table(s)')
        self.text1.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.treeRC)

        self.tree_menu_titles = ["Expand",
                            "Collapse",
                            "Rename",
                            "Delete" ]

        self.tree_menu_title_by_id = {}
        for title in self.tree_menu_titles:
            self.tree_menu_title_by_id[ wx.NewId() ] = title

        self.root_menu_titles = ["Expand",
                            "Collapse",
                            "Add table"]

        self.root_menu_title_by_id = {}
        for title in self.root_menu_titles:
            self.root_menu_title_by_id[ wx.NewId() ] = title

            
        
    


        #Create results outbox and label. The box is able to be modified.
        self.l2 = wx.StaticText(self.panelRSLT, -1, "Database:", pos=(5,5))
        self.l2.SetForegroundColour('WHITE')
        self.text2 = wx.TextCtrl(self.panelRSLT, -1, "", size=(705, 40), pos=(55,5))
        wx.CallAfter(self.text2.SetInsertionPoint, 0)
        
        #Create BLAST action button
        self.colNum = 1
        self.dbList = TestListCtrl(self.panelRSLT, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL, size = (750,428), colNum = self.colNum, pos=(10,60))
        #self.listRefill()
        #self.dbList.SetBackgroundColour(colorList[7][0])
        #self.dbList.SetForegroundColour(colorList[7][1])
        #Create User Modifiable search parameters.
        
        


        #Set initial conditions
        self.fileName=""
        self.blasttype = "blastn"
        #Initialize parameters
        self.abet = "DNA"
        self.dbsel="nr"
        self.ccmd="blastn"
        
        
        
        #self.optBox=optDialog(self, 'Options Menu', self.typeMenu, -1)


    # ============================
    # = ListBox Handling Methods =
    # ============================

    def treeRC(self, event):
        self.selectedTable = self.text1.GetItemText(event.GetItem())
        menu = wx.Menu()
        if self.selectedTable == 'Table(s)':
            print 'horaay'
            for (mid,title) in self.root_menu_title_by_id.items():
                mmi = wx.MenuItem(menu, wx.NewId(), str(title))
                menu.AppendItem(mmi)

                menu.Bind(wx.EVT_MENU, self.RootSelectionCb, mmi )
        #else:
         #   for (mid,title) in self.tree_menu_title_by_id.items():
          #      menu.Append( mid, title )
           #     self.text1.Bind(wx.EVT_MENU, self.MenuSelectionCb )

        self.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        operation = self.tree_menu_title_by_id[ event.GetId() ]
        print 'Perform %s' %operation

    def RootSelectionCb( self, event ):
        print 'horaay'
        operation = event.GetString()
        print operation
        if operation == "Add table":
            self.c.execute('create table counts (GeneID text,times integer)')
            self.c.execute('''insert into counts values (?,?)''' ['hello',9])
            self.con.commit()
            self.doTreeCtrl()
            self.text1.Expand(self.root)
            
        
    
        
    # ============================
    # = ListBox Handling Methods =
    # ============================

    def OnColClick(self, event):
        
        self.col2Sort=event.GetColumn()
        if self.col2Sort == self.colsort:
            self.sortvar=abs(self.sortvar-1)
        else:
            self.sortvar=1
        self.colsort=self.col2Sort
        
        
        
        self.dbList.SortListItems(self.col2Sort,ascending=self.sortvar)



    def ListCntrlFill(self):
        self.dbList.ClearAll()
        self.dbList.InsertColumn(0, "#")
        self.dbList.SetColumnWidth(0, 80)
        iters = self.colNum 
        while iters  > 0:
            self.dbList.InsertColumn(self.colNum - iters+1, self.colTitles[iters - 1])
            self.dbList.SetColumnWidth(self.colNum - iters+1, 620 / self.colNum)
            iters -= 1
        

    def listRefill(self):
        if len(self.colTitles) > 0:
            self.c.execute('''select * from %s'''%self.TableName)
        else:
            self.c.execute('''select %s from %s'''%self.colTitles,self.TableName)
        self.data = self.c.fetchall()
        musicdata = dict()
        j = 0
        while j < len(self.data):
            rHo = [j]
            for col in self.data[j]:
                rHo.append(col)
            musicdata[j] = rHo
            j += 1
        self.dbList.itemIndexMap = musicdata.keys()
        self.dbList.itemDataMap = musicdata
        self.dbList.SetItemCount(len(musicdata)) 



    # ============================
    # == Tree Handling Methods ===
    # ============================


    def OnSelChanged(self,event):
        item =  event.GetItem()
        
        if self.text1.ItemHasChildren(item):
            child = self.text1.GetLastChild(item)
            self.colNum = self.text1.GetChildrenCount(item)
            i = 1
            self.TableName = self.text1.GetItemText(item)
            self.colTitles = [self.text1.GetItemText(child)]
            while i < self.colNum:
                child = self.text1.GetPrevSibling(child)
                self.colTitles.append(self.text1.GetItemText(child))
                i += 1
        else:
            self.colTitles = [self.text1.GetItemText(item)]
            self.TableName = self.text1.GetItemText(self.text1.GetItemParent(item))
            self.colNum = 1

        self.dbList.Show(False)
        self.dbList = TestListCtrl(self.panelRSLT, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL, size = (750,400), colNum = self.colNum+1, pos=(10,60))
        self.ListCntrlFill()
        self.listRefill()
        
        

    def doTreeCtrl(self):
        
        self.c.execute('''select name from sqlite_master where type="table"''')
        tns = self.c.fetchall()
        for tn in tns:
            tname = self.text1.AppendItem(self.root, tn[0])
            self.c.execute('''select * from %s'''%tn)
            cns = [destup[0] for destup in self.c.description]
            for cn in cns:
                cname = self.text1.AppendItem(tname, cn)
        self.text1.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        


    # ============================
    # == Event Handling Methods ==
    # ============================



#Database Menu Executables
    def helpDB(self,event):
        '''Respond to a type menu selection
        '''
        self.gonum=event.GetId()-self.lowDB
        self.dbsel = self.blastdbs.BDB().BlastDBS()[self.gonum]

#Type Menu Executables
    def helpEXE(self,event):
        '''Respond to a selection
        '''
        tempId = event.GetId()
        self.bnum=tempId-self.lowID
        self.ccmd = self.toolPlugins[self.bnum].blastPlugin().pluginEXE()
        
        self.typeMenu.Check(tempId,True)    
        
#Alphabet Menu Executables
    def doProtien (self, event):
        '''Respond to the "Peptide" alphabet command.
        '''
        self.abet = "AA"

    def doDNA (self, event):
        '''Respond to the "Nucleotide" alphabet command.
        '''
        self.abet = "DNA"

        
#File Menu Executables
    def doSaveAs(self, event):
        """ Respond to the "Save As" menu command.
        """
        if self.fileName == None:
            default = ""
        else:
            default = self.fileName

        curDir = os.getcwd()
        fileName = wx.FileSelector("Save File As", "Saving",
                                  default_filename=default,
                                  default_extension="xml",
                                  wildcard="*.xml",
                                  flags = wx.SAVE | wx.OVERWRITE_PROMPT)
        if fileName == "": return # User cancelled.
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)

        title = os.path.basename(fileName)
        self.SetTitle(title)

        self.fileName = fileName
        self.saveContents()

    def doExit(self, event):
        """ Respond to the "Quit" menu command.
        """
        self.askIfUserWantsToSave("closing")
        self.Destroy()

    def doOptions(self, event):
        """ Respond to the "Load" menu command.
        """

        self.optList=self.optBox.getOpts(self.abet,self.bnum)
        self.optBox.ShowModal()
        id,handle=self.menuHandlers[self.optBox.getBType()+10]
        handle(wx.EVT_MENU)
        self.typeMenu.Check(id,True)
        
        
    def doOpen(self, event):
        """ Respond to the "Load" menu command.
        """
        
        curDir = os.getcwd()
        fileName = wx.FileSelector("Load File", default_extension="",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)
        self.con = sqlite3.connect(fileName)
        self.c = self.con.cursor()
        self.text2.Clear()
        self.text2.write(fileName)
        self.doTreeCtrl()
        self.text1.Expand(self.root)

    def doNew(self, event):
        """ Respond to the "New" menu command.
        """
        
        newFrame = GuiFrame(None, -1)
        newFrame.Show(True)

    def doCreateDB(self, event):
        """ Respond to the "New Database" menu command.
        """
        
        import BlastDBCreateDiaolog
        newDBDialog = BlastDBCreateDiaolog.BlastDBCreateDiaolog(self, 'Create a new database', -1)
        newDBDialog.getDB(self)
        newDBDialog.ShowModal()

    def saveContents(self):
        """ Save the contents of our document to disk.
        """

        try:
            objData = []
            for obj in self.contents:
                objData.append([obj.__class__, obj.getData()])

            f = open(self.fileName, "wb")
            #cPickle.dump(objData, f)
            e = open("my_blast.xml")
            te = e.read()
            f.write(te)
            e.close()
            f.close()

            
            #self._adjustMenus()
        except:
            response = wx.MessageBox("Unable to load " + self.fileName + ".",
                                     "Error", wx.OK|wx.ICON_ERROR, self)





    def askIfUserWantsToSave(self, action):
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

            #self.saveContents()
            return True
        elif response == wx.NO:
            return True # User doesn't want changes saved.
        elif response == wx.CANCEL:
            return False # User cancelled.
        
#Blast Executable
    def toolEXE(self, evt):
        tempseq=self.text1.GetValue()

        tempfile = open("my_seq.fasta", "w")
        tempfile.write(str(tempseq))
        tempfile.close()
        

        #qu=str(Seq("my_seq.fasta"))
        cdlu=self.ccmd+" -query my_seq.fasta -db "+self.dbsel+" -evalue "+str(self.texte.GetValue())+" -outfmt 5 -out my_blast.xml -remote=True"
        self.text2.write(str(cdlu))
        p = subprocess.Popen(cdlu)
        p.wait()
        
        
        result_handle = open("my_blast.xml")
        blast_record = NCBIXML.read(result_handle)

        for alignment in blast_record.alignments:
             for hsp in alignment.hsps:
                 self.text2.write('****Alignment****')
                 self.text2.write('\nsequence: ')
                 self.text2.write(str(alignment.title))                    
                 self.text2.write('\nlength: ')
                 self.text2.write(str(alignment.length))                    
                 self.text2.write('\n e value: ')
                 self.text2.write(str(hsp.expect)+'\n')                    
                 self.text2.write(str(hsp.query[0:75]) + '...\n')
                 self.text2.write(str(hsp.match[0:75]) + '...\n')

        
                

 
#----------------------------------------------------------------------------

class optDialog(wx.Dialog):
    """ A frame showing the options of the alignment tools"""

    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================

    def __init__(self, parent, title, menuIn, fileName=None):
        """ Standard constructor.

            'parent', 'id' and 'title' are all passed to the standard wx.Frame
            constructor.  'fileName' is the name and path of a saved file to
            load into this frame, if any.
        """
        self.timesran=0
        self.boxList=[]
        self.abet="AA"
        
        
        
        wx.Dialog.__init__(self, parent, title=title, size=(800, 500))

        menuList=[]
        for arrow in menuIn.GetMenuItems():
            menuList.append(arrow.GetItemLabel())
        self.typeBox = wx.ComboBox(parent=self, id=-1, pos=(30,50), choices=menuList, style=wx.CB_READONLY, name="good luck")
        
        #self.typeBox.choices=menuList
        self.Bind(wx.EVT_COMBOBOX, self.doCOMBOSEL, self.typeBox,-1)
        self.typeBox.SetSelection(0)
        if self.timesran==0:
            self.doCOMBOSEL(wx.EVT_IDLE)

        
        for box in self.boxList:
            box.Destroy()
        self.boxList=[]


        
        
        
    def getOpts(self,bet,btype):
        self.abet=bet
        self.typeBox.SetSelection(btype)
        self.doCOMBOSEL(wx.EVT_IDLE)
        return self.boxList

    def getBType(self):
        return self.blstType
        
    def doCOMBOSEL(self, event):
        for box in self.boxList:
            box.Destroy()
        self.boxList=[]
        self.blstType=self.typeBox.GetCurrentSelection()
        
        self.boxList.append(wx.StaticText(self, -1, "DB size", pos=(300,30)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,50)))
        self.boxList.append(wx.StaticText(self, -1, "culling limit", pos=(300,80)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,100)))

        self.boxList.append(wx.StaticText(self, -1, "Gap Open Cost", pos=(300,130)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,150)))
        self.boxList.append(wx.StaticText(self, -1, "Gap Extend Cos", pos=(300,180)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,200)))

        self.boxList.append(wx.StaticText(self, -1, "Max. Number of Aligned Targets", pos=(300,230)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,250)))
        self.boxList.append(wx.StaticText(self, -1, "Number of Alignments to Show", pos=(300,280)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,300)))

        self.boxList.append(wx.StaticText(self, -1, "Number of 1-line Descriptions to Show", pos=(300,330)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,350)))
        self.boxList.append(wx.StaticText(self, -1, "Number of Threads to Use", pos=(300,380)))
        self.boxList.append(wx.TextCtrl(self, -1, "", size=(75,-1), pos=(300,400)))

        
        

        #Possibly not shown often self.matFileButton = filebrowsebutton.DirBrowseButton(parent=self, id=-1,pos=wx.Point(50,200), size=(500,50), labelText="Select Location\nof Desired Matrix")
            #gilist browser

        #XML or HTML output check boxes
        #Masking options could get messy
        #parse deflines checkbox
        #useful options for rest

        #To add:text-box for adding own options...l could present errors. need error calls.

    def doMsclOpts(self):
        #Check boxes or a refined way to show/hide certain options
        #Need to do this for all other Align Tools
        #Have fun
        self.boxList.append(wx.StaticText(self, -1, "Clustering Algorithm\n1st Iteration", pos=(150,30)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(150,70), choices=["upgma","upgmb","neighborjoining"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "Clustering Algorithm\n2nd Iteration", pos=(150,100)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(150,140), choices=["upgma","upgmb","neighborjoining"], style=wx.CB_READONLY)
        temp.SetSelection(1)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "Distance Measure 1", pos=(150,170)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(150,200), choices=["kmer6_6","kmer20_3", "kmer20_4", "kbit20_3", "kmer4_6"], style=wx.CB_READONLY)
        if self.abet=="AA":
            temp.SetSelection(0)
            self.boxList.append(temp)
        else:
            temp.SetSelection(4)
            self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "Distance Measures 2", pos=(150,225)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(150,250), choices=["kmer6_6","kmer20_3", "kmer20_4", "kbit20_3","pctid_kimura","pctid_log"], style=wx.CB_READONLY)
        temp.SetSelection(4)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "Objective Scores", pos=(150,280)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(150,300), choices=["sp","ps","dp","xp","spf","spm"], style=wx.CB_READONLY)
        temp.SetSelection(5)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "Tree Root Methods", pos=(150,330)))
        self.boxList.append(wx.ComboBox(parent=self, id=-1, pos=(150,350), choices=["psuedo","midlongestspan","minavgleafdist"], style=wx.CB_READONLY))    

        self.boxList.append(wx.StaticText(self, -1, "1st Weighting Scheme", pos=(300,140)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(300,160), choices=["none", "clustalw", "henikoff", "henikoffpb","gsc", "threeway"], style=wx.CB_READONLY)
        temp.SetSelection(0)
        self.boxList.append(temp)
        self.boxList.append(wx.StaticText(self, -1, "2nd Weighting Scheme", pos=(300,180)))
        temp=wx.ComboBox(parent=self, id=-1, pos=(300,200), choices=["none", "clustalw", "henikoff", "henikoffpb","gsc", "threeway"], style=wx.CB_READONLY)
        temp.SetSelection(1)
        self.boxList.append(temp)

        self.boxList.append(wx.StaticText(self, -1, "Anchor Spacing", pos=(300,30)))
        self.boxList.append(wx.TextCtrl(self, -1, "32", size=(75,-1), pos=(300,50)))
        self.boxList.append(wx.StaticText(self, -1, "Center", pos=(300,80)))
        self.boxList.append(wx.TextCtrl(self, -1, "1.0", size=(75,-1), pos=(300,100)))

        self.boxList.append(wx.StaticText(self, -1, "Hydrophobic Window", pos=(500,30)))
        self.boxList.append(wx.TextCtrl(self, -1, "5", size=(75,-1), pos=(500,50)))
        self.boxList.append(wx.StaticText(self, -1, "Hydrophobic Gap Penalty", pos=(500,80)))
        self.boxList.append(wx.TextCtrl(self, -1, "1.2", size=(75,-1), pos=(500,100)))

        self.boxList.append(wx.StaticText(self, -1, "Max. Hours to Run", pos=(500,130)))
        self.boxList.append(wx.TextCtrl(self, -1, "0.0", size=(75,-1), pos=(500,150)))
        self.boxList.append(wx.StaticText(self, -1, "Max. Iterations", pos=(500,180)))
        self.boxList.append(wx.TextCtrl(self, -1, "16", size=(75,-1), pos=(500,200)))

        self.boxList.append(wx.StaticText(self, -1, "Max. Tress", pos=(500,230)))
        self.boxList.append(wx.TextCtrl(self, -1, "1", size=(75,-1), pos=(500,250)))

        self.boxList.append(wx.StaticText(self, -1, "Min. Best Column Score", pos=(650,30)))
        self.boxList.append(wx.TextCtrl(self, -1, "1.0", size=(75,-1), pos=(650,50)))
        self.boxList.append(wx.StaticText(self, -1, "Min. Smooth Score", pos=(650,80)))
        self.boxList.append(wx.TextCtrl(self, -1, "1.0", size=(75,-1), pos=(650,100)))
        self.boxList.append(wx.StaticText(self, -1, "Smooth Score Ceiling", pos=(650,130)))
        self.boxList.append(wx.TextCtrl(self, -1, "1.0", size=(75,-1), pos=(650,150)))
        self.boxList.append(wx.StaticText(self, -1, "Smooth Window", pos=(650,180)))
        self.boxList.append(wx.TextCtrl(self, -1, "7", size=(75,-1), pos=(650,200)))

        self.boxList.append(wx.StaticText(self, -1, "SUEFF Value", pos=(650,230)))
        self.boxList.append(wx.TextCtrl(self, -1, "0.1", size=(75,-1), pos=(650,250)))
        

           
def GetName():
    '''
    Method to return name of tool
'''
    return 'SQuirreL'

def GetBMP():
    return r".\Utils\Icons\SQuirreL.bmp"
    
'''
#----------------------------------------------------------------------------   

#Code to start gui
class MyApp(wx.App):
    def OnInit(self):
        sys.path.append(r'C:\Users\francis\Documents\Monguis\BioGui\Utils')
        import defaultColors
        cL = defaultColors.getColors()
        frame = GuiFrame(None,-1,r'C:\Users\francis\Documents\Monguis\BioGui',cL)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True                
        


global app        
app = MyApp(redirect=True)
app.MainLoop()'''

