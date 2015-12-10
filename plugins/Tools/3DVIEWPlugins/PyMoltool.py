import os
import sys

class Plugin():
    
    def GetOutFile(self):
        2+2

    def GetExec(self):
        plugin_exe = r"C:/Program Files (x86)/py27/PyMOL/PyMOL.exe"
        return plugin_exe

def GetExec():
    plugin_exe = r"C:/Program Files (x86)/py27/PyMOL/PyMOL.exe"
    return plugin_exe


def GetName():
    '''
    Method to return name of tool
    '''
    return "PyMol"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\PyMOL.bmp"
