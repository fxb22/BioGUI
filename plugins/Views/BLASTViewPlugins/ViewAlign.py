import wx

class alignBox(wx.Dialog):
    # A pop up showing the alignment of the selected Blast Record alignment
    def __init__(self, parent, title, size, fileName = None):
        wx.Dialog.__init__(self, parent, title = title, size = size)
        self.text = wx.TextCtrl(self, -1, "", pos = (10, 10),
                                size = (size[0] - 20, size[1] - 40),
                                style = wx.TE_MULTILINE|wx.HSCROLL|wx.VSCROLL)
        font = self.text.GetFont()
        newFont = wx.Font(font.PointSize, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text.SetFont(newFont)

class Plugin():
    def GetFileName(self):
        # Return file name
        return ''

    def GetExec(self, info, bP, hd, bral, brap):
        if len(info[1]) > 7:
            s = 320
        else:
            s = (len(info[1]) + 1) * 35 + 30
        alignDiag = alignBox(bP, 'Alignment', (900, s), -1)
        alignDiag.text.write('****Alignment****\n')
        alignDiag.text.write('\n')
        alignDiag.text.write('Q. query\t' + str(info[1][0]))
        i = 1
        while i < len(info[1]):
            if len(info[1][i]) == len(info[1][0]):
                alignDiag.text.write('\n\t\t')
                for j,m in enumerate(info[1][i]):
                    if info[1][0][j] == m:
                        alignDiag.text.write(r'|')
                    elif m == r'+':
                        alignDiag.text.write(r'+')
                    else:
                        alignDiag.text.write(r' ')
                alignDiag.text.write(
                    '\t\n'+str(i/2)+'. '+info[2][i/2+1]+'\t'+info[1][i])
            i += 2
        alignDiag.ShowModal()

def GetName():
    # Return name
    return "View Alignment"

def GetColors():
    # Return string identifying object of coloring
    return 'ViewPanelButton'

def GetExec(info, bP, bral, brap):
    if len(info[1]) > 7:
        s = 320
    else:
        s = (len(info[1]) + 1) * 35 + 30
    alignDiag = alignBox(bP, 'Alignment', (900,s), -1)
    alignDiag.text.write('****Alignment****\n')
    alignDiag.text.write('\n')
    alignDiag.text.write('Q. query\t' + str(info[1][0]))
    for i,n in enumerate(info[1]):
        alignDiag.text.write('\n\t\t')
        for j,m in enumerate(n):
            if info[1][0][j] == m:
                alignDiag.text.write(r'|')
            elif m == r'+':
                alignDiag.text.write(r'+')
            else:
                alignDiag.text.write(r' ')
        alignDiag.text.write(
            '\t\n' + str(i + 1) + '. ' + info[2][i+1] + '\t'+ n) 
    alignDiag.ShowModal()
    return ''
