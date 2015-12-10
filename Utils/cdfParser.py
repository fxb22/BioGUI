class cdfParse():
    def getProbeSets(self):
        return self.probeSetIDs

    def getPropeLocs(self):
        return self.probeLocs

    def getProbeNumber(self):
        return len(self.probeSetIDs)

    def getPMLocs(self):
        i = 0
        self.PMLocs = []
        while i < len(self.probeLocs):
            colPos1 = self.probeLocs[i][1]
            colPos2 = self.probeLocs[i+1][1]
            if colPos1 > colPos2:
                self.PMLocs.append(self.probeLocs[i+1])
            else:
                self.PMLocs.append(self.probeLocs[i])
            i += 2
        return self.PMLocs
    
    def parse(self,cdfPath):
        cdfFile = open(cdfPath)
        self.affyName = ''
        nameLess = True
        goVar = True
        self.probeSetIDs = []
        self.probeLocs = []
        tracker = 1
        endUnit = 1
        pmNum = 0
        while nameLess:
            line = cdfFile.readline()
            if line[:4] == r'Name':
                self.affyName = line[5:]
                
            if line[:8] == r'MaxUnit=':
                endUnit = line[8:-1]
                nameLess = False

        while goVar:
            line = cdfFile.readline()
            if len(line) > 0:
                if r'_B' in line:
                    psID = cdfFile.readline()[5:-1]
                    cdfFile.readline()
                    pmNum += int(cdfFile.readline()[9:-1])
                    self.probeSetIDs.append([psID,pmNum])
                    stopper = True
                    cellNum = 1
                    while stopper:
                        
                        unitLine = cdfFile.readline()
                        pos = 5 + len(str(cellNum))
                        #print unitLine[:pos]
                        #print (r'Cell'+ str(cellNum) + r'=')
                        if unitLine[:pos] == str(r'Cell'+ str(cellNum) + r'='):
                            xStr = ''
                            yStr = ''
                            while unitLine[pos] != '\t':
                                xStr += str(unitLine[pos])
                                pos += 1
                            pos += 1
                            while unitLine[pos] != '\t':
                                yStr += str(unitLine[pos])
                                pos += 1
                            #print pos
                            #print [xStr,yStr]
                            self.probeLocs.append([int(xStr), int(yStr)])
                            cellNum += 1
                            #print self.probeLocs[-1]
                        elif unitLine == '\n':
                            #print tracker
                            stopper = False
                    tracker += 1        
                elif line == '\n' and tracker == endUnit:
                    goVar = False
            else:
                goVar = False

