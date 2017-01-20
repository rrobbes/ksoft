import wx
try:
        import wx.lib.wxcairo
        import cairocffi as cairo
        haveCairo = True
except ImportError:
        haveCairo = False

class MyFrame(wx.Frame):
        def __init__(self, parent, title):
                wx.Frame.__init__(self, parent, title=title, size=(640,480))
                self.canvas = CairoPanel(self)
                self.Show()
                
class CairoPanel(wx.Panel):
        def __init__(self, parent):
                wx.Panel.__init__(self, parent, style=wx.BORDER_SIMPLE)
                self.Bind(wx.EVT_PAINT, self.OnPaint)
                self.text = 'Hello World!'

        def OnPaint(self, evt):
                #Here we do some magic WX stuff.
                dc = wx.PaintDC(self)
                width, height = self.GetClientSize()
                cr = wx.lib.wxcairo.ContextFromDC(dc)
                
                #Here's actual Cairo drawing
                size = min(width, height)
                cr.scale(size, size)
                cr.set_source_rgb(0, 0, 0) #black
                cr.rectangle(0, 0, width, height)
                cr.fill()
                
                cr.set_source_rgb(1, 1, 1) #white               
                cr.set_line_width (0.04)
                cr.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size (0.07)
                cr.move_to (0.5, 0.5)
                cr.show_text (self.text)
                cr.stroke ()
        
        #Change what text is shown
        def SetText(self, text):
                self.text = text
                self.Refresh()

if haveCairo:
        app = wx.App(False)
        theFrame = MyFrame(None, 'Barebones Cairo Example')
        app.MainLoop()
else:
        print "Error! PyCairo or a related dependency was not found"
