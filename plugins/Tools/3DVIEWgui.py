#Import packages that will be used
#GUI generation Packages
import wx
#Operational Packages
import subprocess
import os
import sys
import numpy as np
from numpy import arange, cos, sin, pi
import matplotlib as mpl
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import axes3d
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from Bio.PDB.PDBParser import PDBParser
import plotter as mpl
import getPlugins as gpi
import MenuToolBarSetup as mtbs

#----------------------------------------------------------------------------
class GuiFrame(wx.Frame):
    """ A frame showing the contents of a single document. """

    # ==========================================
    # ===== Methods for Plug-in Management =====
    # ==========================================

    def GetName(self):
        #Method to return name of tool
        return '3D Views'

    def GetBMP(self):
        #Method to return identifying image
        return self.hD + r"\Utils\Icons\binocular.bmp"

    def SetQuery(self,rec):
        self.Rec = rec
        self.GetExec()
        
    #----------------------Frame Initialization-----------------
    def HelpExec(self,event):
        # Respond to a type selection
        2
        
    def DoProtien (self, event):
        # Respond to the "Peptide" alphabet command.
        self.abet = "AA"

    def DoDNA(self, event):
        # Respond to the "Peptide" alphabet command.
        self.abet = "AA"

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
        self.alphaMenu.Check(self.menu_PROTIEN, True)
        
    def DoOpen(self, event):
        """ Respond to the "Load" menu command.
        """
        self.rec = []
        
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
                 
    def DoAbout(self,event):
        # Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription(
            "Interface to draw 3-D representations of proteins\n"+
            "Capable of drawing for pdb or mmdb files\n\n" +
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
        
    def VarInit(self):
        self.rec = []
        self.menuBar = wx.MenuBar()
        self.pTools = {}
        self.dTools = []
        self.activeDraw = ''
        self.pButtons = []
        self.dButtons = []

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def GetPlugins(self):
        #Method to identify 3D visualization plugins
        self.pList = gpi.GetPlugIns(self.hD + r"\plugins\Tools\3DViewPlugins")
        for i,p in enumerate(self.pList):
            if str(self.pList[p].GetName())[-1] == '^':
                self.dTools.append(self.pList[p])
                if str(self.pList[p].GetName())[:-1] == r"Ribbon":
                    self.activeDraw = self.dTools[-1]
            else:
                self.pTools[p] = self.pList[p]

    def SetPanels(self):
        self.bPSize = self.GetSize()
        self.panelSQ = wx.Panel(self, -1, pos=(7,7),
                           size=(self.bPSize[0] - 25,70),
                           style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.panelR = wx.Panel(self, -1, pos = (7,87),
                             size=(self.bPSize[0] - 25,self.bPSize[1] - 150),
                             style=wx.BORDER_RAISED)
        self.panelR.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])

    def SetPButtons(self):
        xPos = 15
        for tool in self.pTools.keys():
            BMP = self.pTools[tool].GetBMP(self.hD)
            bmp = wx.Image(BMP, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
            temp = wx.BitmapButton(self.panelSQ, -1, bmp, pos = (xPos, 8),
                                   size = (50, 50), name = tool)
            self.Bind(wx.EVT_BUTTON, self.OnBtnHit, temp)
            self.pButtons.append(temp)
            xPos += 60

    def SetDButtons(self):
        xPos = 906
        for tool in self.dTools:
            Bname = tool.GetName()
            BMP = tool.GetBMP(self.hD)
            bmp = wx.Image(BMP, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
            temp = wx.BitmapButton(self.panelSQ, -1, bmp, pos = (xPos, 8),
                                   size = (50, 50), name = Bname)
            self.Bind(wx.EVT_BUTTON, self.OnDrawBtnHit, temp)
            self.dButtons.append(temp)
            xPos -= 60

    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title='3-Dimensional Visualization Interface')
        #self.parent = parent
        if 'homeDir' in kwargs.keys():
            self.hD = kwargs['homeDir']
        else:
            import os
            self.hD = os.getcwd()
        self.VarInit()
        self.GetColors()
        self.SetBackgroundColour(self.colorList['Tool']['Back'])
        self.GetPlugins()
        mts = mtbs.MenuToolBarSetup(self, self.pTools, self.hD)
        self.plugIds = mts.GetIDs()
        mts.DoMenubar("DRAW!","Draw structure",False, False, False, False)
        self.SetPanels()
        self.SetPButtons()
        self.SetDButtons()
        s = self.panelR.GetSize()
        #self.toolbar.Show(False)
        self.menuBar.Show(True)
        self.plotter = mpl.PlotNotebook(self.panelR,size=(s[0]-18,s[1]-18),
                                        pos=(5, 5))
        self.ax = self.plotter.add('figure1')
        self.ax2 = self.ax.gca(projection='3d')
        self.ax2.axis('off')

    def HelpExec(self, event):
        self.GetExec(event)

    def GetExec(self):
        #structure_id = Rec[1]
        filename = self.hD + r'\Records\PDB/' + str(self.Rec[0][0])
        self.activeDraw.Plugin().Draw(self, filename)
        self.plotter.resize([2.9 / 225., 2.75 / 220.])

    def OnBtnHit(self, event):
        Btn = event.GetEventObject()
        for p in self.pTools.keys():
            if Btn.GetName() == self.pTools[p].GetName():
                PITexec = self.pTools[p].Plugin().GetExec()
        p = subprocess.Popen(PITexec + ' ' + self.hD + r'\Records\PDB/' + str(self.Rec[0][0]))
        p.wait()
    
    def OnDrawBtnHit(self, event):
        Btn = event.GetEventObject()
        for d in self.dTools:
            if Btn.GetName() == d.GetName():
                self.activeDraw = d
        self.plotter.remove()
        self.ax = self.plotter.add('figure 1')
        self.ax2 = self.ax.gca(projection='3d')
        self.ax2.axis('off')
        self.GetExec()

def GetName():
    # Return name of tool
    return '3D Views'

def GetBMP():
    # Return name of tool image
    return r".\Utils\Icons\binocular.bmp"
