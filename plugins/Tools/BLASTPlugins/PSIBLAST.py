import traceback
import types
import os
import sys



class toolPlugin():
    def GetName(self):
        return "PSIBLAST"
    
    def GetBMP(self, dirH):
        return dirH + r"\Utils\Icons\PSIBlast.bmp"
        
    def pluginEXE(self):
        '''Respond to the "psiblast" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/psiblast.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "psiblast" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/psiblast.exe"
    return plugin_exe

def GetName():
    return "PSIBLAST"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\PSIBlast.bmp"
