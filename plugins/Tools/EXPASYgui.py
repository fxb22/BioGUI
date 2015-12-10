#Import packages that will be used
#GUI generation Packages
import wx
import wx.aui
from wx.lib.buttons import GenBitmapButton,GenBitmapToggleButton
#Operational Packages
import subprocess
import traceback
import types
import os
import sys
import errno
import numpy as np

from xml.dom import minidom


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
        return 'ExPASy'

    def GetBMP(self):
        '''
        Method to return identifying image
        '''
        return r".\Utils\Icons\ExPASy.bmp"

    def GetPlugIns(self):
        '''
        Method to identify 3D visualization plugins
        '''
        self.PIlist = os.listdir(self.hD + r"\plugins\Tools\ExpasyPlugins")
        del sys.path[-1]
        del sys.path[-1]
        del sys.path[-1]
        del sys.path[-1]
        del sys.path[-1]
        sys.path.append(self.hD + r"\plugins\Tools\ExpasyPlugins")
        self.toolPlugins=[]
        for i,filePI in enumerate(self.PIlist):
            (self.PIname, self.PIext) = os.path.splitext(filePI)
            if self.PIext == '.py':
                self.toolPlugins.append(__import__(str(self.PIname)))

    def SetQuery(self,qseq):
        self.SeqRecs = qseq

    
    # ==========================================
    # == Initialization and Window Management ==
    # ==========================================

    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title='Swiss-Prot / ExPASy Interface')
        #self.parent = parent
        if 'homeDir' in kwargs.keys():
            self.hD = kwargs['homeDir']
        else:
            self.hD = os.getcwd()
        self.SetBackgroundColour('#FBFFCF')
        self.GetPlugIns()
        self.dbList = ['uniprot', 'uniref', 'uniparc', 'citations', 'taxonomy',
                       'keywords', 'locations', 'database']

        self.colPoss = dict()
        self.colPoss['uniprot'] = [['id','entry name','reviewed','protein names','genes','organism','length',
                                    '3d','created','last-modified','sequence-modified','domains','ec',
                                    'features','fragment','encodedon','go','go-id','interpro','interactor',
                                    'keywords','citationmapping','context','organism-id','pathway','existence',
                                    'families','citation','sequence','subcellular locations','tools',
                                    'virus hosts'],7]
        self.colPoss['uniref'] =  [['Status','Cluster name','Size','Cluster member(s)',
                                   'Organism','Length','Identity','Common Taxon',
                                   'Date of creation','Matched text','Organism IDs',
                                   'Reference sequence'],7]
        self.colPoss['uniparc'] = [['Oganisms','UniProtKB','First Seen','Last Seen','Length',
                                   'Checksum','Matched text','Organism IDs','Sequence'],5]

        # Menu item IDs:

        menu_OPTIONS      = wx.NewId()     # File menu items
        menu_EXPASY       = wx.NewId()     # BLAST command
        
        self.toolGoMenu=[]                 # Tools menu options.
        for dummy in self.toolPlugins:     # Iterate through all available tools
            self.toolGoMenu.append(wx.NewId())

        self.dbGoMenu=[]                                # Database menu options.
        for dummy in self.dbList:    # Iterate through all available databases
            self.dbGoMenu.append(wx.NewId())
        
        self.menu_ABOUT         = wx.NewId()                 # Help menu items.
        self.menu_TOOLBARV      = wx.NewId()
        self.menu_COLOPTS       = wx.NewId()
        
        # Setup our menu bar.
        self.menuBar = wx.MenuBar()

        #Setup options for the file menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_NEW,    "New\tCtrl-N",    "Create a new window")
        self.fileMenu.Append(wx.ID_OPEN,   "Load...",        "Load an existing eTools result")
        self.fileMenu.Append(menu_EXPASY,  "GO",             "Perform action")
        self.fileMenu.Append(menu_OPTIONS, "Options...",     "Options...")
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_SAVEAS, "Save As...")
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT,   "Quit\tCtrl-Q")
        #Setup the file menu
        self.menuBar.Append(self.fileMenu, "File")

        #Setup the Program type menu options
        self.typeMenu = wx.Menu()
        for itnum,tool in enumerate(self.toolPlugins):
            self.typeMenu.Append(self.toolGoMenu[itnum],   tool.Plugin().GetName(),      kind=wx.ITEM_RADIO)
        #Setup the type menu
        self.menuBar.Append(self.typeMenu,         "Type")

        #Setup the database menu options
        self.dbaseMenu = wx.Menu()
        for itnum,tool in enumerate(self.dbList):
            self.dbaseMenu.Append(self.dbGoMenu[itnum],   tool,      kind=wx.ITEM_RADIO)
        #Setup the database menu
        self.menuBar.Append(self.dbaseMenu, "Database")

        #Set up the options menu options
        self.helpMenu = wx.Menu()
        self.helpMenu.Append(self.menu_TOOLBARV, "Toolbar on/off",      kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.menu_COLOPTS,  "Colors...",           kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.menu_ABOUT,    "About...")
        #Setup the option menu
        self.menuBar.Append(self.helpMenu,         "Help")
        
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
        for itnum,tool in enumerate(self.toolPlugins):
            name = tool.Plugin().GetName()
            BMP = tool.Plugin().GetBMP(self.hD)
            self.toolbar.AddSimpleTool(
                self.toolGoMenu[itnum], wx.Bitmap(BMP, wx.BITMAP_TYPE_BMP), name)

        self.toolbar.SetBackgroundColour('LIGHT GRAY')
        self.toolbar.Realize()

        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (menu_EXPASY,      self.toolEXE),
            (wx.ID_NEW,        self.doNew),
            (wx.ID_OPEN,       self.doOpen),
            (wx.ID_EXIT,       self.doExit),
            (wx.ID_SAVEAS,     self.doSaveAs),
            (menu_OPTIONS,     self.doOptions),
            (self.menu_TOOLBARV,  self.doTBOnOff),
            (self.menu_COLOPTS,   self.doColDlg),
            ]
        tempIdNum = len(self.menuHandlers)
        
        for itnum,tool in enumerate(self.toolPlugins):       
            self.menuHandlers.append((self.toolGoMenu[itnum],     self.helpEXE))

        self.lowID,dummy = self.menuHandlers[tempIdNum]

        for itnum,tool in enumerate(self.dbList):       
            self.menuHandlers.append((self.dbGoMenu[itnum],     self.helpDB))
            
        self.lowDB,dummy = self.menuHandlers[len(self.toolPlugins)+tempIdNum]

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
        self.panelSQ = wx.Panel(self, -1, pos=(7,15), size=(976,105), style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour('#53728c')

        self.panelRSLT = wx.Panel(self, -1, pos=(7,120), size=(976,405), style=wx.BORDER_RAISED)
        self.panelRSLT.SetBackgroundColour('#53728c')

        #Create user interface text boxes
        #Create input box and label. Allow input to be modified.
        self.l1 = wx.StaticText(self.panelSQ, -1, "Query: ", pos=(460,10))
        self.l1.SetForegroundColour('WHITE')
        self.text1 = wx.TextCtrl(self.panelSQ, -1, "", size=(300, 40),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(505,6))
        wx.CallAfter(self.text1.SetInsertionPoint, 0)

        #Create results outbox and label. The box is able to be modified.
        self.l2 = wx.StaticText(self.panelRSLT, -1, "Results: ", pos=(25,10))
        self.l2.SetForegroundColour('WHITE')
        self.text2 = wx.TextCtrl(self.panelRSLT, -1, "", size=(892, 370),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10))
        wx.CallAfter(self.text2.SetInsertionPoint, 0)

        #Create holder for tool specific windows
        self.windowBin = []

        #Create action button
        self.GObutton = wx.Button(self.panelSQ, -1, "GO!", pos=(835,6), size=(75,25))
        self.GObutton.SetBackgroundColour('RED')
        self.GObutton.SetForegroundColour('WHITE')
        self.Bind(wx.EVT_BUTTON, self.toolEXE, self.GObutton)

        #Create USE RESULTS action button
        self.urGObutton = wx.Button(self.panelSQ, -1, "Use Results", pos=(835,35), size=(75,25))
        self.urGObutton.SetBackgroundColour('WHITE')
        self.urGObutton.SetForegroundColour('RED')
        self.Bind(wx.EVT_BUTTON, self.doReuse, self.urGObutton)

        #Create User Modifiable search parameters.
        self.l3 = wx.StaticText(self.panelSQ, -1, "Database: ", pos=(450, 56))
        self.l3.SetForegroundColour('WHITE')
        self.dbCB = wx.ComboBox(parent=self.panelSQ, id=-1, pos=(505,54),
                         choices=self.dbList, style=wx.CB_READONLY)
        self.HasLB = False
        self.dbCB.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.helpDB, self.dbCB)
        self.helpDB(wx.wxEVT_COMMAND_CHECKBOX_CLICKED)
        
        
        
        
        #Set initial conditions
        self.fileName=""
        #Initialization of variables
        self.tbOnOff = 1
        

        #self.optBox=optDialog(self, 'Options Menu', self.typeMenu, -1)

    # ============================
    # == Event Handling Methods ==
    # ============================

