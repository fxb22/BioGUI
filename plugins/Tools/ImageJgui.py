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
from Bio import Entrez

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
        return 'ImageJ'

    def GetBMP(self):
        '''
        Method to return identifying image
        '''
        return r".\Utils\Icons\imagej.bmp"

    def GetPlugIns(self):
        '''
        Method to identify 3D visualization plugins
        '''

        self.PIlist = os.listdir(self.homeDir + r"\plugins\Tools\EtoolsPlugins")
        sys.path.append(self.homeDir + r"\plugins\Tools\EtoolsPlugins")
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

    def __init__(self, parent, title, homeDir, cL):
        self.homeDir = homeDir
        Entrez.email = "bioGui@BioGUI.com"
        """
        Standard constructor.
        'parent', 'id' and 'title' are all passed to the standard wx.Frame
        constructor.  'fileName' is the name and path of a saved file to
        load into this frame, if any.
        """        
        wx.Frame.__init__(self, parent, title='Entrez E-Utilities GUI', size=(1000, 620))
        self.SetBackgroundColour('#FBFFCF')
        self.GetPlugIns()
        self.buttons = []

        # Menu item IDs:

        menu_OPTIONS      = wx.NewId()     # File menu items
        menu_ETOOLS       = wx.NewId()     # BLAST command
        
        self.toolGoMenu=[]                 # Tools menu options.
        for dummy in self.toolPlugins:     # Iterate through all available tools
            self.toolGoMenu.append(wx.NewId())
        
        #menu_ABOUT        = wx.NewId()                 # Help menu items.
        
        # Setup our menu bar.
        self.menuBar = wx.MenuBar()

        #Setup options for the file menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_NEW,    "New\tCtrl-N",    "Create a new window")
        self.fileMenu.Append(wx.ID_OPEN,   "Load...",        "Load an existing eTools result")
        self.fileMenu.Append(menu_ETOOLS,  "ETOOL GO",       "Perform eTools action")
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
            self.typeMenu.Append(self.toolGoMenu[itnum],   tool.etPlugin().GetName(),      kind=wx.ITEM_RADIO)
        #Setup the type menu
        self.menuBar.Append(self.typeMenu,         "Type")

        # Create our toolbar.

        tsize = (15,15)
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

        self.toolbar.AddSimpleTool(
            wx.ID_NEW, wx.Bitmap(self.homeDir + r"\Utils\Icons\Blank.bmp", wx.BITMAP_TYPE_BMP), "New")
        self.toolbar.AddSimpleTool(
            wx.ID_OPEN, wx.Bitmap(self.homeDir + r"\Utils\Icons\openFolder.bmp", wx.BITMAP_TYPE_BMP), "Open")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.homeDir + r"\Utils\Icons\Disk.bmp", wx.BITMAP_TYPE_BMP), "Save")
        self.toolbar.AddSimpleTool(
            wx.ID_SAVEAS, wx.Bitmap(self.homeDir + r"\Utils\Icons\diskCopied.bmp", wx.BITMAP_TYPE_BMP), "Save As...")
        self.toolbar.AddSimpleTool(
            wx.ID_EXIT, wx.Bitmap(self.homeDir + r"\Utils\Icons\RedX.bmp", wx.BITMAP_TYPE_BMP), "Exit")
        self.toolbar.AddSeparator()
        for itnum,tool in enumerate(self.toolPlugins):
            name = tool.etPlugin().GetName()
            BMP = tool.etPlugin().GetBMP(self.homeDir)
            self.toolbar.AddSimpleTool(
                self.toolGoMenu[itnum], wx.Bitmap(BMP, wx.BITMAP_TYPE_BMP), name)

        self.toolbar.SetBackgroundColour('LIGHT GRAY')
        self.toolbar.Realize()

        # Associate menu/toolbar items with their handlers.
        self.menuHandlers = [
            (menu_ETOOLS,      self.toolEXE),
            (wx.ID_NEW,        self.doNew),
            (wx.ID_OPEN,       self.doOpen),
            (wx.ID_EXIT,       self.doExit),
            (wx.ID_SAVEAS,     self.doSaveAs),
            (menu_OPTIONS,     self.doOptions),
            ]
        tempIdNum = len(self.menuHandlers)
        
        for itnum,tool in enumerate(self.toolPlugins):       
            self.menuHandlers.append((self.toolGoMenu[itnum],     self.helpEXE))

        self.lowID,dummy = self.menuHandlers[tempIdNum]

        #Update Menu Bar with User Input
        for combo in self.menuHandlers:
            id, handler = combo[:2]
            self.Bind(wx.EVT_MENU, handler, id = id)
            if len(combo)>2:
                self.Bind(wx.EVT_UPDATE_UI, combo[2], id = id)
        #Set the menu bar
        self.SetMenuBar(self.menuBar)

        #Create user interface appearance       
        self.panelSQ = wx.Panel(self, -1, pos=(7,15), size=(976,70), style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour('#53728c')

        self.panelRSLT = wx.Panel(self, -1, pos=(7,85), size=(976,440), style=wx.BORDER_RAISED)
        self.panelRSLT.SetBackgroundColour('#53728c')

        #Create user interface text boxes
        #Create sequence input box and label. Allow input to be modified.
        self.l1 = wx.StaticText(self.panelSQ, -1, "Query: ", pos=(445,10))
        self.l1.SetForegroundColour('WHITE')
        self.text1 = wx.TextCtrl(self.panelSQ, -1, "", size=(260, 53),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(490,6))
        wx.CallAfter(self.text1.SetInsertionPoint, 0)

        #Create results outbox and lable. The box is able to be modified.
        self.l2 = wx.StaticText(self.panelRSLT, -1, "Results: ", pos=(25,10))
        self.l2.SetForegroundColour('WHITE')
        self.text2 = []
        self.text2.append(wx.TextCtrl(self.panelRSLT, -1, "", size=(892, 390),
                         style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(75,10)))
        wx.CallAfter(self.text2[0].SetInsertionPoint, 0)

        #Create ETOOL GO action button
        etGObutton = wx.Button(self.panelSQ, -1, "GO!", pos=(820,6), size=(75,25))
        etGObutton.SetBackgroundColour('RED')
        etGObutton.SetForegroundColour('WHITE')
        self.Bind(wx.EVT_BUTTON, self.toolEXE, etGObutton)

        #Create USE RESULTS action button
        urGObutton = wx.Button(self.panelSQ, -1, "Use Results", pos=(820,35), size=(75,25))
        urGObutton.SetBackgroundColour('WHITE')
        urGObutton.SetForegroundColour('RED')
        self.Bind(wx.EVT_BUTTON, self.doReuse, urGObutton)

        #Create User Modifiable search parameters.
        self.l3 = wx.StaticText(self.panelSQ, -1, "Database: ", pos=(195,10))
        self.l3.SetForegroundColour('WHITE')
        self.dbCB = wx.ComboBox(parent=self.panelSQ, id=-1, pos=(256,6),
                         choices=["All", "Books", "Cancer Chromosomes", "CDD","CoreNucleotide", "3D Domains",
                                  "EST", "Gene", "Genome", "Genome Project", "dbGaP", "GENSAT", "GEO Datasets",
                                  "GEO Profiles", "GSS", "HomoloGene", "Journnals", "MeSH", "NCBI Web Site",
                                  "NLM Catalog", "OMIA", "OMIM", "PopSet", "Probe", "Protein",
                                  "PubChem BioAssay", "PubChem Compound", "PubChem Substance", "PubMed",
                                  "PubMed Central", "SNP", "Structure", "Taxonomy", "UniGene", "UniSTS"],
                         style=wx.CB_READONLY)
        self.dbCB.SetSelection(0)

        self.l4 = wx.StaticText(self.panelSQ, -1, "E-Utility: ", pos=(18,10))
        self.l4.SetForegroundColour('WHITE')

        etCbchoices = []
        for tool in self.toolPlugins:
            etCbchoices.append(tool.etPlugin().GetName())
        self.etoolCB = wx.ComboBox(parent=self.panelSQ, id=-1, pos=(75,6), choices=etCbchoices, style=wx.CB_READONLY)

        #Initialization of variables
        self.curIDs=[]

    #Additional methods
    def doReuse(self,event):
        print self.curIDs
        if len(self.curIDs)>0:
            idBox = reuseBox(self,self.curIDs)
            idBox.ShowModal()
            newID = idBox.getRet()
            self.text1.Clear()
            self.text1.write(newID)
        else:
            print 'holdup'
        
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
        
#Type Menu Executables
    def helpEXE(self,event):
        tempId = event.GetId()
        self.bnum=tempId-self.lowID
        self.ccmd = self.toolPlugins[self.bnum].blastPlugin().pluginEXE()
        
        self.typeMenu.Check(tempId,True)

#eTools Executable
    def toolEXE(self, evt):
        dbName = self.dbCB.GetValue()
        if dbName == 'All':
            dbName = ''
        idName = self.text1.GetValue()
        if idName == '':
            self.text2.write('plese enter a query')
        else:
            Btn = evt.GetEventObject()
            print self.toolPlugins[self.etoolCB.GetSelection()].etPlugin().GetName()
            self.curIDs = self.toolPlugins[self.etoolCB.GetSelection()].etPlugin().GetExec(self,dbName,idName)
            
        
        

#----------------------------------------------------------------------------   
'''
#Code to start gui
class MyApp(wx.App):
    def OnInit(self):
        frame = GuiFrame(None,-1,r'C:\Users\francis\Documents\Monguis\BioGui')
        self.SetTopWindow(frame)
        frame.Show(True)
        return True            
        '''

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
        
        

def GetName():
    '''
    Method to return name of tool
    '''
    return 'ImageJ'

def GetBMP():
    '''
    Method to return identifying image
    '''
    return r".\Utils\Icons\imagej.bmp"
'''
global app        
app = MyApp(redirect=True)
app.MainLoop()
'''    
                

         
