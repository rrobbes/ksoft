import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class SourceEditor(Gtk.Widget):

    def __init__(self):
        Gtk.Widget.__init__(self)


        #self.grid = Gtk.Grid()
        #self.add(self.grid)

        #self.create_toolbar()
        #self.create_buttons()

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
	scrolledwindow.set_policy(Gtk.PolicyType.NEVER,  Gtk.PolicyType.ALWAYS)
        #self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
	self.textview.set_cursor_visible(True)
        self.textview.set_size_request(200,150)
        self.textbuffer = self.textview.get_buffer()
        text = '\n'.join(map(lambda n: str(n), range(1, 500)))
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. " + text)
        scrolledwindow.add(self.textview)
        scrolledwindow.set_size_request(300,200)
        return scrolledwindow

    def add_to(self, window):
        scroll = self.create_textview()
        window.add(scroll)


    def set_text(self, text):
        self.textbuffer.set_text(text)
         
    def scroll_to(self, line_num):
         textiter = self.textbuffer.get_iter_at_line(line_num)
	 self.textbuffer.create_mark("go_there", textiter, False)
         mark = self.textbuffer.get_mark("go_there")
         #if self.textview.scroll_to_mark(mark, 0.1, True, 0.5, 0.5):
         #    print "Yay!"
         #else:
         #    print "Nay ..."
         while textiter.forward_line():
                 print '.'
             #for i in range(1,100):
             #   textiter.forward_line()
         if self.textview.scroll_to_iter(textiter, 0.1, True, 0.5, 0.5):
                print "Scrolled"
         else:
                print "Failed"

     
def main():
     
     editor = SourceEditor()
     win = Gtk.Window()
     editor.add_to(win)
     win.show_all()
     win.connect("delete-event", Gtk.main_quit)
     win.present()
     editor.scroll_to(50)
     Gtk.main()
	 
	 
if __name__ == "__main__":    
     main()
 
