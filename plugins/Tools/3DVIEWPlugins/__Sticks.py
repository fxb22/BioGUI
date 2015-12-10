import numpy as np
from Bio.PDB.PDBParser import PDBParser

class Plugin():
    def Draw(self, parent, filename):
        p = PDBParser(PERMISSIVE=1)
        #structure_id = Rec[1]
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
            for resnum,residue in enumerate(chain.get_list()):
                atom = residue.get_list()
                if len(atom) > 3:
                    if resnum > 1:
                        bx[resnum-2].append(npos[0])
                        by[resnum-2].append(npos[1])
                        bz[resnum-2].append(npos[2])                    
                    npos = atom[0].get_coord()
                    capos = atom[1].get_coord()
                    cpos = atom[2].get_coord()
                    opos = atom[3].get_coord()                    
                    rx.append([npos[0],capos[0]])
                    ry.append([npos[1],capos[1]])
                    rz.append([npos[2],capos[2]])
                    bx.append([capos[0],cpos[0]])
                    by.append([capos[1],cpos[1]])
                    bz.append([capos[2],cpos[2]])
                    gx.append([cpos[0],opos[0]])
                    gy.append([cpos[1],opos[1]])
                    gz.append([cpos[2],opos[2]])
        for n,line in enumerate(rx):
            x = np.array(line)
            y = np.array(ry[n])
            z = np.array(rz[n])
            parent.ax2.plot(x,y,z,'r-',linewidth=5)
        for n,line in enumerate(bx):
            x = np.array(line)
            y = np.array(by[n])
            z = np.array(bz[n])
            parent.ax2.plot(x,y,z,'b-',linewidth=5)
        for n,line in enumerate(gx):
            x = np.array(line)
            y = np.array(gy[n])
            z = np.array(gz[n])
            parent.ax2.plot(x,y,z,'g-',linewidth=5)
        
    


def GetName():
    '''
    Method to return name of tool
    '''
    return "Sticks^"

def GetBMP(dirH):
    '''
    Method to return identifying image
    '''
    return dirH + r"\Utils\Icons\sticks.bmp"


    
