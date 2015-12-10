import math
import subprocess

class tTestClass():
    def __init__(self):
        self.sumMat = []
        self.varMat = []
        self.sigMat = []
        self.sumMatEx = []
        self.varMatEx = []
        self.tscoreMat = []
        self.degfree = []
        self.pMat = []
        self.tcdFile = r"C:\Users\francis\Documents\Monguis\BioGui\Utils\tcditest.txt"
        self.tcdoFile = r"C:\Users\francis\Documents\Monguis\BioGui\Utils\tcdotest.txt"
        self.bitFprint = ''

    def GetTScores(self):
        return self.tscoreMat

    def GetDof(self):
        return self.degfree

    def GetPMat(self):
        return self.pMat

    def Update(self):
        for x in self.geMat[1][1:]:
            self.sumMat.append(0.)
            self.varMat.append(0.)
            self.sumMatEx.append(0.)
            self.varMatEx.append(0.)
            self.tscoreMat.append(0.)
            self.degfree.append(0.)
            self.pMat.append(0.)
        for row in self.geMat[:-1]:
            for i, v in enumerate(row[1:]):
                if row[0] in self.rec[0]:
                    self.sumMat[i] += float(v)
                else:
                    self.sumMatEx[i] += float(v)
        for row in self.geMat[:-1]:
            for i, v in enumerate(row[1:]):
                if row[0] in self.rec[0]:
                    self.varMat[i]+=(float(v)-self.sumMat[i]/self.n1)**2
                else:
                    self.varMatEx[i]+=(float(v)-self.sumMatEx[i]/self.n2)**2

    def Sizes(self):
        self.n1 = float(len(self.rec[0])-1.)
        self.n2 = float(len(self.geMat) - self.n1)
        if self.n1 < 2:
            self.n1 = 2.
        if len(self.rec[0]) > 2 and len(self.rec[0]) < len(self.geMat) - 2:
            self.n1 = float(len(self.rec[0]))
            self.n2 = float(len(self.geMat) - len(self.rec[0]) - 1)
        else:
            self.n1 = 2.
            self.n2 = float(len(self.geMat) - 2)
        if self.n2 < 2:
            self.n2 = 2.

    def TcdFileMake(self):
        f = open(self.tcdFile,'w')
        for i,val in enumerate(self.geMat[1][1:]):
            s1 = float(self.varMat[i]/(self.n1-1.0))
            s2 = float(self.varMatEx[i]/(self.n2-1.0))
            if s1 == 0:
                s1 = .001
            if s2 == 0:
                s2 = .001
            x1 = float(self.sumMat[i]/self.n1)
            x2 = float(self.sumMatEx[i]/self.n2)
            self.tscoreMat[i]=abs(x1-x2)/math.sqrt((s1/self.n1)+(s2/self.n2))
            den=((s1/self.n1)**2/(self.n1-1.0))+((s2/self.n2)**2/(self.n2-1.0))
            self.degfree[i] = ((s1/self.n1)+(s2/self.n2)) ** 2/den
            strng = str(self.tscoreMat[i])+'\t'+str(self.degfree[i])+'\n'
            f.write(strng)
        f.close()

    def RunTTest(self):
        strtupinfo = subprocess.STARTUPINFO()
        strtupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        exe = r"C:\Users\francis\Documents\Monguis\BioGui\Utils\calcTCumDist.exe"
        inf = self.tcdFile
        outf = self.tcdoFile
        p = subprocess.Popen(exe+' '+inf+' '+outf+' '+str(len(self.degfree)),
                             startupinfo = strtupinfo)
        p.wait()

    def Results(self):
        tf = open(self.tcdoFile,'r')
        tr = tf.read()
        beta = []
        temp = self.geMat
        self.geMat = []
        for row in temp:
            self.geMat.append([row[0]])
        for i,t in enumerate(tr.split('\n')[:-1]):
            self.pMat[i] = float(t)
            if float(t) < self.a:
                self.sigMat.append(temp[-1][i])
                self.bitFprint += '1'
                if self.sumMat[i] > self.sumMatEx[i]:
                    self.bitFprint += '1'
                else:
                    self.bitFprint += '0'
                for j,r in enumerate(self.geMat[:-1]):
                    r.append(temp[j][i+1])
                beta.append(temp[-1][i])
            else:
                self.bitFprint += '00'
        tf.close()
        self.geMat[-1] = beta
        return self.geMat

    def GetRho(self, rows):
        i = 1
        compdf = self.a
        rho = -1
        while i < len(rows[0]):
            if float(rows[0][i]) == compdf:
                rho = i
                i = len(rows[0])
            else:
                i += 1
        return rho

    def RunResults(self, r, rows):
        beta = []
        temp = self.geMat
        self.geMat = []
        for row in temp:
            self.geMat.append([row[0]])
        for i,t in enumerate(self.tscoreMat):
            j = 0
            while j < len(rows):
                if float(rows[j][0]) >= self.degfree[i]:
                    a = float(rows[j][r])-float(rows[j-1][r])
                    b = self.degfree[i]-float(rows[j-1][0])
                    mu=(a)*(b)+float(rows[j-1][r])
                    j = len(rows)
                else:
                    j += 1
            if t >= mu:
                self.sigMat.append(temp[-1][i]+'\n')
                self.bitFprint += '1'
                if self.sumMat[i] > self.sumMatEx[i]:
                    self.bitFprint += '1'
                else:
                    self.bitFprint += '0'                    
                q = 0
                while q < (len(tempGeo) - 1):
                    self.geMat[q].append(temp[q][i+1])
                    q += 1
                beta.append(temp[-1][i])
            else:
                self.bitFprint += '00'

    def GetExec(self, rec, geMat, alpha):
        self.rec = rec
        self.geMat = geMat
        self.a = alpha
        self.Sizes()
        self.Update()
        self.TcdFileMake()
        self.RunTTest()
        return self.Results()
        """datafile = open(r"..\..\Gene Expressions\tvalues.txt")
        rows = [line.split('\t') for line in datafile]
        return self.RunResults(self.GetRho(rows), rows)"""
