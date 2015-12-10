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
        self.ppl=[]
        ge = GetExec(seqRec, frSize)
        i = 0
        while i < len(ge[0]):
            self.ppl.append(wx.StaticText(frame, -1, ge[0][i],
                                          pos = (30, 110 + (20 * i))))
            self.ppl.append(wx.StaticText(frame, -1, ge[1][i],
                                          pos = (115, 110 + (20 * i))))
            i += 1

def GetName():
    # Return name
    return "Statistics"

def GetExec(seqRec, frSize):    
    # Calculate protParamData
    pa = ProtParam.ProteinAnalysis(str(seqRec))
    d = Decimal(10) ** -2
    flexList = pa.flexibility()
    lenf = len(flexList) * 1.
    flexSum = 0
    for f in flexList:
        flexSum += f
    retMat = [[],[]]        
    retMat[0].append("Mol. Weight:")
    retMat[1].append(str(Decimal(pa.molecular_weight()).quantize(d)))
    retMat[0].append("Aromaticity:")
    retMat[1].append(str(Decimal(pa.aromaticity()).quantize(d)))
    retMat[0].append("Instability:")
    retMat[1].append(str(Decimal(pa.instability_index()).quantize(d)))
    retMat[0].append("Avg. Flexibility:")
    retMat[1].append(str(Decimal(flexSum/lenf/1.).quantize(d)))
    retMat[0].append("pI:")
    retMat[1].append(str(Decimal(pa.isoelectric_point()).quantize(d)))
    #retMat[0].append("Avg. Hydropathy:")
    #retMat[1].append(
    #    str(Decimal(pa.protein_scale(ProtParamData.kd,lenf,1)[0]).quantize(d)))
    return retMat
