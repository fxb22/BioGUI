import wx
import math
from Bio.SeqUtils import ProtParam, ProtParamData
from decimal import Decimal

class Plugin():
    def GetParamList(self):
        # Return protParamData
        return self.ppl
    
    def GetExec(self, frame, BigPanel, seqRec, frSize):
        # Display protParamData
        self.ppl = []
        ge = GetExec(seqRec, frSize)
        xPos = -55
        for i,n in enumerate(ge[0]):
            if i % 7 == 0:
                xPos += 55
            self.ppl.append(wx.StaticText(frame, -1, n + ": " + ge[1][i],
                                          pos=(30 + xPos, 110 + 17 * (i % 7))))

def GetName():
    # Return name
    return "Frequency"

def GetExec(seqRec, frSize):
    # Calculate protParamData
    a = ProtParam.ProteinAnalysis(str(seqRec)).count_amino_acids()
    retMat = [[],[]]
    for b in a.keys():
        retMat[0].append(b)
        retMat[1].append(str(Decimal(a[b]).quantize(0)))
    return retMat
