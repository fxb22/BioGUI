import wx
import os

class Plugin():
    def OnSize(self):
        self.bPSize = self.bigPanel.GetSize()
        if hasattr(self, 'display'):
            self.Clear()
            self.ShowImage()

    def Refresh(self,record):
        self.Clear()
        self.GetExec(record)

    def Clear(self):
        if hasattr(self, 'display'):
            self.display.Show(False)
            self.display.Destroy()

    def Init(self, parent, bigPanel, colorList):
        self.colorList = colorList
        self.bigPanel = bigPanel
        #self.bigPanel.Show(True)
        #bigPanel.SetBackgroundColour("BLUE")
        self.bPSize = bigPanel.GetSize()
        self.dir = parent.dirCtrl.GetPath()
        self.rec = ""
               
    def ShowImage(self):
        h = self.img.GetHeight() * 1.
        w = self.img.GetWidth()*1.
        if self.bPSize[1] / h > (self.bPSize[0] - 187)/ w:
            ratio = (self.bPSize[0] - 187)/ w
        else:
            ratio = self.bPSize[1] / h
        self.img = self.img.Rescale(w*ratio,h*ratio)
        self.display = wx.StaticBitmap(self.bigPanel, -1, 
                                  bitmap = self.img.ConvertToBitmap(),
                                  pos=((self.bPSize[0] - 97 - w*ratio)/2.,
                                       (self.bPSize[1] + 10 - h * ratio)/2.),
                                  size = (w * ratio - 10, h * ratio - 10),
                                       style = wx.SIMPLE_BORDER)

    def GetExec(self, rec):
        self.rec = self.dir + '/' + rec[0][0]
        self.img = wx.Image(self.rec, wx.BITMAP_TYPE_ANY)
        self.ShowImage()

    def GetType(self):
        return "Images"

    def GetName(self):
        return "ImageView"

def GetType():
    return "Images"

def GetName():
    return "ImageView"
