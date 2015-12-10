import numpy as np
from Bio.PDB.PDBParser import PDBParser

class Plugin():
    def Draw(self, parent, filename):
        p = PDBParser(PERMISSIVE=1)
        #structure_id = Rec[1]
        structure = p.get_structure('WHYY', filename)
        self.pdbMat = structure.get_list()
        x = []
        y = []
        z = []
        for chain in self.pdbMat[0].get_list():
            for residue in chain.get_list():
                for atom in residue.get_list():
                    if atom.get_name() == 'CA':
                        pos = atom.get_coord()
                        x.append(pos[0])
                        y.append(pos[1])
                        z.append(pos[2])
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        parent.ax2.plot(x,y,z)
        
def GetName():
    '''
    Method to return name of tool
    '''
    return "Ribbon^"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\StringLine.bmp"
