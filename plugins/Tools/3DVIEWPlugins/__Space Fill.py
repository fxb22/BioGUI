import numpy as np
from Bio.PDB.PDBParser import PDBParser

class Plugin():
    def Draw(self, parent, filename):
        p = PDBParser(PERMISSIVE=1)
        structure = p.get_structure('WHYY', filename)
        self.pdbMat = structure.get_list()
        rx = []
        ry = []
        rz = []
        bx = []
        by = []
        bz = []
        gx = []
        gy = []
        gz = []
        for chain in self.pdbMat[0].get_list():
            for residue in chain.get_list():
                for atom in residue.get_list():
                    if atom.get_id()[0][0] not in ["H","W"]:
                        pos = atom.get_coord()
                        if atom.get_name() == 'CA':
                            bx.append(pos[0])
                            by.append(pos[1])
                            bz.append(pos[2])
                        elif atom.get_name() == 'N':
                            rx.append(pos[0])
                            ry.append(pos[1])
                            rz.append(pos[2])
                        elif atom.get_name() == 'O':
                            gx.append(pos[0])
                            gy.append(pos[1])
                            gz.append(pos[2])
        x = np.array(bx)
        y = np.array(by)
        z = np.array(bz)
        parent.ax2.scatter(x, y, z,  zdir='z', marker='o', s=385, c='b')            #385 is the radius of carbon times 5
        x = np.array(rx)
        y = np.array(ry)
        z = np.array(rz)
        parent.ax2.scatter(x, y, z,  zdir='z', marker='o', s=350, c='r')            #350 is the radius of Nitrogen times 5
        x = np.array(gx)
        y = np.array(gy)
        z = np.array(gz)
        parent.ax2.scatter(x, y, z,  zdir='z', marker='o', s=330, c='g')            #330 is the radius of oxygen times 5

def GetName():
    '''
    Method to return name of tool
    '''
    return "Space Fill^"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\ballspace.bmp"

        
    

