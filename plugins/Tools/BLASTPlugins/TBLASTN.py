import traceback
import types
import os
import sys



class toolPlugin():
    def GetName(self):
        return "TBLASTN"
    
    def GetBMP(self, dirH):
        return dirH + r"\Utils\Icons\tBlastN.bmp"
        
    def pluginEXE(self):
        '''Respond to the "tblastn" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/tblastn.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "tblastn" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/tblastn.exe"
    return plugin_exe

def GetName():
    return "TBLASTN"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\tBlastN.bmp"
