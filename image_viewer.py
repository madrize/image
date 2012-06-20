import wx
import os
import shutil

class ImageViewer(wx.Frame):
    
    def __init__(self,parent):
        
        wx.Frame.__init__(self,parent,title="Image Viewer",size=(800,600))
        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.CreateMenu()
        self.MakeToolbar()
        self.images = []
        self.count = 0
        self.dirname = ""
        self.Centre()
        self.picMaxSize = 600
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onPrev)
        self.panel.Bind(wx.EVT_KEY_UP, self.onNext)
    
    def CreateMenu(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        aboutMenu = wx.Menu()
        openMenu = fileMenu.Append(-1,"Open","Open an image file")
        fileMenu.AppendSeparator()
        exitMenu = fileMenu.Append(-1,"Exit","Exit the application")
        mirrorMenu = editMenu.Append(-1,"Mirror","Mirror image")
        infoMenu = aboutMenu.Append(-1,"About","About this application")
        menubar.Append(fileMenu,"&File")
        menubar.Append(editMenu,"&Edit")
        menubar.Append(aboutMenu,"&About")
        self.Bind(wx.EVT_MENU, self.onMirror, mirrorMenu)
        self.Bind(wx.EVT_MENU, self.onOpen, openMenu)
        self.Bind(wx.EVT_MENU, self.onAbout, infoMenu)
        self.Bind(wx.EVT_MENU, self.onExit, exitMenu)
    
    def onOpen(self,e):
        wildcard = 'Image files (*.gif;*.png;*.jpg)|*.gif;*.png;*.jpg'
        dbox = wx.FileDialog(self,"Choose an image to display",self.dirname,"",wildcard=wildcard,style=wx.OPEN)
        if dbox.ShowModal() == wx.ID_OK:
            self.filename = dbox.GetPath()
            self.dirname = dbox.GetDirectory()
            self.SetTitle(self.filename)
            # image chosen
            self.image = wx.Image(self.filename, wx.BITMAP_TYPE_ANY, -1)
            self.scaleImage()
            # if the app is run for the first time
            # use showbitmap method, else set a new bitmap
            if not len(self.images) == 0:
                self.bitmap.SetBitmap(wx.BitmapFromImage(self.image))
                self.SetClientSize(self.bitmap.GetSize())
            else:
                self.showBitMap()
            # construct/reconstruct the image list
            tmpimages = [x for x in os.listdir(self.dirname) if os.path.isfile(os.path.join(self.dirname,x))]
            self.images = [x for x in tmpimages if x[-4:] == ".jpg" or x[-4:] == ".png" or x[-4:] == ".JPG" or  x[-4:] == ".PNG" or x[-4:] == ".bmp"]
            # reset the count variable
            self.count = 0
            # enable tools
            self.toolbar.EnableTool(self.pTool.GetId(),True)
            self.toolbar.EnableTool(self.nTool.GetId(),True)
        dbox.Destroy()
    
    def showBitMap(self):
        self.bitmap = wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(self.image))
        self.SetClientSize(self.bitmap.GetSize())

    def onNext(self,e):
        # get next image
        try:
            self.count = self.count + 1
            new_image = os.path.join(self.dirname,self.images[self.count])
        except IndexError:
            self.count = 0
            new_image = os.path.join(self.dirname,self.images[self.count])
        self.SetTitle(new_image)
        self.image = wx.Image(new_image, wx.BITMAP_TYPE_ANY, -1)
        self.scaleImage()
        self.bitmap.SetBitmap(wx.BitmapFromImage(self.image))
        self.SetClientSize(self.bitmap.GetSize())
    
    def onPrev(self,e):
        try:
            self.count = self.count - 1
            new_image = os.path.join(self.dirname,self.images[self.count])
        except IndexError:
            self.count = 0
            new_image = os.path.join(self.dirname,self.images[self.count])
        self.SetTitle(new_image)
        self.image = wx.Image(new_image, wx.BITMAP_TYPE_ANY, -1)
        self.scaleImage()
        self.bitmap.SetBitmap(wx.BitmapFromImage(self.image))
        self.SetClientSize(self.bitmap.GetSize())
    
    def MakeToolbar(self):
        self.toolbar = self.CreateToolBar()
        # open and save tool
        oTool = self.toolbar.AddSimpleTool(-1, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,wx.ART_TOOLBAR,(16,16)), "Open", "Open an image")
        self.Bind(wx.EVT_TOOL, self.onOpen, oTool)
        sTool = self.toolbar.AddSimpleTool(-1, wx.ArtProvider.GetBitmap(wx.ART_COPY,wx.ART_TOOLBAR,(16,16)), "Save", "Save the image file as...")
        self.Bind(wx.EVT_MENU, self.onCopy, sTool)
        # separator
        self.toolbar.AddSeparator()
        # prev tool
        self.pTool = self.toolbar.AddSimpleTool(-1,wx.Bitmap('prev.png'),"Previous","Previous image...")
        self.Bind(wx.EVT_TOOL, self.onPrev, self.pTool)
        self.toolbar.EnableTool(self.pTool.GetId(),False)
        # next tool
        self.nTool = self.toolbar.AddSimpleTool(-1,wx.Bitmap('next.png'),"Next","Next image...")
        self.Bind(wx.EVT_TOOL, self.onNext, self.nTool)
        self.toolbar.EnableTool(self.nTool.GetId(),False)
        # init toolbar
        self.toolbar.Realize()
        
    
    def onMirror(self,e):
        self.image = self.image.Mirror()
        self.bitmap.SetBitmap(wx.BitmapFromImage(self.image))
    
    def onAbout(self,e):
        desc = "This a simple Image Viewer application written in Python using wxPython GUI."
        licence = "This application is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as \
                    published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version."
        info = wx.AboutDialogInfo()
        # info.SetIcon(wx.Icon('image.png', wx.BITMAP_TYPE_PNG))
        info.SetName('ImageViewer')
        info.SetVersion('1.0')
        info.SetDescription(desc)
        info.SetCopyright('(C) 2012 Ugur Yoruk')
        info.SetWebSite('http://www.google.com')
        info.SetLicence(licence)
        wx.AboutBox(info)
    
    def onExit(self,e):
        self.Destroy()
    
    def scaleImage(self):
        ## to be improved...
        w = self.image.GetWidth()
        h = self.image.GetHeight()
        if w > self.picMaxSize:
            if w > h:
                NewW = self.picMaxSize
                NewH = self.picMaxSize * h/w
            else:
                NewH = self.picMaxSize
                NewW = self.picMaxSize * w/h
            self.image = self.image.Scale(NewW, NewH)
        else:
            pass
        
        self.panel.Refresh()

    def onCopy(self,e):
        wildcard = 'Image files (*.gif;*.png;*.jpg)|*.gif;*.png;*.jpg'
        dbox = wx.FileDialog(self,"Choose an image to display",self.dirname,"",wildcard=wildcard,style=wx.OPEN)
        if dbox.ShowModal() == wx.ID_OK:
            n_dir = dbox.GetDirectory()
            n_name= dbox.GetFilename()
            new_path = os.path.join(n_dir,n_name)
            imagetosave = os.path.join(self.dirname,self.images[self.count])
            shutil.copyfile(imagetosave,new_path)
        dbox.Destroy()

# run the app
app = wx.App(False)
iv = ImageViewer(None)
iv.Show()
app.MainLoop()
