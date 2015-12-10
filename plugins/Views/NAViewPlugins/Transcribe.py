class Plugin():
    def GetBackColor(self):
        return "CYAN"

    def GetForeColor(self):
        return "BLACK"
    
    def GetList(self):
        return self.transcribed

    def GetType(self):
        return "Nucleic Acids"

    def GetExec(self, frame, BigPanel, seqRec):
        self.transcribed = GetExec(seqRec)

def GetExec(seqRec):
    return seqRec.transcribe()

def GetName():
    return "Transcribe"
