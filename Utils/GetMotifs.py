import CirclePlotClass as cpc

class GetMotifs():
    def DefineColLists(self):
        self.colList = []
        r = 0
        while r < self.total_length:
            self.colList.append(-1)
            r += 1
        self.sse = self.cpss.GetSSE()
        self.secLinks = self.cpss.GetSecLinks()
        for s in self.sse:
            j = s[0]
            while j < s[1]:
                self.colList[j] = s[2] + 1
                j += 1
        for s in self.secLinks:
            if s[2] > 0:
                j = s[0]
                while j < s[1]:
                    self.colList[int(j)] = 2
                    j += 1
                    
    def CheckSse(self):
        shets = []
        for s in self.sse:
            f = s[0]
            n = s[1]
            c = s[2]
            for e in self.sse:
                if f < e[0]:
                    if n >= e[0]:
                        if n < e[1]:
                            n = e[1]
                if f <= e[1]:
                    if n <= e[1]:
                        if f > e[0]:
                            f = e[0]
            if not [f, n, c] in shets:
                shets.append([f, n, c])
        for s in shets:
            go = True
            for e in shets:
                if s[0] > e[0] and s[0] < e[1]:
                    go = False
                if s[1] > e[0] and s[1] < e[1]:
                    go = False
            if go:
                self.sheets.append(s)

    def CheckSecLinks(self):
        for s in self.secLinks:
            f = -1
            n = -1
            for i,e in enumerate(self.sheets):
                if s[0] >= e[0] and s[0] < e[1]:
                    f = i
                if s[1] > e[0] and s[1] <= e[1]:
                    n = i
            if f >= 0 and n >= 0:
                t = -1
                if self.sheets[f][2] == self.sheets[n][2]:
                    t = 1
                a = [self.sheets[f][:2], self.sheets[n][:2], t]
                if not a in self.motif:
                    if not a[0] == a[1]:
                        self.motif.append(a)
            if s[2] == 1:
                self.helices.append(s[0])

    def FormMotifs(self):
        self.motif = []
        self.helices = []
        self.sheets = []
        self.CheckSse()
        self.CheckSecLinks()

    def FormFrequencies(self, order):
        freqs = dict()
        for o in order:
            if not o[0][0] in freqs:
                freqs[o[0][0]] = 1
            else:
                freqs[o[0][0]] += 1
            if not o[1][0] in freqs:
                freqs[o[1][0]] = 1
            else:
                freqs[o[1][0]] += 1
        return freqs

    def FindMotif(self, n):
        i = 0
        out = [-1,[[n,-1],[-1,-1],-1]]
        while i < len(self.motif):
            if self.motif[i][0][0] == n:
                out = [i,self.motif[i]]
                self.motif.pop(i)
                i = len(self.motif)
            elif self.motif[i][1][0] == n:
                out = [i,[self.motif[i][1],self.motif[i][0],self.motif[i][2]]]
                self.motif.pop(i)
                i = len(self.motif)
            i += 1
        return out

    def FormGuess(self, freqs):
        self.orders = []
        fk = freqs.keys()
        i = 0
        while i < len(fk):
            if freqs[fk[i]] == 1:
                freqs[fk[i]] -= 1
                m = self.FindMotif(fk[i])
                self.orders.append([[m[1][0],1]])
                prevDir = 1
                while m[1][1][0] >= 0 and freqs[m[1][1][0]] >= 1:
                    prevDir = m[1][2]
                    self.orders[-1].append([m[1][1], m[1][2]])
                    freqs[m[1][0][0]] -= 1
                    m = self.FindMotif(m[1][1][0])
                    freqs[m[1][0][0]] -= 1
                i = -1
                if self.orders[-1][-1][0][0]<self.orders[-1][0][0][0]:
                    temp = []
                    temp.append([self.orders[-1][-1][0],1])
                    idk = 1
                    while idk<len(self.orders[-1]):
                        temp.append([self.orders[-1][-idk-1][0],
                                     self.orders[-1][-idk][1]])
                        idk += 1
                    self.orders[-1] = temp
            elif i == len(fk) - 1:
                if freqs[fk[0]] > 1:
                    freqs[fk[0]] -= 1
                    i = -1
            i += 1

    def MotifFolds(self):
        self.FormMotifs()
        freqs = self.FormFrequencies(self.motif)
        self.FormGuess(freqs)

    def GetExec(self, rec, frSize, pdbMat, meth):
        self.cpss = cpc.SecondaryStructure()
        self.cpss.GetExec(rec, frSize, pdbMat, meth)
        self.alpha_carb_pos = self.cpss.cp.GetCarbonPos()
        self.chainEnds = self.cpss.cp.GetChainEnds()
        self.total_length = self.cpss.cp.GetLength()
        self.residueList = self.cpss.cp.GetResidues()
        self.DefineColLists()
        self.MotifFolds()
        return [[self.orders], self.helices, self.secLinks]
