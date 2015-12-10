# Parser for secondary structure information contained in PDB files.
# Identifies HELIX, SHEET, and SSBOND headings.

import re

class pdbParse():
    def helices(self):
        return self.helix

    def sheets(self):
        return self.sheet

    def cbonds(self):
        return self.ssbond

    def parse(self,filename):
        self.helix = []
        self.sheet = []
        self. ssbond = []
        linfo = []
        pdb = open(filename)
        lines = pdb.read().split('\n')
        i = 0
        while i < len(lines):
            if lines[i][:5] == 'HELIX':
                l = lines[i]
                linfo = [int(re.sub(' ','',l[21:25])),
                         int(re.sub(' ','',l[33:37]))]
                self.helix.append(linfo)
            elif lines[i][:5] == 'SHEET':
                l = lines[i]
                linfo = [int(re.sub(' ','',l[22:26])),
                         int(re.sub(' ','',l[33:37])),
                         int(re.sub(' ','',l[38:40]))]
                self.sheet.append(linfo)
            elif lines[i][:6] == 'SSBOND':
                l = lines[i]
                linfo = [int(re.sub(' ','',l[17:21])),
                         int(re.sub(' ','',l[31:35]))]
                self.ssbond.append(linfo)
            elif lines[i][:5] == 'MODEL':
                i = len(lines)
            i += 1
            
            
