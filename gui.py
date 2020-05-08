# gui.py

import wx
title = 'SpreadMaster'


class SimpleFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # config
        self.version = '1.0b'
        self.title = title
        self.description = 'Oldalpárok vágása JPG formátumú képekből...'
        self.email = 'tothjx@gmail.com'
        self.title_path = 'Könyvtárak elérési útvonala:'

        #main frame
        super(SimpleFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self)


        st = wx.StaticText(panel, label=self.title_path, pos=(10,10))
        font = st.GetFont()
        #font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        path_original = wx.TextCtrl(self, value='eredeti útvonal', pos=(10, 50), size=(300, -1))
        self.makeMenuBar()
        self.CreateStatusBar()

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        #fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&About")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox('hello')

    def OnAbout(self, event):
        version = 'verziószám: ' + self.version
        info = self.title + \
            '\n' + self.description + \
            '\n' + version + \
            '\n\n' + 'további információ: ' + self.email
        wx.MessageBox(info, self.title, wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frm = SimpleFrame(None, title = title, size=(800, 600))
    frm.Show()
    app.MainLoop()
