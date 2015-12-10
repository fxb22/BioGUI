import os
import sys

class Plugin():
    def GetOutFile(self):
        outfile = dirH + r"\plugins\clustal.aln"
        return outfile

    def GetExec(self):
        plugin_exe = r"C:/Program Files (x86)/NCBI/Cn3D 4.1/Cn3D.exe"
        return plugin_exe

def GetExec(self):
    plugin_exe = r"C:/Program Files (x86)/NCBI/Cn3D 4.1/Cn3D.exe"
    return plugin_exe

def GetName():
    '''
    Method to return name of tool
    '''
    return "Cn3D"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\Cn3D.bmp"
    
