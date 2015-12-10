import wx
import os
import plotter as mpl

class Plugin():
    def OnSize(self):
        if hasattr(self,'plotter'):
            self.axes1.clear()
            self.bPSize = self.coverPanel.GetSize()
            self.plotter.Show(False)
            self.plotter.SetSize((self.bPSize[0], self.bPSize[1]))
            self.plotter.SetPosition((0, 0))
            self.plotter.resize([3.05 / 244, 3.05 / 244])
            self.plotter.Show(True)
            self.DoDraw(wx.EVT_IDLE)

    def Refresh(self,rec):
        if hasattr(self,'plotter'):
            self.axes1.clear()
            self.rec = rec[0][0]
            self.DoDraw(wx.EVT_IDLE)

    def Clear(self):
        self.coverPanel.SetBackgroundColour('WHITE')
        self.coverPanel.SetForegroundColour('BLACK')
        if hasattr(self,'plotter'):
            self.plotter.Show(False)

    def Init(self, parent, bigPanel, colorList):
        self.coverPanel = bigPanel
        self.bPSize = bigPanel.GetSize()
        self.cL = colorList
        self.hD = os.getcwd()

    def GetExec(self, rec):
        self.rec = rec[0][0]
        self.plotter = mpl.PlotNotebook(self.coverPanel,
                                size = (self.bPSize[0] - 105,self.bPSize[1]),
                                pos = (0,0))
        self.coverPanel.SetBackgroundColour('GRAY')
        self.coverPanel.SetForegroundColour('WHITE')
        self.plotter.Show(True)
        self.axes1 = self.plotter.add('figure 1').gca()
        self.DoDraw(wx.EVT_IDLE)

    def get_x_positions(self):
        """Create a mapping of each clade to its horizontal position.
        Dict of {clade: x-coord} 
        """
        self.depths = dict()
        for d in self.rec.depths().keys():
            self.depths[d] = self.rec.depths()[d] * self.ml / 2
        # If there are no branch lengths, assume unit branch lengths 
        if not max(self.depths.itervalues()):
            self.depths = self.rec.depths(unit_branch_lengths=True)

    def get_y_positions(self): 
        """Create a mapping of each clade to its vertical position. Dict of {clade: y-coord}. 
        Coordinates are negative, and integers for tips. 
        """
        #maxheight = self.rec.count_terminals() + 5
        # Rows are defined by the tips 
        """I want to change here so row width can be adjustable
        terminals[-1] is lowest, x_pos is depth so no worry
        start low and work up, term[-1:]
        maxH = sum terminal widths
        if clade width but not child, child width = clade width / len(children)

        bfs e.g. to find max width at depth i
        should add (num term - 1) 5% for space

        maxD = dict()
        for d in self.depths.keys():
            if not self.depths[d] in maxD:
                maxD[self.depths[d]] = 0
            #may need this
                if not hasattr(d, 'width') or d.width is None:
                    d.width = 1
            maxD[self.depths[d]] += d.width
        maxxi = 0
        for d in maxD.values():
            if d > maxxi:
                maxxi = d

        maxheight = (1 + 0.05 * (len(self.depths,keys()) - 1))
        """
        self.heights = dict()
        th = 3
        group = 0
        for i, tip in enumerate(self.rec.get_terminals()):
            if hasattr(tip,'date') and tip.date is not None:
                print tip.date.value - (tip.date.value % 1)
                print group
                if hasattr(tip.date,'value') and tip.date.value is not None:
                    if not tip.date.value - (tip.date.value % 1) == group:
                        #th += 1
                        group = tip.date.value - (tip.date.value % 1)
            self.heights[tip] = th
            th += 3
                
        # Internal nodes: place at midpoint of children
        def calc_row(clade):
                for subclade in clade:
                    if subclade not in self.heights:
                        calc_row(subclade) 
                # Closure over self.heights 
                self.heights[clade] = (self.heights[clade.clades[0]] + self.heights[clade.clades[-1]]) / 2.0

        if self.rec.root.clades: 
              calc_row(self.rec.root)

    def draw_clade(self, clade, x_start): 
        """recursively draw a tree, down from the given clade."""
        x_here = self.depths[clade]
        y_here = self.heights[clade]
        # phyloXML-only graphics annotations 
        if hasattr(clade, 'color') and clade.color is not None: 
            color = clade.color.to_hex()
        else:
            color = 'k'
        if hasattr(clade, 'width') and clade.width is not None: 
            lw = clade.width
        else:
            lw = 2
        # Draw a horizontal line from start to here
        if x_start <= 0:
            x_start=0
        self.axes1.hlines(y_here, x_start, x_here-0.7, color = color, lw = lw) 
        # Add node/taxon labels
        labs = ''
        xys = x_here-0.7
        fys = self.fs
        yys = y_here
        if not clade.clades:
            """labs = clade.name
            fys -= 1
            conf = clade.confidence
            if int(conf) == conf:
                labs+=' '+str(int(conf))
            else:
                labs+=' '+str(int(conf))"""
            yys -= 1
            xys = x_start
            fys = self.fs
            labs = clade.name
            conf = clade.confidence
            if int(conf) == conf:
                while len(labs) < self.ml + 2:
                    labs+=' '
                labs+=str(int(conf))
            else:
                labs+=' '+str(int(conf))
            if clade.taxonomy:
                ref = clade.taxonomy
                labs+=' ['+str(ref)+']'
        elif clade.confidence:
            yys -= 1
            xys = x_start
            fys = self.fs
            labs = clade.name
            conf = clade.confidence
            if int(conf) == conf:
                labs+=' '+str(int(conf))
            else:
                labs+=' '+str(int(conf))
            if clade.taxonomy:
                ref = clade.taxonomy
                labs+=' ['+str(ref)+']'
        if not labs == None:
            self.axes1.text(xys + 0.05, yys,
                            labs, ha = 'left', va = 'center',
                            family = 'monospace', fontsize = fys)
        if clade.clades: 
            # Draw a vertical line connecting all children 
            y_top = self.heights[clade.clades[0]] 
            y_bot = self.heights[clade.clades[-1]]
            if x_here < 0.7:
                x_here = 0.7
            # Only apply widths to horizontal lines, like Archaeopteryx 
            self.axes1.vlines(x_here-0.7, y_bot, y_top, color = color, lw = lw) 
            # Draw descendents 
            for child in clade:
                if hasattr(child, 'color') and child.color is not None: 
                    child.color = child.color.to_hex()
                elif hasattr(clade, 'color') and clade.color is not None: 
                    child.color = clade.color.to_hex()
                else:
                    child.color = 'k'
                if hasattr(child, 'widthr') and child.width is not None: 
                    child.width = child.width
                elif hasattr(clade, 'width') and clade.width is not None: 
                    child.width = clade.width
                self.draw_clade(child, x_here-0.7)

    def CladeNameLen(self, c):
        if not c.name == None:
            if len(c.name) > self.ml and not c.clades:
                self.ml = len(c.name)
        for child in c:
            self.CladeNameLen(child)
    
    def DoDraw(self, event):
        # Add margins around the tree to prevent overlapping the axes 
        self.ml = 0
        self.CladeNameLen(self.rec.root)
        self.get_x_positions()
        self.get_y_positions()
        self.xmax = max(self.depths.itervalues())
        self.fs = int(12 + self.bPSize[1] / 12. / self.ml)
        self.axes1.set_xlim(-0.05 * self.xmax, 1.5 + self.xmax)
        self.draw_clade(self.rec.root, 0)
        self.axes1.scatter(self.depths[self.rec.root],
                           self.heights[self.rec.root],
                           s = 20, c = 'k', marker = 'x')
        # Aesthetics 
        if hasattr(self.rec, 'name') and self.rec.name: 
            self.axes1.set_title(self.rec.name) 
        self.axes1.set_xlabel('branch length') 
        self.axes1.set_ylabel('taxa') 
        # Also invert the y-axis (origin at the top) 
        # Add a small vertical margin, but avoid including 0 and N+1 on the y axis 
        self.axes1.set_ylim(max(self.heights.itervalues()) + 5, 0.1)
        self.plotter.resize([3.05 / 244, 3.05 / 244])
        #print self.depths
  
    def GetType(self):
        return "Phylogenetic Trees"

    def GetName(self):
        return "PhyloTreeView"

def GetType():
    return "Phylogenetic Trees"

def GetName():
    return "PhyloTreeView"
