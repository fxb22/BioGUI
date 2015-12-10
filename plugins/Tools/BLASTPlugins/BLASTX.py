import traceback
import types
import os
import sys

class toolPlugin():
    def GetName(self):
        return "BLASTX"
    
    def GetBMP(self, dirH):
        return dirH + r"\Utils\Icons\BlastX.bmp"
        
    def pluginEXE(self):
        '''Respond to the "blastx" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastx.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "blastx" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastx.exe"
    return plugin_exe

def GetName():
    return "BLASTX"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\BlastX.bmp"
