import os
import sys

class Plugin():
    def GetOutFile(self):
        outfile = dirH + r"\plugins\clustal.aln"
        return outfile

    def GetExec(self):
        plugin_exe = r"C:/Program Files (x86)/RasWin/raswin.exe"
        return plugin_exe

def GetExec():
    plugin_exe = r"C:/Program Files (x86)/RasWin/raswin.exe"
    return plugin_exe

def GetName():
    '''
    Method to return name of tool
    '''
    return "RasWin"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\raswin.bmp"
    
