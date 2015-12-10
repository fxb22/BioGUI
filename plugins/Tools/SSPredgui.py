#Import packages that will be used
#GUI generation Packages
import wx
#Operational Packages
import SysUpdate
import os
import re
import getPlugins as gpi
import MenuToolBarSetup as mtbs
import plotter as mpl
import SSEPlotGenerator as spg

#----------------------------------------------------------------------------

class GuiFrame(wx.Frame):
    def GetName(self):
        #Method to return name of tool
        return 'SSPred'

    def GetBMP(self):
        #Method to return identifying image
        return r".\Utils\Icons\SecStructPred.bmp"

    def OnSize(self, event):
        # Method to respond to window sizing
        self.bPSize = self.GetSize()
        self.panelSQ.Show(False)
        self.panelR.Show(False)
        for b in self.resBoxes.values():
            b.Show(False)
        self.toolButton.Show(False)
        self.toolButton.SetPosition((self.bPSize[0] / 3, 80))
        self.toolButton.SetSize((self.bPSize[0] / 3, 25))
        self.panelSQ.SetSize((self.bPSize[0] - 25,70))
        self.panelSQ.SetPosition((7, 6))
        self.panelR.SetSize((self.bPSize[0] - 25,
                            self.bPSize[1] - 175 - 35 * self.tbOnOff))
        self.panelR.SetPosition((7, 110))
        for b in self.resBoxes.values():
            siz = b.GetSize()
            b.SetSize((self.bPSize[0] - 108, siz[1]))
            b.Show(True)
        self.toolButton.Show(True)
        self.panelSQ.Show(True)
        self.panelR.Show(True)

    def SetQuery(self,seq):
        for s in seq:
            ss = ">" + str(s[0].id) + "\n" + str(s[0].seq)+"\n"
            self.seqInput.write(ss)
        self.rec = seq[0][0]
            
    #----------------------Frame Initialization-----------------
    def HelpExec(self,event):
        # Respond to a type selection
        if self.name == "GOR V":
            self.resBoxes['low'].Show(False)
            ps = self.GetSize()[0] - 108
            yp = self.panelR.GetSize()[1]/3.-32
            newFont = wx.Font(8, wx.FONTFAMILY_MODERN,
                              wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
            self.resBoxes['low'] = wx.TextCtrl(self.panelR, -1, "",
                        size = (ps, yp), pos = (75,yp + 40),
                        style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL)
            self.resBoxes['low'].SetFont(newFont)
        self.name = self.menuBar.GetLabel(event.GetId())
        self.curPlugin = self.plugins[self.name].Plugin()
        self.typeMenu.Check(event.GetId(), True)
        
    def DoProtien (self, event):
        # Respond to the "Peptide" alphabet command.
        self.abet = "AA"

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
        else:
            self.alphaMenu.Check(self.menu_DNA, True)
        
    def DoOpen(self, event):
        # Respond to the "Load" menu command.
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
        for b in self.resBoxes.values():
            b.Show(False)
        a = self.resBoxes['ax'].GetSize()
        self.plotter = mpl.PlotNotebook(self.resBoxes['ax'], pos = (0, 0),
                                        size = (a[0],a[1]))
        if self.rec == []:
            query = self.seqInput.GetValue()
            if not query == "":
                try:
                    q = query.split('>')
                    for seq in q:
                        s = seq.split('\n')
                        seqID = s[0]
                        st = ''
                        for l in s[1:]:
                            st += l                
                        self.rec.append(SeqRecord(st,id=seqID,name=seqID,
                                                  description=seqID))
                except:
                    self.seqInput.clear()
                    self.seqInput.write('Incorrect Formatting')
            else:
                self.seqInput.write('enter alignment!')
        self.plotter.remove()
        self.plugins[self.name].GetExec(self,self.rec)

    def SSEPlot(self, sse):
        self.plotter.Show(False)
        axes1 = spg.SSEPlot(sse, self.plotter)
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.plotter.Show(True)
                 
    def DoAbout(self,event):
        # Respond to the "About" menu command
        info = wx.AboutDialogInfo()
        info.SetDescription(
            "Interface to predict Secondary Structure when given sequence\n"+
            "Capable of running many prediction servers/programs\n\n" +
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
        #self.curPlugin.tbChange(self.tbOnOff)
        
    #----------------------Frame Initialization-----------------
    def VarInit(self):
        # Initialize variables
        self.fileName = ""
        self.name = "Chou Fasman"
        self.abet = "AA"
        self.ccmd = 'choufas'
        self.menuBar = wx.MenuBar()
        self.rec = []
        self.plugins = {}
        self.plugIds= {}
        self.resBoxes = {}
        self.bPSize = self.GetSize()
        self.tbOnOff = 1

    def GetPlugins(self):
        # Method to identify BLAST plugins
        dirt = self.hD + r"\plugins\Tools\SSPredPlugins"
        self.plugins = gpi.GetPlugIns(dirt)
        self.curPlugin = self.plugins[self.name].Plugin()

    def GetColors(self):
        # Acquire coloring options
        if "userColors.py" in os.listdir(r".\Utils"):
            import userColors as uc
            self.colorList = uc.getColors()
        else:
            import defaultColors as dc
            self.colorList = dc.getColors()

    def SetPanels(self):
        self.panelSQ = wx.Panel(self, -1, pos=(7,6),
                                size=(self.bPSize[0] - 25,70),
                                style=wx.BORDER_RAISED)
        self.panelSQ.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
        self.panelR = wx.Panel(self, -1, pos = (7,110), style=wx.BORDER_RAISED,
                             size=(self.bPSize[0] - 25,self.bPSize[1] - 175))
        self.panelR.SetBackgroundColour(
            self.colorList['ToolInterface']['Back'])
                
    def SetViewWindows(self):
        # Create user interface appearance
        self.SetPanels()
        ps = self.GetSize()[0] - 108
        yp = self.panelR.GetSize()[1]/3.-32
        newFont = wx.Font(8, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.seqText = wx.StaticText(self.panelSQ, -1, "Sequences: ", pos=(10,6))
        self.seqText.SetForegroundColour('WHITE')
        self.seqInput = wx.TextCtrl(self.panelSQ, -1,
                        "", size=(ps,40), pos=(75,10),
                        style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.resText = wx.StaticText(self.panelR, -1, "Results: ", pos=(25,10))
        self.resText.SetForegroundColour('WHITE')
        self.resBoxes['top'] = wx.TextCtrl(self.panelR, -1, "",  pos=(75,10),
                        size = (ps - 75, yp),
                        style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL)
        self.resBoxes['low'] = wx.TextCtrl(self.panelR, -1, "",
                        size = (ps - 75, yp), pos=(75, yp+25),
                        style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL)
        wx.CallAfter(self.resBoxes['top'].SetInsertionPoint, 0)
        wx.CallAfter(self.resBoxes['low'].SetInsertionPoint, 0)
        self.resBoxes['top'].SetFont(newFont)
        self.resBoxes['low'].SetFont(newFont)
        self.resBoxes['ax'] = wx.Panel(self.panelR, -1, style=wx.BORDER_RAISED,
                                       size = (ps, yp), pos=(75, 2*yp+40))
        self.resBoxes['ax'].SetBackgroundColour('WHITE')
        
    def SetButtons(self):
        # Create action button
        self.toolButton = wx.Button(self, -1, "PREDICT!",
                                    pos = (self.bPSize[0] / 3,76),
                                    size = (self.bPSize[0] / 3, 25))
        self.toolButton.SetBackgroundColour(
            self.colorList['ToolButton']['Back'])
        self.toolButton.SetForegroundColour(
            self.colorList['ToolButton']['Fore'])
        self.Bind(wx.EVT_BUTTON, self.GetExec, self.toolButton)
        
    def __init__(self, parent, *args, **kwargs):
        # Method to initialize the interface
        wx.Frame.__init__(self, parent, size = (1000, 595),
                          title = 'Secondary Structure Prediction GUI')
        self.parent = parent
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
        mts.DoMenubar("PREDICT!","Predict SSE",False,False,False,False)
        menus = self.menuBar.GetMenus()
        for i,m in enumerate(menus):
            if m[1] == 'Alphabet':
                menus.pop(i)
        self.menuBar.SetMenus(menus)
        self.SetMenuBar(self.menuBar)
        mts.DoToolbar()
        self.SetButtons()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.DoExit)
        self.toolbar.Show(False)
        self.tbOnOff = 0
        self.DoTBOnOff(wx.EVT_IDLE)    

def GetName():
    # Method to return name of tool
    return 'SSPred'

def GetBMP():
    # Method to return identifying image
    return r".\Utils\Icons\SecStructPred.bmp"
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

         
