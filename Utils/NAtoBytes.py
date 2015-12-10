from Bio import SeqIO
import Catche as mP

na=['A','C','G','T','R','Y','S','W','K','M','B','D','H','V','N','.']

a=dict()
alpha=1
for i in na:
    for j in na:
        a[i+j]=alpha
        alpha+=1

seqIORec = SeqIO.read(r'C:\Users\francis\Documents\Monguis\BioGui\Nucleic Acids\NC_003074.gbk','genbank')
trace = 0
outcome = []

while trace < len(seqIORec.seq)-1:
    temp = str(seqIORec.seq[trace:trace+2])
    outcome.append(a[temp])
    trace += 2
if len(seqIORec.seq)%2 == 1:
    temp = str(seqIORec.seq[trace]+'.')
    outcome.append(a[temp])
    trace += 2
mP.spickle('plainseq.pickle',seqIORec.seq)
mP.spickle('modseq.pickle',outcome)
