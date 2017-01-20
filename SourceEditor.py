import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Gdk

class SourceEditor: #(Gtk.Window):

    def __init__(self, *args, **kwargs):
        self.line_num = 50
        #Gtk.Window.__init__(self, *args, **kwargs)
        #self.connect("destroy", Gtk.main_quit)
        #self.create_widgets()
        #self.show_all()

    def create_widgets(self, parent = None):
        self.sourceview=GtkSource.View.new()        
        self.lm = GtkSource.LanguageManager.new()
        self.scrolledwindow = Gtk.ScrolledWindow()
        vbox = Gtk.VBox()
        if parent: parent.add(vbox)
        vbox.pack_start(self.scrolledwindow,True,True,0)
        self.scrolledwindow.add(self.sourceview)      
        self.scrolledwindow.show_all()
        button = Gtk.Button("Jump To Line")
        button.connect("clicked", self.scroll_to_line_and_mark)
        self.open_file_in_srcview("diagram.py")
        vbox.pack_start(button, False, False, 5)
        vbox.set_size_request(300, 250)
        self.vbox = vbox
        self.button = button
        return vbox

    def open_file_in_srcview(self,filename,*args,**kwargs):
        self.buffer = self.sourceview.get_buffer()
        self.filename = filename
        self.language = self.lm.guess_language(self.filename,None)
        self.sourceview.set_show_line_numbers(True)
        if self.language:
            self.buffer.set_highlight_syntax(True)
            self.buffer.set_language(self.language)
        else:
            print 'No language found for file "%s"' % self.filename
            self.buffer.set_highlight_syntax(False)
        txt = open(self.filename).read()
        self.buffer.set_text(txt)
        self.buffer.place_cursor(self.buffer.get_start_iter())


    def scroll_to_line_and_mark(self, *args,**kwargs):
        print "setting iterator"
        iterator = self.sourceview.get_buffer().get_iter_at_line(self.line_num)
        print "scrolling to iter"
        if self.sourceview.scroll_to_iter(iterator,0, False, 0.5, 0.5):
            print "done!"
        else:
            print "scrolling failed!!"


    def scroll_to_line_n_and_mark(self, n):
        print "scroll to n = ", n
        self.line_num = n
        self.button.clicked()
        #print "setting iterator"
        #iterator = self.sourceview.get_buffer().get_iter_at_line(n)
        #print iterator
        #print "scrolling to iter"
        #if self.sourceview.scroll_to_iter(iterator,0, False, 0.5, 0.5):
        #    print "done!"
        #else:
        #    print "scrolling failed!!"

    def do_scroll(self, window):
        event = Gdk.Event()
        event.type = Gdk.EventType.BUTTON_RELEASE
        event.button = 1
        event.window = window
        event.send_event = True
        #event.put()
        #x, y =  window.get_pointer()
        #event.x = x
        #event.y = y
        self.button.emit("button-press-event", event)
        #print "emit ??"
        #self.button.emit("clicked") #, event)
        #print "after emit ??"
        #Gtk.main_do_event(event)


def main():
     editor = SourceEditor()
     win = Gtk.Window()
     editor.create_widgets(win)
     win.connect("delete-event", Gtk.main_quit)
     win.connect("destroy", Gtk.main_quit)
     win.show_all()
     win.present()
     editor.scroll_to_line_n_and_mark(100)
     Gtk.main()
	
if __name__ == "__main__":
    main()
