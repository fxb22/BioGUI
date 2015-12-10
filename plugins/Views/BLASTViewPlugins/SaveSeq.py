from Bio import SeqIO
from Bio.Alphabet import generic_alphabet
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from time import strftime

class Plugin():
    def GetFileName(self):
        # Return file name
        return self.fn

    def GetExec(self, info, bp, hd, bral, brap):
        try:
            seqs = info[1]
            seqList = []
            d = strftime('%d%m%y%H%M')
            for i,n in enumerate(info[2]):
                seqList.append(SeqRecord(Seq(seqs[i], generic_alphabet),id = n))
                alignment = bral[0]
                q = alignment.title.split('|')
                if brap in ['BLASTN', 'TBLASTN', 'TBLASTX']:
                    self.fn = hd+r"\Nucleic Acids/"+q[0]+'_'+q[1]+'_'+d+'.fasta'
                else:
                    self.fn = hd+r"\Amino Acids/"+q[0]+'_'+q[1]+'_'+d+'.fasta'
                SeqIO.write(seqList, self.fn, "fasta")
        except: print 'oops'

def GetName():
    # Return name
    return "Save Sequence"

def GetColors():
    # Return string identifying object of coloring
    return 'ViewButton'

def GetExec(info, bral, brap):
    info = Info()
    try:
        seqs = info[1]
        seqList = []
        d = strftime('%d%m%y%H%M')
        for i,n in enumerate(info[2]):
            seqList.append(SeqRecord(Seq(seqs[i], generic_alphabet),id = n))
            alignment = bral[0]
            q = alignment.title.split('|')
            bra = self.BlastRec.application
            if bra in ['BLASTN', 'TBLASTN', 'TBLASTX']:
                fn = r".\Nucleic Acids/"+q[0]+'_'+q[1]+'_'+d+'.fasta'
            else:
                fn = r".\Amino Acids/"+q[0]+'_'+q[1]+'_'+d+'.fasta'
            SeqIO.write(seqList,fn,"fasta")
    except: print 'oops'
    return fn
