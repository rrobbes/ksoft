from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource

class MyApplication (Gtk.Window):

    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.set_title("SourceView Test")
        self.set_size_request(400, 400)
        self.connect("destroy", Gtk.main_quit)
        self.create_widgets()
        self.show_all()

    def create_widgets(self):
        self.sourceview=GtkSource.View.new()        
        self.lm = GtkSource.LanguageManager.new()
        self.scrolledwindow = Gtk.ScrolledWindow()
        vbox = Gtk.VBox()
        self.add(vbox)
        vbox.pack_start(self.scrolledwindow,True,True,0)
        self.scrolledwindow.add(self.sourceview)      
        self.scrolledwindow.show_all()
        button = Gtk.Button("Jump To Line")
        button.connect("clicked", self.scroll_to_line_and_mark)
        self.open_file_in_srcview("diagram.py")
        vbox.pack_start(button, False, False, 5)

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


    def scroll_to_line_and_mark(self,*args,**kwargs):
        print "setting iterator"
        iterator = self.sourceview.get_buffer().get_iter_at_line(150)
        print iterator
        print "scrolling to iter"
        if self.sourceview.scroll_to_iter(iterator,0, False, 0.5, 0.5):
            print "done!"
        else:
            print "scrolling failed!!"

if __name__ == "__main__":
    MyApplication()
    Gtk.main()
