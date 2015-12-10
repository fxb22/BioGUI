import traceback
import types
import os
import sys



class toolPlugin():
    def GetName(self):
        return "BLASTP"
    
    def GetBMP(self, dirH):
        return dirH + r"\Utils\Icons\BlastP.bmp"
        
    def pluginEXE(self):
        '''Respond to the "blastp" type command.
        '''
        plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastp.exe"
        return plugin_exe

def GetExec():
    '''Stand-alone "blastp" command.
    '''
    plugin_exe = r"C:/Program Files/NCBI/blast-2.2.24+/bin/blastp.exe"
    return plugin_exe

def GetName():
    return "BLASTP"

def GetBMP():
    # Method to return identifying image
    return r"C:\Users\francis\Documents\Monguis\BioGui\Utils\Icons\BlastP.bmp"
