import wx

class Plugin():
    def GetName(self):
        #Method to return name of tool
        return "Chou Fasman"
    
    def GetBMP(self, dirH):
        #Method to return identifying image
        return dirH + r"\Utils\Icons\choufasman.bmp"
    
    def GetOutFile(self):
        self.self.outfile=dirH + r"\plugins\clustal.aln"
        return self.self.outfile

    def GetTable(self):
        # The Chou-Fasman table, with rows of the table indexed by AA name.
        #   Data copied, pasted, and reformatted from 
        #     http://prowl.rockefeller.edu/aainfo/chou.htm
        # Columns are SYM,P(a), P(b),P(turn), f(i),   f(i+1), f(i+2), f(i+3)
        self.CF = {}
        self.CF['A'] = [142,  83,   66,   0.06,   0.076,  0.035,  0.058]
        self.CF['R'] = [98,   93,   95,   0.070,  0.106,  0.099,  0.085]
        self.CF['D'] = [101,  54,  146,   0.147,  0.110,  0.179,  0.081]
        self.CF['N'] = [67,   89,  156,   0.161,  0.083,  0.191,  0.091]
        self.CF['C'] = [70,  119,  119,   0.149,  0.050,  0.117,  0.128]
        self.CF['E'] = [151,  37,   74,   0.056,  0.060,  0.077,  0.064]
        self.CF['Q'] = [111, 110,   98,   0.074,  0.098,  0.037,  0.098]
        self.CF['G'] = [57,   75,  156,   0.102,  0.085,  0.190,  0.152]
        self.CF['H'] = [100,  87,   95,   0.140,  0.047,  0.093,  0.054]
        self.CF['I'] = [108, 160,   47,   0.043,  0.034,  0.013,  0.056]
        self.CF['L'] = [121, 130,   59,   0.061,  0.025,  0.036,  0.070]
        self.CF['K'] = [114,  74,  101,   0.055,  0.115,  0.072,  0.095]
        self.CF['M'] = [145, 105,   60,   0.068,  0.082,  0.014,  0.055]
        self.CF['F'] = [113, 138,   60,   0.059,  0.041,  0.065,  0.065]
        self.CF['P'] = [57,   55,  152,   0.102,  0.301,  0.034,  0.068]
        self.CF['S'] = [77,   75,  143,   0.120,  0.139,  0.125,  0.106]
        self.CF['T'] = [83,  119,   96,   0.086,  0.108,  0.065,  0.079]
        self.CF['W'] = [108, 137,   96,   0.077,  0.013,  0.064,  0.167]
        self.CF['Y'] = [69,  147,  114,   0.082,  0.065,  0.114,  0.125]
        self.CF['V'] = [106, 170,   50,   0.062,  0.048,  0.028,  0.053]
        self.Res={}
        self.Res['H'] = ['E','M','A','L','K','F','Q','W','I','V']
        self.Res['E'] = ['V','I','Y','F','W','L','C','T','Q','M']

    def CountRes(self,seq,char):
        count = 0
        i = 0
        while i < len(seq):
            if seq[i] in self.Res[char]:
                count += 1
            i += 1
        return char

    def TestHelix(self, seq):
        self.Hel = ''
        for i,s in enumerate(seq):
            if s in self.Res['H'] and self.CountRes(seq[i:i+6],'H') >= 4:
                self.Hel += 'H'
            else:
                self.Hel += '.'
        temp = ''
        for i,s in enumerate(seq):
            count = 0
            for d in self.Hel[i-2:i+4]:
                if d == 'H':
                    count += 1
            if count >= 3:
                temp += 'H'
            else:
                temp += '.'
        tem = ''
        for i,t in enumerate(temp[:-1]):
            if t == '.' and temp[i+1] == 'H' and self.Hel[i] == 'H':
                tem += 'H'
            else:
                tem += temp[i]
        self.Hel = ''
        i = 0
        while i < len(seq):
            count = 0
            while i<len(tem) and tem[i] == 'H':
                i += 1
                count += 1
            if count >= 5:
                c = 'H'
            else:
                c = '.'
            while count > 0:
                self.Hel += c
                count -= 1
            self.Hel += '.'
            i += 1

    def TestSheet(self, seq):
        self.She = ''
        for i,s in enumerate(seq):
            if s in self.Res['E'] and self.CountRes(seq[i:i+5],'E') >= 3:
                self.She += 'E'
            else:
                self.She += '.'
        temp = ''
        for i,s in enumerate(seq):
            count = 0
            for d in self.She[i-2:i+3]:
                if d == 'E':
                    count += 1
            if count >= 3:
                temp += 'E'
            else:
                temp += '.'
        i = 0
        tem = ''
        for i,t in enumerate(temp[:-1]):
            if t == '.' and temp[i+1] == 'E' and self.She[i] == 'E':
                tem += 'E'
            else:
                tem += t
        self.She = ''
        i = 0
        while i < len(seq):
            count = 0
            while i<len(tem) and tem[i] == 'E' :
                i += 1
                count += 1
            if count >= 4:
                c = 'E'
            else:
                c = '.'
            while count > 0:
                self.She += c
                count -= 1
            i += 1
            self.She += '.'

    def SetFinal(self,seq):
        self.final = '.'
        i = 1
        while i < len(self.She) - 1:
            avg = 0
            avb = 0
            j = -1
            while j < 2:
                avg += self.CF[seq[i+j]][0]
                avb += self.CF[seq[i+j]][1]
                j += 1
            if self.Hel[i] == 'H':
                if self.She[i] == 'E':
                    if avg >= avb:
                        self.final += 'H'
                    else:
                        self.final += 'E'
                else:
                    self.final += 'H'
            elif self.She[i] == 'E':
                self.final += self.She[i]
            else:
                self.final += '.'
            i += 1
        self.final += '.'

    def WriteBoxes(self, parent, seq):
        for v in self.parent.resBoxes.values():
            v.Show(True)
        parent.resBoxes['top'].write('query:\n'+str(seq))
        parent.resBoxes['low'].write('\nstates:\n')
        i = 0
        tens = ''
        while i < len(seq):
            if i%10 == 9:
                tens += '*'
            else:
                tens += ' '
            i += 1
        parent.resBoxes['low'].write(self.Hel+'\n')
        parent.resBoxes['low'].write(self.She+'\n')
        wx.CallAfter(parent.resBoxes['top'].SetInsertionPoint, 0)
        self.SetFinal(seq)
        parent.resBoxes['low'].write('final:\n'+str(self.final))
        parent.resBoxes['low'].write('\n')
        parent.SSEPlot(self.final)

    def GetExec(self,parent,query):
        self.parent = parent
        self.out = ['','','']
        seq = query.seq
        self.GetTable()
        self.TestHelix(seq)
        self.TestSheet(seq)
        if parent == None:
            return self.out
        else:
            self.out[0] = self.Hel
            self.out[1] = self.She
            self.WriteBoxes(parent, seq)
            
            
def GetExec(seq):
    a = Plugin()
    return a.GetExec(None,seq)

def GetName():
    #Method to return name of tool
    return "Chou Fasman"

def GetBMP():
    #Method to return identifying image
    return r".\Utils\Icons\choufasman.bmp"
