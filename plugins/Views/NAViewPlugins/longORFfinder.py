class Plugin():
    def GetBackColor(self):
        return "RED"

    def GetForeColor(self):
        return "White"
    
    def GetList(self):
        return self.longORF

    def GetType(self):
        return "Nucleic Acids"

    def GetExec(self, frame, BigPanel, seqRec):
        stopCodons = ['TAA','TAG','TGA']
        i = 0
        curOrf = 0
        longOrf = 0
        orfStart = 0
        self.longORF = ''
        while i < 3:
            j = i
            while j < len(seqRec)-2:
                if str(seqRec[j:j+3]) in stopCodons:
                    if curOrf > longOrf:
                        orfStart = j - 3 * curOrf
                        longOrf = curOrf + 1
                    curOrf = 0
                else:
                    curOrf += 1
                j += 3
            if curOrf > longOrf:
                orfStart = j - 3 * curOrf
                longOrf = curOrf
            i += 1
        i = 0
        while i < orfStart:
            self.longORF += ' '
            i += 1
        self.longORF += seqRec[orfStart:(orfStart + longOrf * 3)]
        i = (orfStart + longOrf * 3)
        while i < len(seqRec):
            self.longORF += ' '
            i += 1

def GetName():
    return "Long ORF"


   
