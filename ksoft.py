#! /usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import sys
from os import listdir, walk
from os.path import isfile, join
import search
import SourceEditor

class MouseButtons:
     
     LEFT_BUTTON = 1
     RIGHT_BUTTON = 3
     
     
class KSoft(Gtk.Window):

     def __init__(self):
	 super(KSoft, self).__init__()
	 
	 self.init_ui()
	 
     def get_files(self, path = '.', ext = '.py'):
	     result = []
	     for root, dirs, files in walk(path):
		 result.extend([ join(root,fi) for fi in files if fi.endswith(ext) ])
	     return result

	 
     def init_ui(self):    

	self.set_title("4K Soft")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, False, 4)

        self.add_search(hbox, (255, 0, 0), "red")
        self.add_search(hbox, (0, 255, 0), "green")
        self.add_search(hbox, (0, 0, 255), "blue")
        self.add_search(hbox, (255, 255, 0), "yellow")
        self.add_search(hbox, (255, 100, 0), "orange")
        self.add_search(hbox, (0, 255, 255), "cyan")
        #hbox.pack_start(Gtk.Label("red"), False, False, 0)
        #hbox.pack_start(Gtk.Entry(), False, False, 0)
        #hbox.pack_start(Gtk.Label("green"), False, False, 0)
        #hbox.pack_start(Gtk.Entry(), False, False, 0)

	self.darea = Gtk.DrawingArea()
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)        
	self.darea.connect("draw", self.on_draw)
        print "connecting button press"
	self.darea.connect("button-press-event", self.on_button_press)
        #self.darea.set_size_request(3000,1600)
        self.darea.set_size_request(1300,500)
        vbox.pack_start(self.darea, True, True, 0)

        self.add_editors(vbox)

	self.resize(1300, 700)
	#self.resize(3500, 2000)
	self.set_position(Gtk.WindowPosition.NONE)
	self.connect("delete-event", Gtk.main_quit)


	#self.source_files = [open('ksoft.py'), open('lines.py'), open('clock.py')]
        args = sys.argv[1:]
        if len(args) >= 2:
            directory = args[0]
            extension = args[1]
            self.source_files = self.get_files(directory, extension)
        else:
	    self.source_files = self.get_files()
        self.searcher = search.Searcher()
        self.searcher.add_searches("def fun if else elif yield return print for class import from while", (0, 0, 255))
	print self.source_files
	#self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
	#self.keywords = sys.argv[1:]

	self.show_all()
        self.present()

        screen = self.get_screen()
        monitors = []
        print screen.get_width()
        print screen.get_height()
        print screen.get_n_monitors()
        for m in range(screen.get_n_monitors()):
          data = screen.get_monitor_geometry(m)
          print data.x, data.y
          print data.width, data.height
          monitors.append(data)
	 
     
     def add_search(self, box, color, text):
         label = Gtk.Label(text)
         box.pack_start(label, False, False, 0)
         entry = Gtk.Entry()
         box.pack_start(entry, False, False, 0)
         entry.connect("activate", lambda x: self.search(x.get_text(), color))

     def search(self, text, color):
        self.searcher.add_searches(text, color)
        self.darea.queue_draw()

     def add_editors(self,vbox):
         hbox = Gtk.Box(spacing = 6)
         vbox.pack_start(hbox, False, False, 4)
         self.editors = []
         self.add_editor(hbox)
         self.add_editor(hbox)
         self.add_editor(hbox)
         self.add_editor(hbox)
         self.add_editor(hbox)
         self.add_editor(hbox)
       
     def add_editor(self, hbox):
         the_editor = SourceEditor.SourceEditor()
         self.editors.append(the_editor)
         vbox = the_editor.create_widgets()
         hbox.pack_start(vbox, False, False, 4)
         #the_editor.set_text("testing")

     def on_button_press(self, w, e):
         print "press"
         print e.x, e.y, self.get_line_num(e.y)
         print "hey"
         thefile = self.get_file_at(e.x)
         if not thefile:
             print "no file found"
             return 0
         #thelines = self.get_lines_around(thefile, e.y)
         theline = self.get_line_num(e.y)
         edit = self.editors[0]
         #edit.set_text(open(thefile).read())
         edit.open_file_in_srcview(thefile)
         edit.scroll_to_line_n_and_mark(theline)
         self.editors = self.editors[1:] + [edit]
         edit.do_scroll(self)

     def get_file_at(self, x):
         index = int(x / 80)
         print index, 'vs', len(self.source_files)
         if len(self.source_files) > index:
             return self.source_files[index]

     def get_lines_around(self, sourcefile, y):
         print sourcefile
         f = open(sourcefile)
         adjusted_y = (y - 10) / 2
         return f.read()

     def get_line_num(self, y):
         return int((y - 10) / 2)

     def on_draw(self, wid, cr):
	 print "drawing"
         #self.do_draw(cr)

         #def do_draw(self, cr):
	 print "do_draw"
	 cr.set_source_rgb(255, 255, 255)
         x, y = (0, 0) #self.darea.translate_coordinates(self, 0, 0)
         cr.rectangle(x, y, self.darea.get_allocated_width(), self.darea.get_allocated_height())
         cr.fill()
	 cr.set_line_width(0.5)
	 y = 0
	 fnum = 0
	 for f in self.source_files:
		 self.draw_file(f, fnum, cr)
		 fnum += 1


     def draw_file(self, fname, fnum, cr):
	 #f.seek(0)
	 f = open(fname)
	 y = 10
	 offset = fnum * 80
	 for l in f:
		 self.draw_line(l, y, offset, cr)
		 y += 2

     """
	 for l in self.source_file:
		 if l.strip() > 0:
			 x = 0
			 for char in l:
				 if char == ' ':
					 x += 1
				 elif char == '\t':
			 		 x += 4
				 else: break
			 xend = 0
			 for char in l:
				 if char == '\t':
					 xend += 4
				 else: 
					 xend += 1

			 if xend > x:
			 	 cr.move_to(x,y)
				 cr.line_to(len(l), y)
				 cr.stroke()
		 y += 2
		 print(y, len(l)) 
		 print(y, len(l)) 
		 print(y, len(l))   l   l   l   l   l
		 print(y, len(l)) lll lll lll lll lll
		 print(y, len(l)) 
		 print(y, len(l)) 
		 print(y, len(l)) 
     """

     def draw_line(self, line, y, offset, cr):
	     words = line.split()
	     x = offset
	     tab = 8
	     working_line = line[:]
	     for word in words:
		     index = working_line.index(word)
		     spaces = working_line[0:index]
		     for s in spaces:
			     if s == '\t': x += tab
			     else: x += 1
		     self.draw_word(x, y, word, cr)
		     x += len(word)
		     working_line = working_line[index + len(word):]
	
     def draw_word(self, x, y, word, cr):
	      self.draw_colored_word(x, y, len(word), cr)
              for match in self.searcher.matches(word):
                  start, end, color = match
                  self.draw_colored_word(x+start, y, end, cr, color, 2)
	      #kidx = 0
	      #for k in self.keywords:
	      #      if k in word:
	      #	      idx = word.index(k)
	      #	      color = self.colors[kidx]
	      #	      self.draw_colored_word(x+idx, y, len(k), cr, color, 2)
	      #      kidx += 1


     def draw_colored_word(self, x, y, end, cr, color = (0, 0, 0), width = 0.5):

	 	cr.set_line_width(width)
	        cr.set_source_rgb(*color)
		cr.move_to(x, y)
		cr.line_to(x + end,y)
		cr.stroke()
     """
	     for char in line:
		     if char == '\t':
			     x += tab
		     else: x += 1

		     if char.isspace():
			     #check if end word boundary
			     if prev.isspace():
				     # not word boundary
		     else:
			     #check if start word boundary
     """

			  
							 
     
def main():
     
     app = KSoft()
     Gtk.main()
	 
	 
if __name__ == "__main__":    
     main()
 
