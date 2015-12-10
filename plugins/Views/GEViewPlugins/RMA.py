import os
import Catche
import subprocess


class Plugin():
    def GetParamList(self):
        return self.geoMat

    def GetName(self):
        return "RMA"

    def GetExec(self, frame, BigPanel, Rec, lenX, colorList):
        pluginEXE(Rec, lenX)
        self.geoMat = Catche.opickle(r'.\GeneExpressions\CurrentCel\RMAFinal.pickle')
        return self.geoMat


def pluginEXE(Rec, lenX):
    outdir = os.getcwd()
    p = subprocess.Popen(r'C:\Program Files (x86)\py27\python.exe ',+outdir+r'\Utils\RMAAdjust.py')
    p.wait()
    p = subprocess.Popen(r'C:\Program Files (x86)\py27\python.exe ',+outdir+r'\Utils\quantileNormalize.py')
    p.wait()
    p = subprocess.Popen(r'C:\Program Files (x86)\py27\python.exe ',+outdir+r'\Utils\RMASum.py')
    p.wait()

def GetName():
    return "RMA"

