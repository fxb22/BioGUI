import wx
import os
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas

class Plot(wx.Panel):
    def __init__(self, parent, id = -1, dpi = None):
        ps = parent.GetSize()
        wx.Panel.__init__(self, parent, id=id, size=ps)
        self.SetBackgroundColour('WHITE')
        self.figure = mpl.figure.Figure(dpi=dpi, facecolor = 'w',
                                        figsize=(ps[0] * .09,
                                                 ps[1] * .09))
        #self.figure.SetBackgroundColour('WHITE')
        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour('WHITE')
        self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.doSave)

    def doSave(self, event):
        dlg = wx.FileDialog(self, message = "Save file as ...",
                            defaultDir = os.curdir, defaultFile = "",
                            wildcard = "*.png", style = wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        self.figure.savefig(path, dpi = None, facecolor = 'w', edgecolor = 'w',
                            orientation = 'portrait', papertype = None,
                            format='png', transparent=False, bbox_inches=None,
                            pad_inches = 0.1, frameon = None)

class PlotNotebook(wx.Panel):
    def __init__(self, parent, size, pos, id = -1):
        wx.Panel.__init__(self, parent, size = size, pos = pos, id = id)
        self.SetBackgroundColour('WHITE')
        self.Show(True)

    def resize(self, ratio):
        ss = self.GetSize()
        self.page.SetSize(ss)
        self.page.figure.set_figwidth(ss[0] * ratio[0])
        self.page.figure.set_figheight(ss[1] * ratio[1])
        self.page.canvas.draw()

    def add(self, name = "plot"):
        self.page = Plot(self)
        self.page.SetBackgroundColour('WHITE')
        return self.page.figure

    def remove(self):
        if hasattr(self, 'page'):
            self.page.Show(False)
