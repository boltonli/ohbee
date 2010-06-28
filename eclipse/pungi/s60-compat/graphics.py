#
# graphics
#
# Copyright 2006 Alexander Igonichev.  All rights reserved.
#
# amigo12@newmail.ru
#

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
wxPython emulation of graphics module from Python for S60
"""

import wx

Draw=lambda x: x

def GetFont(fill,font):
    fonts = {
        u'LatinBold12': (8, wx.SWISS, wx.NORMAL, wx.BOLD, 'arial'),
        u'LatinPlain12': (8, wx.SWISS, wx.NORMAL, wx.NORMAL, 'arial'),
        u'LatinBold13': (9, wx.SWISS, wx.NORMAL, wx.BOLD, 'tahoma'),
        u'LatinBold17': (12, wx.SWISS, wx.NORMAL, wx.BOLD, 'arial'),
        u'LatinBold19': (13, wx.SWISS, wx.NORMAL, wx.BOLD, 'arial narrow'),
    }
    
    (size,family,style,weight,face) = fonts[font]
    fnt = wx.Font(size,family,style,weight,False,face=face,encoding=wx.FONTENCODING_UTF8)
    return fnt

class DC:
    def __init__(self,size):
        self._size = size
    size=property(lambda self:self._size)

    def Colour(self,clr):
        if isinstance(clr,int):
            b = clr % 256
            g = (clr>>8) % 256
            r = (clr>>16) % 256
        else:
            (r,g,b) = clr
        return wx.Colour(r,g,b)

    def SetColors(self,dc,outline=None,fill=None,width=1):
        if fill and outline is None:
            outline = fill
        if not outline is None:
            color = self.Colour(outline)
        else:
            color = 'BLACK'
        dc.SetPen(wx.Pen(color,width))
        if not fill is None:
            color = self.Colour(fill)
        elif self.bgcolor:
            color = self.bgcolor
        else:
            color = 'WHITE'
        dc.SetBrush(wx.Brush(color))

    def Coords(self,coords,rect=0):
        list = []
        try:
            for x in coords:
                for i in (0,1):
                    list.append(int("%.0f"%x[i]))
        except:
            for x in coords:
                list.append(int("%.0f"%x))
        ret = []
        i = 0
        prev = None
        nc = rect > 0 and 4 or 2
        while i < len(list):
            x = list[i:i+nc]
            i += nc
            if rect == 1:
                #ret.append((x[0],x[1],x[2]-x[0]+1,x[3]-x[1]+1))
                ret.append((x[0],x[1],x[2]-x[0],x[3]-x[1]))
            elif rect == 2:
                ret.append((x[0],x[1],x[2]-x[0]-1,x[3]-x[1]-1))
            else:
                if rect == 0:
                    if prev:
                        tmp = x
                        x = (prev[0],prev[1],x[0],x[1])
                        prev = tmp
                    else:
                        prev = x
                        continue
                ret.append(x)
        return ret

    def text(self,coords,text,fill=0,font=u'LatinBold12'):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        Font = GetFont(fill,font)
        dc.SetFont(Font)
        #color = isinstance(fill,int) and wx.ColourRGB(fill) or wx.Colour(fill[0],fill[1],fill[2])
        color = self.Colour(fill)
        dc.SetTextForeground(color)
        x = self.Coords(coords,-1)
        dc.BeginDrawing()
        dc.DrawText(text, x[0][0], x[0][1]-Font.GetPointSize()-3)
        dc.EndDrawing()

    def line(self,coords,outline=None,fill=None,width=1,pattern=None):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        dc.BeginDrawing()
        self.SetColors(dc,outline,fill,width)
        dc.DrawLineList(self.Coords(coords))
        dc.EndDrawing()

    def polygon(self,coords,outline=None,fill=None,width=1,pattern=None):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        dc.BeginDrawing()
        self.SetColors(dc,outline,fill,width)
        dc.DrawPolygon(self.Coords(coords,-1))
        dc.EndDrawing()

    def point(self,coords,outline=None,fill=None,width=1,pattern=None):
        if width > 1:
            new_coords = []
            hw = width/2
            for x in self.Coords(coords,-1):
                new_coords.append(x[0]+hw)
                new_coords.append(x[1]+hw)
                new_coords.append(x[0]-hw)
                new_coords.append(x[1]-hw)
            self.ellipse(new_coords,outline,outline,1)
        else:
            dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
            dc.BeginDrawing()
            self.SetColors(dc,outline,fill,width)
            dc.DrawPointList(self.Coords(coords,-1))
            dc.EndDrawing()

    def rectangle(self,coords,outline=None,fill=None,width=1,pattern=None):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        dc.BeginDrawing()
        self.SetColors(dc,outline,fill,width)
        dc.DrawRectangleList(self.Coords(coords,1))
        dc.EndDrawing()

    def ellipse(self,coords,outline=None,fill=None,width=1,pattern=None):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        dc.BeginDrawing()
        self.SetColors(dc,outline,fill,width)
        dc.DrawEllipseList(self.Coords(coords,2))
        dc.EndDrawing()

    def clear(self,color=0xffffff):
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        self.SetColors(dc,fill=color)
        dc.SetBackground(dc.GetBrush())
        self.bgcolor = dc.GetBrush().GetColour()
        dc.Clear()

    def blit(self,image,target=(0,0),source=((0,0),(None,None)),mask=None,scale=0):
        if mask:
            image.buffer.SetMask(wx.Mask(mask.buffer,wx.Colour(0,0,0)))
        dc = (self.dc or wx.BufferedPaintDC(self, self.buffer))
        xdest = target[0]
        ydest = target[0]
        xsrc = source[0][0]
        ysrc = source[0][1]
        width = source[1][0] or image.size[0]
        height = source[1][0] or image.size[1]
        dc.Blit(target[0],target[1],width,height,image.dc,xsrc,ysrc,useMask=(mask and True or False))

class Image(DC):
    def __init__(self,size):
        DC.__init__(self,size)
        dc = wx.MemoryDC()
        bmp = wx.EmptyBitmap(size[0], size[1])
        dc.SelectObject(bmp)
        dc.Clear()
        self.buffer = bmp
        self.dc = dc
        self.bgcolor = None

    def new(size,mode=None):
        return Image(size)
    new=staticmethod(new)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    img = Image.new((100,100))
    print img
    print img.size
    app.MainLoop()