#Database Menu Executables
    def helpDB(self,event):
        '''Respond to a type menu selection
        '''
        #print event.GetId()
        try:
            if event.GetId() > 0:
                self.gonum = event.GetId()-self.lowDB
            else:
                self.gonum = self.dbCB.GetSelection()
        except:
            self.gonum = self.dbCB.GetSelection()
        #self.dbsel = dbList[self.gonum]
        self.dbCB.SetSelection(self.gonum)
        self.dbaseMenu.Check(self.gonum + self.lowDB ,True)
        namers = self.dbList[self.gonum]
        if self.HasLB:
            self.colPossLB.Show(False)
            self.colSetLB.Show(False)
            self.addButton.Show(False)
            self.removeButton.Show(False)
        if self.colPoss.has_key(namers):
            itmax = self.colPoss[namers][1]
            self.possCol = self.colPoss[namers][0][itmax:]
            #Create list controls for column selection
            self.colPossLB = wx.ListBox(self.panelSQ, -1, (18,21), (150,73),
                                        self.possCol,
                                        style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
            self.colSet = self.colPoss[namers][0][:itmax]
            self.colSetLB = wx.ListBox(self.panelSQ, -1, (258,21), (150,73),
                                       self.colSet,
                                       style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
            self.addButton = wx.Button(self.panelSQ, -1, label = u'add >>', name = 'button1',
                                       pos = (179, 37), size = (60,-1))
            self.removeButton = wx.Button(self.panelSQ, -1, label = u'<< remove', name = 'button2',
                                          pos = (179, 63), size = (60,-1))
            self.addButton.Bind(wx.EVT_BUTTON, self.onAdd)
            self.removeButton.Bind(wx.EVT_BUTTON, self.onRemove)


            self.HasLB = True
        else:
            self.HasLB = False

#Add button executable
    def onAdd(self,event):
        '''Respond to a ADD button click
        '''
        for sel in self.colPossLB.GetSelections():
            self.colSet.append(self.possCol[sel])
        self.colSetLB.Show(False)
        self.colSetLB = wx.ListBox(self.panelSQ, -1, (258,21), (150,73),
                                        self.colSet,
                                        style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
        self.colSetLB.Show(True)
        temp = []
        iowa = 0
        while iowa < len(self.possCol):
            if not iowa in self.colPossLB.GetSelections():
                temp.append(self.possCol[iowa])
            iowa += 1
        self.possCol = temp
        self.colPossLB.Show(False)
        self.colPossLB = wx.ListBox(self.panelSQ, -1, (18,21), (150,73),
                                        self.possCol,
                                        style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
        self.colPossLB.Show(True)

#Remove button executable
    def onRemove(self,event):
        '''Respond to a REMOVE button click
        '''
        for sel in self.colSetLB.GetSelections():
            self.possCol.append(self.colSet[sel])
        self.colPossLB.Show(False)
        self.colPossLB = wx.ListBox(self.panelSQ, -1, (18,21), (150,73),
                                        self.possCol,
                                        style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
        self.colPossLB.Show(True)
        temp = []
        iowa = 0
        while iowa < len(self.colSet):
            if not iowa in self.colSetLB.GetSelections():
                temp.append(self.colSet[iowa])
            iowa += 1
        self.colSet = temp
        self.colSetLB.Show(False)
        self.colSetLB = wx.ListBox(self.panelSQ, -1, (258,21), (150,73),
                                        self.colSet,
                                        style = wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.HSCROLL)
        self.colSetLB.Show(True)
        
#USE RESULTS button executable
    def doReuse(self,event):
        '''Respond to a USE RESULTS button click
        '''
        if len(self.curIDs)>0:
            idBox = reuseBox(self,self.curIDs)
            idBox.ShowModal()
            newID = idBox.getRet()
            self.text1.Clear()
            self.text1.write(newID)
        else:
            print 'holdup'

#Date button executable
    def doMDY(self,event):
        '''Respond to a Set Date(s) button click
        '''
        mdyBox = dateBox(self)
        mdyBox.ShowModal()        
        
#Type Menu Executables
    def helpEXE(self,event):
        '''Respond to a selection
        '''
        idk = 0
        while idk < len(self.windowBin):
            self.windowBin[idk].Show(False)
            self.windowBin.pop(idk)
            
        self.l1.Show(False)
        self.text1.Show(False)
        self.l2.Show(False)
        self.text2.Show(False)
        self.l3.Show(False)
        #self.dbCB.Show(False)
                
        idk = 0
        while idk < len(self.windowBin):
            self.windowBin[idk].Show(False)
            
        if event.GetId() > 0:
            self.bnum = event.GetId() - self.lowID
        else:
            self.bnum = 1#self.etoolCB.GetSelection()
            
        #self.etoolCB.SetSelection(self.bnum)
        #self.typeMenu.Check(self.bnum + self.lowID,True)
            
        self.toolPlugins[self.bnum].Plugin().helpEXE(self)
            

#File Menu Executables
    def doSaveAs(self, event):
        """ Respond to the "Save As" menu command.
        """
        if self.fileName == None:
            default = ""
        else:
            default = self.fileName = wx.FileSelector("Save File As", "Saving",
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
        fileName = wx.FileSelector("Load File", default_extension=".fasta",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return
        fileName = os.path.join(os.getcwd(), fileName)
        os.chdir(curDir)

        fasta_string = open(fileName).read()
        self.text1.write(fasta_string)

    def doNew(self, event):
        """ Respond to the "New" menu command.
        """
        
        newFrame = GuiFrame(None, -1)
        newFrame.Show(True)

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
        
#eTools Executable
    def toolEXE(self, evt):
        idk = 0
        while idk < len(self.windowBin):
            self.windowBin[idk].Show(False)
            self.windowBin.pop(idk)
            
        dbName = self.dbCB.GetValue()
        if dbName == 'All':
            dbName = ''
        idName = self.text1.GetValue()
        if idName == '':
            #if not self.etoolCB.GetValue() == 'EInfo':
            #    self.text2.write('please enter a query')
            #else:
                Btn = evt.GetEventObject()
                self.curIDs = self.toolPlugins[1].Plugin().GetExec(self,dbName,idName)
        else:
            Btn = evt.GetEventObject()
            self.curIDs = self.toolPlugins[1].Plugin().GetExec(self,dbName,idName)
            
#--------------------------Help Menu Executables---------------------
    def doAbout(self,event):
        #Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription("Have an angry day!")
        wx.AboutBox(info)

    def doTBOnOff(self,event):
        #Respond to the "Tollbar On/Off" menu command
        self.tbOnOff = abs(self.tbOnOff-1)
        if self.tbOnOff:
            self.toolbar.Show(True)
        else:
            self.toolbar.Show(False)
        self.panelSQ.Show(False)
        self.panelSQ.SetPosition((7,15))
        self.panelSQ.Show(True)
        self.panelRSLT.Show(False)
        self.panelRSLT.SetPosition((7,85))
        self.panelRSLT.Show(True)

    def doColDlg(self,event):
        import changeColorDialog
        dlg = changeColorDialog.changeColorDialog(self,self.colorList, self.hD)
        dlg.ShowModal()        
        
"""
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
        """

class reuseBox(wx.Dialog):
    """ A frame showing the alignment of the selected Blast Record alignment"""

    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================

    def __init__(self, parent, idChoices):

        wx.Dialog.__init__(self, parent, title='ID selection', size=(200, 100))
        selTxt = wx.StaticText(self, -1, "Please select ID:", pos=(5,10))
        selTxt.SetForegroundColour('BLACK')

        self.selBool = False
        self.retkey=idChoices[0]
        self.idCB = wx.ComboBox(parent=self, id=-1, pos=(100,10), choices=idChoices, style=wx.CB_READONLY)

        #Create return button
        retbutton = wx.Button(self, -1, "OK", pos=(40,50), size=(50,25))
        retbutton.SetBackgroundColour('RED')
        retbutton.SetForegroundColour('WHITE')
        self.Bind(wx.EVT_BUTTON, self.retMain, retbutton)

    def retMain(self,evt):
        self.retkey = self.idCB.GetValue()
        self.Destroy()

    def getRet(self):
        return self.retkey

class dateBox(wx.Dialog):
    """ A frame showing the alignment of the selected Blast Record alignment"""

    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================

    def __init__(self, parent, idChoices):

        wx.Dialog.__init__(self, parent, title='ID selection', size=(200, 100))

        
        
def GetName():
    '''
    Method to return name of tool
    '''
    return 'ExPASy'

def GetBMP():
    '''
    Method to return identifying image
    '''
    return r".\Utils\Icons\ExPASy.bmp"

"""
global app        
app = MyApp(redirect=True)
app.MainLoop()"""
  
                

         
