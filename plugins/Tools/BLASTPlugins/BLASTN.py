import traceback
import types
import os
import sys

class toolPlugin():
    def GetName(self):
        return "BLASTN"
    
    def GetBMP(self, dirH):
        return dirH + r"\Utils\Icons\BlastN.bmp"
        
    def pluginEXE(self):
        '''Respond to the "blastn" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastn.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "blastn" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastn.exe"
    return plugin_exe


def GetName():
    return "BLASTN"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\BlastN.bmp"
