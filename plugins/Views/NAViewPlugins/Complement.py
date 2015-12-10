class Plugin():
    def GetBackColor(self):
        return "#FF9966"

    def GetForeColor(self):
        return "BLACK"
    
    def GetList(self):
        return self.complement

    def GetType(self):
        return "Nucleic Acids"

    def GetExec(self, frame, BigPanel, seqRec):
        self.complement = GetExec(seqRec)

def GetName():
    return "Complement"

def GetExec(seqRec):
    return seqRec.complement()
