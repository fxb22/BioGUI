import math
import BGpdbParse

class CirclePlot():
    def GetChainEnds(self):
        return self.chainEnds

    def GetResidues(self):
        return self.residueList

    def GetLinks(self):
        return self.links

    def GetLength(self):
        return self.total_length

    def GetCarbonPos(self):
        return self.alpha_carb_pos
    
    def DistCompare(self):
        for i,pi in enumerate(self.alpha_carb_pos):
            if pi[0] != 'inf':
                for j,pj in enumerate(self.alpha_carb_pos[i+3:]):
                    x = pi[0] - pj[0]
                    y = pi[1] - pj[1]
                    z = pi[2] - pj[2]
                    dist = math.sqrt(x**2 + y**2 + z**2)
                    if dist <= self.frSize:
                        self.links.append([i, i + j + 3, dist])

    def ResInfo(self):
        for chain in self.pdbMat.get_list():
            for residue in chain.get_list():                
                for atom in residue.get_list():
                    if atom.get_name() == 'CA':
                        if atom.get_id()[0][0] not in ["H","W"]:
                            self.total_length += 1
                            self.alpha_carb_pos.append(atom.get_coord())
                            self.residueList.append(residue.get_resname())
            self.chainEnds.append(self.total_length)
            self.total_length += 4
            self.alpha_carb_pos.append([float('inf'),
                                        float('inf'),
                                        float('inf')])
            self.residueList.append('W')

    def Dist_Calc(self, rec, frSize, pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.frSize = frSize
        self.links = []
        self.chainEnds = []
        self.total_length = 0
        self.alpha_carb_pos = []
        self.residueList = []
        self.ResInfo()
        self.DistCompare()

class SecondaryStructure():
    def GetSecLinks(self):
        return self.secLinks

    def GetSSE(self):
        return self.sse
    
    def DSSPSheets(self):
        col = 'g'
        for l in self.sheets:
            lenb = l[1] - l[0]
            if l[2] == -1:
                if col == 0:
                    col = 1
                else:
                    col = 1
            elif l[2] == 0:
                col = 1
            i = -1
            while i < lenb:
                self.colList[l[0]+i] = col
                i += 1
            
        for l in self.sheets:
            lenb = l[1] - l[0]
            if l[2] == -1:
                if col == 1:
                    col = 0
                else:
                    col = 1
            elif l[2] == 0:
                col = 1
            self.sse.append([l[0]-1, l[0]-1+lenb+0.4, col])
        for l in self.links:
            if self.colList[l[0]] >= 0:
                if self.colList[l[1]] >= 0:
                    self.secLinks.append([l[0]+0.3,l[1]+0.3, 0])
                    
    def DSSPHelices(self):
        for a in self.helices:
            n = 0
            while (n+3) < (a[1]-a[0]) and a[0]+n < len(a) - 2:
                self.secLinks.append([a[0] + n + 0.3, a[0] + n + 2 + 0.3, 1])
                self.colList[a[0] + n] = 'r'
                self.colList[a[0] + n + 2] = 'r'
                n += 1

    def LGSheetsOne(self, l, lenb):
        j = 0
        nocol = True
        while j < lenb:
            if self.colList[l[0] + j] == -1:
                j += 1
            else:
                onecol = self.colList[l[0] + j]
                j = lenb
                nocol = False
            if nocol:
                onecol = 1
            if onecol == 1:
                twocol = 0
            else:
                twocol = 1
        k = 0
        while k < lenb:
            self.colList[l[0] + k] = onecol
            self.colList[l[1] - k] = twocol
            k += 1
        
        j = lenb - 1
        while j >= 0:
            self.secLinks.append([l[0]+j+0.3, l[1]-j+0.3, 0])
            j -= 1
        self.sse.append([l[0], l[0] + lenb - 0.4, onecol])
        self.sse.append([l[1] - lenb + 1, l[1] + 0.6, twocol])

    def LGHelices(self, l, lenb):
        if (l[0] + lenb) > l[1]:
            j = 0
            while (j + 2) < lenb:
                self.secLinks.append([l[0]+j+0.3, l[0]+j+2+0.3, 1])
                j += 1
            while lenb > 0:
                del self.links[self.links.index([l[0]+lenb-1, l[1]+lenb-1])]
                if self.colList[l[0]+lenb - 1] == -1:
                    self.colList[l[0] + lenb - 1] = 2
                lenb -=1
        elif (l[0] + lenb) == l[1]:
            j = 0
            while (j + 2) < lenb:
                self.secLinks.append([l[0]+j+0.3, l[0]+j+2+0.3, 2])
                j += 1
            while lenb > 0:
                del self.links[self.links.index([l[0]+lenb-1, l[1]+lenb-1])]
                if self.colList[l[0] + lenb - 1] == -1:
                    self.colList[l[0] + lenb - 1] = 3
                lenb-=1

    def LGSheetsTwo(self, l, lenb):
        j = 0
        nocol = True
        while j <= lenb:
            if self.colList[l[0] + j] == -1:
                j += 1
            else:
                onecol = self.colList[l[0] + j]
                j = lenb + 1
                nocol = False
        if nocol == True:
            onecol = 1 
        if onecol == 1:
            twocol = 1
        else:
            twocol = 0
        k = 0
        while k < lenb:
            self.colList[l[0] + k] = onecol
            self.colList[l[1] + k] = twocol
            k += 1
        j = lenb - 1
        while j >= 0:
            self.secLinks.append([l[0]+j+0.3, l[1]-j+0.3, 0])
            j -= 1
        self.sse.append([l[0], l[0] + lenb - 0.4, onecol])
        self.sse.append([l[1] - lenb + 1, l[1] + 0.6, twocol])

    def DoDSSP(self):
        if len(self.rec) > 2:
            self.rec = [self.rec]
        parser = BGpdbParse.pdbParse()
        parser.parse(self.rec[0])
        self.sheets = parser.sheets()
        self.DSSPSheets()
        self.helices = parser.helices()
        self.DSSPHelices()

    def DoLG(self):
        i = 0
        while i < len(self.links):
            self.links[i] = self.links[i][:2]
            i += 1
        for l in self.links:
            lenb = 0
            while [l[0] + lenb,l[1] - lenb] in self.links:
                lenb += 1
            if lenb >= 4:
                self.LGSheetsOne(l, lenb)
            stopper = True
            lenb = 0
            while [l[0] + lenb, l[1] + lenb] in self.links and l[1] > l[0]:
                lenb += 1
            if lenb >= 3:
                self.LGHelices(l, lenb)
            lenb = 0
            while [l[0] + lenb,l[1] + lenb] in self.links:
                lenb += 1
            if lenb >= 4:
                self.LGSheetsTwo(l, lenb)

    def GetExec(self, rec, frSize, pdbMat, meth):
        self.cp = CirclePlot()
        self.cp.Dist_Calc(rec, frSize, pdbMat)
        self.links = self.cp.GetLinks()
        self.colList = []
        i = 0
        while i < self.cp.GetLength():
            self.colList.append(-1)
            i += 1
        self.secLinks = []
        self.sse = []
        self.rec = rec
        if meth == 1:
            self.DoDSSP()
        elif meth == 0:
            self.DoLG()
