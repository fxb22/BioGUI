import wx
import plotter as mpl
import GetMotifs as gm
from numpy import arange, cos, sin, pi

class Plugin():
    def GetMeth(self):
        return self.ssCombo.GetSelection()

    def SetMeth(self, meth):
        self.ssCombo.SetSelection(meth)
        
    def OnSize(self):
        self.bPSize = self.coverPanel.GetSize()
        self.plotter.Show(False)
        self.plotter.SetSize(self.bPSize[1], self.bPSize[1])
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        self.ssText.SetPosition((5,self.bPSize[1]/2 - 50))
        self.ssCombo.SetPosition((5,self.bPSize[1]/2))
        self.r1Text.SetPosition(3 * self.bPSize[1] / 4 + 25,
                                self.bPSize[1] / 3 - 25)
        self.r1Combo.SetPosition(3 * self.bPSize[1] / 4 + 25,
                                 self.bPSize[1] / 3 + 25)
        self.r2Text.SetPosition(3 * self.bPSize[1] / 4 + 25,
                                2 * self.bPSize[1] / 3 - 25)
        self.r2Combo.SetPosition(3 * self.bPSize[1] / 4 + 25,
                                 2 * self.bPSize[1] / 3 + 25),
        self.plotter.Show(True)

    def FrChange(self, frSize):
        self.frSize = frSize
        self.DoDraw(wx.EVT_IDLE)

    def Refresh(self, rec, pdbMat):
        self.rec = rec
        self.pdbMat = pdbMat
        self.DoDraw(wx.EVT_IDLE)

    def DoSCombo(self, event):
        self.SetOrders()
        self.plotter.remove()
        self.DoDraw(wx.EVT_IDLE)

    def SComboInit(self):
        self.ssText = wx.StaticText(self.coverPanel, -1,
                                    "Secondary\n  Structure\n    Algorithm:",
                                    pos = (5, self.bPSize[1] / 2 - 50))
        self.ssCombo = wx.ComboBox(self.coverPanel, -1,
                                   choices = ['Backbone','DSSP'],
                                   pos = (5, self.bPSize[1] / 2),
                                   style = wx.CB_READONLY)
        self.ssCombo.SetSelection(0)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoSCombo, self.ssCombo)

    def RCombosInit(self):
        self.choices = []
        i = 0
        while i < len(self.pdbMat):
            self.choices.append(str(i))
            i += 1
        self.r1Text = wx.StaticText(self.coverPanel, -1,
                                    "File 1:",
                                    pos = (3 * self.bPSize[0] / 4 + 25,
                                           self.bPSize[1] / 3 - 5))
        self.r1Combo = wx.ComboBox(self.coverPanel, -1,
                                   choices = self.choices,
                                   pos = (3 * self.bPSize[0] / 4 + 25,
                                          self.bPSize[1] / 3 + 15),
                                   size = (self.bPSize[0] / 4 - 50, -1),
                                   style = wx.CB_READONLY)
        self.r1Combo.SetSelection(0)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoDraw, self.r1Combo)
        self.r2Text = wx.StaticText(self.coverPanel, -1,
                                    "File 2:",
                                    pos = (3 * self.bPSize[0] / 4 + 25,
                                           2 * self.bPSize[1] / 3 - 5))
        self.r2Combo = wx.ComboBox(self.coverPanel, -1,
                                   choices = self.choices,
                                   pos = (3 * self.bPSize[0] / 4 + 25,
                                          2 * self.bPSize[1] / 3 + 15),
                                   size = (self.bPSize[0] / 4 - 50, -1),
                                   style = wx.CB_READONLY)
        if len(self.pdbMat) >= 2:
            self.r2Combo.SetSelection(1)
        else:
            self.r1Combo.SetSelection(0)
        self.coverPanel.Bind(wx.EVT_COMBOBOX, self.DoDraw, self.r2Combo)

    def SetOrders(self):
        motifs = gm.GetMotifs()
        self.orders = []
        self.helices = []
        self.secLinks = []
        self.sheets = []
        for i,p in enumerate(self.pdbMat):
            temp = motifs.GetExec(self.rec[i], self.frSize, p, 0)
            self.orders.append(temp[0][0])
            self.helices.append(temp[1])
            self.secLinks.append(temp[2])
        for j,order in enumerate(self.orders):
            self.sheets.append([])
            for ordr in order:
                for o in ordr:
                    self.sheets[-1].append(o)
                    i = o[0][0]
                    while i < o[0][1]:
                        self.resPos[j][i][1] = o[1] + 1
                        i += 1
            
    def SetLen(self):
        self.pdbLen = []
        self.resPos = []
        for m in self.pdbMat:
            self.pdbLen.append([0])
            self.resPos.append([])
            ts = 0
            for chain in m.get_list():
                for residue in chain.get_list():                
                    for atom in residue.get_list():
                        if atom.get_name() == 'CA':
                            if atom.get_id()[0][0] not in ["H","W"]:
                                self.resPos[-1].append([ts,-1])
                                ts += 1
                self.pdbLen[-1].append(ts)
            self.pdbLen[-1][0] = ts

    def FindDrawLinks(self, hole):
        for link in self.secLinks[self.active[1]]:
            if link[2] == 0:
                for h in hole:
                    if link[0] >= h[0][0] and link[0] < h[0][1]:
                        for o in hole:
                            if link[1] >= o[0][0] and link[1] < o[0][1]:
                                self.DrawEllipse(h[1][0]+(link[0]-h[0][0]),
                                                  o[1][0]+(link[1]-o[0][0]),
                                                  self.col[1][0])

    def MatchCombo(self, s, m, n):
        a = []
        c = m[0][1]
        while len(a) < len(n) - s:
            a.append([[-1, -1], 0])
        for i in m:
            c*=i[1]
            a.append([[i[0][0],i[0][1]],c])
        while len(a) < s:
            a.append([[-1,-1], 0])
        b = []
        c = n[0][1]
        while len(b) < s - len(m):
            b.append([[-1,-1], 0])
        for i in n:
            c*=i[1]
            b.append([[i[0][0],i[0][1]],c])
        while len(b) < len(a):
            b.append([[-1,-1], 0])
        while len(a) < len(b):
            a.append([[-1,-1], 0])
        return [a, b]

    def SheetScore(self, first, last):
        a = (last[0][1] - last[0][0])
        b = (first[0][1] - first[0][0])
        score = 0
        pos = 0
        if first[1] == 0 or last[1] == 0:
            score = 0
            pos = 0
        else:
            pos = (a - b) / 2
            if a > b:
                score = 7 * b - 5 * (a - b)
            elif a < b:
                score = 7 * a - 5 * (b - a)
            else:
                score = 7 * b 
                pos = 0
        return [score,pos]

    def InHelices(self,a,b,num):
        for rHo in self.helices[self.active[num]]:
            if rHo > a[0][1] and rHo < b[0][0]:
                return True
        return False

    def OrderMatch(self):
        ret = []
        for inner in self.orders[self.active[0]]:
            sumin = 0
            for outer in self.orders[self.active[1]]:
                s = len(inner) + len(outer)
                maxi = 0
                reti = []
                while s > 0:
                    su = 0
                    temp = []
                    tem = self.MatchCombo(s, inner, outer)
                    a = tem[0]
                    b = tem[1]
                    for i,aa in enumerate(a):
                        temp.append([self.SheetScore(a[i],b[i]),a[i],
                                     b[i],-1,-1])
                        if i >= 1:
                            if self.InHelices(a[i-1],aa,0):
                                if self.InHelices(b[i-1],b[i],1):
                                    su += 50
                                    temp[-1][3] = [b[i-1][0][1],b[i][0][0]]
                                    temp[-1][4] = [a[i-1][0][1],a[i][0][0]]
                                else:
                                    su -= 50
                        su += temp[-1][0][0]
                    if s == len(inner) + len(outer) or su > maxi:
                        maxi = su
                        if su > sumin:
                            sumin = su
                            reti = temp
                    s -= 1
            ret.append(reti)
        return ret

    def CountSort(self, mo):
        t = dict()
        maxi = 0
        for m in mo:
            t[int(m[1][0])] = m
            if m[1][0] > maxi:
                maxi = m[1][0]
        ret = []
        i = 0
        while i <= maxi:
            if i in t.keys():
                ret.append(t[i])
            i += 1
        return ret

    def DrawOuter(self):
        strt = 0
        for pl in self.pdbLen[self.active[1]][1:]:
            while strt < pl:
                self.DrawArc(strt, strt + .6, self.col[1][4], 1, 1.1)
                strt += 1
        for order in self.orders[self.active[1]]:
            sign = 1
            for o in order:
                sign *= o[1]
                self.DrawArc(o[0][0],o[0][1],self.col[1][sign+1], 6, 1.1)
                self.resPos[self.active[1]][o[0][0]][1] = sign + 1
        for link in self.secLinks[self.active[1]]:
            if link[2] == 1:
               link[2] = 2
            self.DrawEllipse(link[0],link[1],self.col[1][link[2]+1])

    def PlaceHelix(self,m):
        for h in self.secLinks[self.active[1]]:
            if h[0] >= m[3][0] and h[1] < m[3][1]:
                self.DrawEllipse(h[0], h[1], self.col[0][3])
                i = int(m[4][0])+1
                while i < m[4][1]:
                    if i + 0.3 in self.helices[self.active[0]]:
                        j = 0
                        while j < m[3][1] - m[3][0]:
                            if j + i + 0.3 in self.helices[self.active[0]]:
                                self.resPos[self.active[0]][i]=[h[0],1]
                            else:
                                j = m[3][1] - m[3][0]
                            j += 1
                        i = m[4][1]
                    i += 1
                    
    def DrawInner(self):
        sheetMatches = self.OrderMatch()
        for match in sheetMatches:
            for m in match:
                i = m[1][0]
                if not i[0] == -1:
                    o = int(0.5 + m[0][1])
                    t = m[2][0][0]
                    sign = self.resPos[self.active[1]][t][1]
                    self.DrawArc(t+o,t+i[1]-i[0]+o,self.col[0][sign],6,1)
                    j = 0
                    while i[0] + j < i[1]:
                        self.resPos[self.active[0]][i[0]+j] = [t+j+o,sign]
                        j += 1
                    if not m[3] == -1:
                        self.PlaceHelix(m)                           
        for z,s in enumerate(self.secLinks[self.active[0]]):
            if s[2] == 0:
                self.DrawEllipse(self.resPos[self.active[0]][int(s[0])][0],
                                  self.resPos[self.active[0]][int(s[1])][0],
                                  self.col[0][1])
        i = 0
        while i < len(self.resPos[self.active[0]]):
            t = self.resPos[self.active[0]][i]
            while not t[1] == -1 and i < len(self.resPos[self.active[0]])-1:
                i += 1
                t = self.resPos[self.active[0]][i]
            strt = [self.resPos[self.active[0]][i-1],i-1]
            while t[1] == -1 and i < len(self.resPos[self.active[0]])-1:
                i += 1
                t = self.resPos[self.active[0]][i]
            last = [self.resPos[self.active[0]][i],i]
            if strt[0][1] < 0:
                strt[0][0] = -1
                strt[1] = -1
            if last[0][1] < 0:
                last[0][0] = strt[0][0] + (last[1] - strt[1])
            self.DrawCra(strt[0][0]+1,last[0][0],(last[1] - strt[1] - 1))
            i += 1
            
    def DoDraw(self, event):
        self.axes1 = self.plotter.add('figure 1').gca()
        a = self.pdbLen[self.r1Combo.GetSelection()][0]
        if a < self.pdbLen[self.r2Combo.GetSelection()][0]:
            self.active = [self.r1Combo.GetSelection(),
                           self.r2Combo.GetSelection()]
        else:
            self.active = [self.r2Combo.GetSelection(),
                           self.r1Combo.GetSelection()]
        self.col = [['#FFCC00','#0000AA','#66CC66','#880000','#0000CC'],
                    ['#CC9900','#8888FF','#336633','#DE89BC','#000000'],
                    ['#CCFF44','#00CCCC','#6666CC','#00CCFF','#00FFAA']]
        self.DrawOuter()
        self.DrawInner()
        self.axes1.set_xlim(-1.3, 1.3)
        self.axes1.set_ylim(-1.3, 1.3)
        self.axes1.axis('off')
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        
    def GetExec(self, rec, frame, coverPanel, frSize, pdbMat):
        self.rec = []
        for r in rec:
            self.rec.append([str(r[1]+'/'+r[0])])
        self.pdbMat = pdbMat
        self.frame = frame
        self.coverPanel = coverPanel
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.SetForegroundColour('WHITE')
        self.frSize = frSize
        self.bPSize = self.coverPanel.GetSize()
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                            size = (self.bPSize[1],self.bPSize[1]),
                            pos = ((self.bPSize[0]-self.bPSize[1])/2, 0))
        self.plotter.Show(True)
        self.SComboInit()
        self.RCombosInit()
        self.SetLen()
        self.SetOrders()
        self.DoDraw(wx.EVT_IDLE)

    def DrawEllipse(self,numa,numb,col):
        denom = self.pdbLen[self.active[1]][0]+4
        ecc1 = sin(2 * pi * numa / (denom))
        ecc2 = sin(2 * pi * numb / (denom))
        ell1 = cos(2 * pi * numa / (denom))
        ell2 = cos(2 * pi * numb / (denom))
        eccb = .1*sin(2*pi*((numa-numb)/2+numb)/(denom))
        ellb = .1 * cos(2 * pi * ((numa - numb) / 2 + numb) / (denom))
        i = .03
        ecc = []
        ell = []
        while i <= .98:
            ecc.append((1-i)*((1-i)*ecc1+i*eccb)+i*((1-i)*eccb+i*ecc2))
            ell.append((1-i)*((1-i)*ell1+i*ellb)+i*((1-i)*ellb+i*ell2))
            i += 0.01
        self.axes1.plot(ecc,ell,col)

    def DrawArc(self,starter,india,col,num,rad):
        t = arange(starter, india, 0.05)
        s = rad*cos(-2*pi*t/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        u = rad*sin(2*pi*t/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        self.axes1.plot(s,u, color=col, lw = num)

    def DrawCra(self, strt, last, diff):
        pointAx = cos(-2*pi*strt/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        pointAy = sin(2*pi*strt/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        pointBx = cos(-2*pi*last/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        pointBy = sin(2*pi*last/(self.pdbLen[self.active[1]][0]+4)+pi/2)
        slope = (pointBy - pointAy) / (pointBx - pointAx)
        jump = (pointBx - pointAx) / diff / 2.
        if jump < 0:
            hole = pointBx
            pointBx = pointAx
            jump *= -1
        else:
            hole = pointAx
        while hole < pointBx:
            y1 = pointAy + slope * (hole - pointAx)
            y2 = pointAy + slope * (hole + jump - pointAx)
            self.axes1.plot([hole, hole + jump], [y1, y2],
                            color = self.col[0][4], lw = 1)
            hole += 2 * jump
            
def GetExec(rec, frSize, pdbMat, meth):
    cpss = cpc.SecondaryStructure()
    cpss.GetExec(rec, frSize, pdbMat, meth)
    return cpss

def GetName():
    return "CPCompS"
