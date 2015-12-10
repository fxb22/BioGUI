class Plugin():
    def GetBackColor(self):
        return "YELLOW"

    def GetForeColor(self):
        return "BLACK"
    
    def GetList(self):
        return self.translated

    def GetType(self):
        return "Amino Acids"

    def GetExec(self, frame, BigPanel, seq):
        self.translated = ''
        self.translate = GetExec(seq)
        for t in translate:
            self.translated += ' '+t+' '

def GetExec(seq):
    translate = seq.translate()
    return translate

def GetName():
    return "Translate"


