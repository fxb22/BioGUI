import wx

class BusyNote():
    def Show(self, parent):
        ps = parent.GetSize()
        self.panel = wx.Panel(parent, -1, pos = (ps[0]/2-72,ps[1]/2-100),
                              size = (144,200), style = wx.BORDER_RAISED)
        self.panel.Show(False)
        self.panel.SetBackgroundColour('GRAY')
        img = wx.Image(r'./Utils/Icons/Busy.bmp', wx.BITMAP_TYPE_ANY)
        bmp = wx.StaticBitmap(self.panel, bitmap = wx.BitmapFromImage(img))
        self.panel.Show(True)

    def Clear(self):
        self.panel.Show(False)
        self.panel.Destroy()

