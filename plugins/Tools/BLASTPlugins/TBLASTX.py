import traceback
import types
import os
import sys



class toolPlugin():
            
    def pluginEXE(self):
        '''Respond to the "tblastx" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/tblastx.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "tblastx" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/tblastx.exe"
    return plugin_exe

def GetName():
        return "TBLASTX"
    
def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\tBlastX.bmp"
