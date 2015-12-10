from Bio import AlignIO
from Bio.Alphabet import generic_alphabet
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from time import strftime

class Plugin():
    def GetFileName(self):
        # Return file name
        return self.fn

    def GetExec(self, info, bp, hd, bral, brap):
        t = []
        for i,n in enumerate(info[1]):
            t.append(SeqRecord(Seq(n, generic_alphabet), id = info[2][i]))
        d = strftime('%d%m%y%H%M')
        self.fn = r".\Alignments/"+brap+"align"+d+".fasta"
        AlignIO.write(MultipleSeqAlignment(t), self.fn, "fasta")

def GetName():
    # Return name
    return "Save Alignment"

def GetColors():
    # Return string identifying object of coloring
    return 'ViewPanelButton'

def GetExec(info, bral, brap):
    t = []
    for i,n in enumerate(info[1]):
        t.append(SeqRecord(Seq(n, generic_alphabet), id = info[2][i]))
    d = strftime('%d%m%y%H%M')
    self.fn = r".\Alignments/"+brap+"align"+d+".fasta"
    AlignIO.write(MultipleSeqAlignment(t), self.fn, "fasta")
    return ''
