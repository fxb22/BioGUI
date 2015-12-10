import wx
import os

class acDialog(wx.Dialog):
    def SaveImg(self, event):
        a = os.getcwd()+'\Records\Ancestor Charts/GO_'+self.title[3:]+'.png'
        self.ac.SaveFile(a, wx.BITMAP_TYPE_PNG)
    
    def ShowImage(self,img):
        ac = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.ac = ac
        panel = wx.Panel(self,-1,size=(5,5),pos=(0,0))
        self.display = wx.StaticBitmap(panel, -1,
                         bitmap=ac)
        panel.SetSize((ac.GetWidth(), ac.GetHeight()))
        self.SetSize((ac.GetWidth(), ac.GetHeight()+75))
        self.saveButton = wx.Button(panel, -1, "Save", size=(70,30),
                                    pos = (self.GetSize()[0]/2.-35,
                                           ac.GetHeight() + 10))
        self.saveButton.SetBackgroundColour('RED')
        self.saveButton.SetForegroundColour('WHITE')
        panel.Bind(wx.EVT_BUTTON, self.SaveImg, self.saveButton)
        self.ShowModal()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent, title):
        self.title = title
        wx.Dialog.__init__(self, parent, title = title + r' Ancestor Chart')

    def OnClose(self, event):
        self.Destroy()        


