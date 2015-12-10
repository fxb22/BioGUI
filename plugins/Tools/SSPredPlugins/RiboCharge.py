import wx

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "RiboCharge"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\RiboCharge.bmp"
    
    def GettopFile(self):
        self.topfile = dirH + r"\plugins\clustal.aln"
        return self.topfile

    def GetFinal(self):
        return self.final

    def SetChargeDict(self):
        # Define charges. hydrophobic: 0, hydrophilic: 1, charged: 2
        # Treat glycine and proline differently
        # Serine and Threonine behave differently
        # Consider Cystine as unique
        # Handle Uncommon residues
        self.chargeDict = {'A':'0','V':'0','L':'0','I':'0','M':'0',
                           'F':'0','W':'0','J':'0','Y':'0',
                           'S':'S','T':'T',
                           'C':'7',
                           'N':'1','Q':'1',
                           'K':'2','R':'2','H':'2','D':'2','E':'2',
                           'P':'0','G':'3',
                           'B':'0','Z':'0','X':'9'}    

    def InitVars(self):
        self.charge = ''
        self.turn = ''
        self.sheet = '.'
        self.helix = '..'
        self.final = ''
        for q in self.query:
            self.charge += self.chargeDict[q]

    def FindTurns(self):
        pos = 0
        while pos < len(self.query) - 4:
            l = -3
            sumNon = 0
            while l < 3:
                if not self.charge[pos + l] in ['1','0']:
                    sumNon += 1
                    if self.query[pos + l] == 'G':
                        sumNon += 1
                elif self.query[pos + l] == 'P':
                    sumNon += 1
                l += 1
            if sumNon >= 4:
                self.turn += 'X'
            else:
                self.turn += '.'
            pos += 1
        self.turn = self.turn[:-2]+'.'
        while len(self.turn) < len(self.query):
            self.turn += '.'

    def FindSheets(self):
        i = 1
        prev = False
        while i < len(self.charge) - 4:
            l = -3
            sumNon = 0
            while l < 3:
                if self.charge[i + l] in ['1','0','S']:
                    sumNon += 1
                l += 1
            if prev:
                if sumNon >= 3:
                    self.sheet += 'E'
                else:
                    self.sheet += '.'
                    prev = False
            elif sumNon >= 4:
                self.sheet += 'E'
                prev = True
            else:
                self.sheet += '.'
                prev = False
            i += 1
        while len(self.sheet) < len(self.query):
            self.sheet += '.'

    def FindHelices(self):
        i = 2
        while i<len(self.query) - 6:
            l = -3
            sumNon = 0
            sumCha = 0
            sumBad = 0
            while l < 3:
                if self.charge[i + l] in ['1','0','T']:
                    sumNon += 1
                elif self.charge[i + l] == '2':
                    sumCha += 1
                else:
                    sumBad += 1                    
                l += 1
            if sumBad < 3:
                if sumNon > 4:
                    self.helix = self.helix[:-1] + 'HH'
                elif sumCha >= 2:
                    self.helix = self.helix[:-1] + 'HH'
                else:
                    self.helix += '.'
            else:
                self.helix += '.'
            i += 1
        while len(self.helix) < len(self.query):
            self.helix += '.'
        
    def AdjustBoxes(self):
        self.parent.resBoxes['top'].Clear()
        self.parent.resBoxes['low'].Clear()
        for v in self.parent.resBoxes.values():
            v.Show(True)

    def WriteBoxes(self):
        self.parent.resBoxes['top'].write('Initial:\n'+str(self.query))
        self.parent.resBoxes['low'].write('Final:\n')
        self.parent.resBoxes['top'].write('\n')
        for t in self.turn:
            self.parent.resBoxes['top'].write(t)
        self.parent.resBoxes['top'].write('\n')
        for e in self.sheet:
            self.parent.resBoxes['top'].write(e)
        self.parent.resBoxes['top'].write('\n')
        self.final = ''
        for i,h in enumerate(self.helix):
            self.parent.resBoxes['top'].write(h)
            if h == 'H':
                self.final += 'H'
            else:
                self.final += str(self.sheet[i])
        self.parent.resBoxes['low'].write(str(self.final))
        self.parent.resBoxes['low'].write('\n')

    def SmoothFinal(self):
        for i,h in enumerate(self.helix):
            if not self.turn[i] == 'X':
                if h == 'H':
                    self.final += 'H'
                else:
                    self.final += str(self.sheet[i])
            else:
                self.final += '.'
        i = 2
        while i < len(self.final):
            if self.final[i] == '.':
                if not self.final[i-1] == '.':
                    if self.final[i-1] == self.final[i+1]:
                        self.final=self.final[:i]+self.final[i-1]+self.final[i+1:]
                    elif self.final[i-1:i+2] == 'H..H':
                        self.final = self.final[:i] + 'HH' + self.final[i+2:]
            i += 1
        i = 2
        while i < len(self.final):
            run = 0
            while i < len(self.final) and self.final[i] == 'H':
                run += 1
                i += 1
            if run > 0 and not '2' in self.charge[i-run:i]:
                t = ''
                while run >= 0:
                    t += 'E'
                    run -= 1
                self.final = self.final[:i-len(t)]+t+self.final[i:]
            i += 1
        i = 2
        run = 0
        while i < len(self.final):
            while i < len(self.final) and self.final[i] == self.final[i-1]:
                run += 1
                i += 1
            t = ''
            if self.final[i - 1] == 'E' and run <= 1:
                while run >= 0:
                    t += '.'
                    run -= 1
                self.final = self.final[:i-len(t)]+t+self.final[i:]
                i -= 1
            elif run <= 2 and self.final[i - 1] == 'H':
                while run >= 0:
                    t += '.'
                    run -= 1
                self.final = self.final[:i-len(t)]+t+self.final[i:]
                i -= 1
            i += 1
            run = 0

    def GetExec(self,parent,query):
        self.parent = parent
        self.query = query#.seq
        self.SetChargeDict()
        self.InitVars()
        self.FindTurns()
        self.FindSheets()
        self.FindHelices()
        self.SmoothFinal()
        if not parent == None:
            self.AdjustBoxes()
            self.WriteBoxes()
            self.parent.SSEPlot(self.final)
           
def GetExec(query):
    a = Plugin()
    a.GetExec(None, query)
    return a.GetFinal()
    

def GetName():
    #Method to return name of tool
    return "RiboCharge"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\RiboCharge.bmp"
