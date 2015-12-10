import sys
import wx
import os
import errno
import time
import math
from wx.lib.buttons import GenBitmapButton,GenBitmapToggleButton
import  wx.lib.mixins.listctrl  as  listmix
from Bio import SeqIO
from Bio.SeqUtils import ProtParam, ProtParamData
from decimal import Decimal
import  wx.lib.filebrowsebutton as filebrowse



class addToolDialog(wx.Dialog):
    """ A dialog window showing the options of the alignment tools"""

    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================

    def __init__(self, parent, title, homeDir, fileName=None):
        """ Standard constructor.

            'parent', 'id' and 'title' are all passed to the standard wx.Frame
            constructor.  'fileName' is the name and path of a saved file to
            load into this frame, if any.
        """
        wx.Dialog.__init__(self, parent, title='title', size=(500, 600))

        self.statToolName = wx.StaticText(self, -1, "Name of New Tool", size=(100,-1), pos=(50,50))
        self.textToolName = wx.TextCtrl(self, -1, "", size=(300,-1), pos=(50,75))

        self.newToolIconButton = filebrowse.DirBrowseButton(parent=self, id=-1,pos=wx.Point(50,100), size=(400,50), labelText="Select icon\nfor new tool")
        self.newToolIconButton.SetValue(homeDir + r"\Utils\Icons\Default")

        self.newToolLocButton = filebrowse.DirBrowseButton(parent=self, id=-1,pos=wx.Point(50,150), size=(400,50), labelText="Select location\nof original script")

        self.statToolClass = wx.StaticText(self, -1, "What class(es) are used with the tool?", size=(350,-1), pos=(50,200))
        self.textToolClass = wx.TextCtrl(self, -1, "", size=(350,-1), pos=(50,225))

        self.statToolInput = wx.StaticText(self, -1, "What inputs does this class recognize?", size=(350,-1), pos=(50,250))
        self.textToolInput = wx.TextCtrl(self, -1, "", size=(350,-1), pos=(50,275))
        
        addToolButton = wx.Button(self, -1, "Create", pos=(300,325))
        addToolButton.SetBackgroundColour('RED')
        addToolButton.SetForegroundColour('WHITE')
        self.Bind(wx.EVT_BUTTON, self.doCreate, addToolButton)

    def doCreate(self,event):
        newFile=0
