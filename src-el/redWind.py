import pygtk
pygtk.require('2.0')
import gtk
import re
from relations import *
from helper import *

class RedWindow():
    def toggle_handler(self, widget, data):
	self.returnValue[data] = (False, True)[widget.get_active()]

    def click_handler(self, widget):
	if self.Selected():
	    if self.flag:
		self.flag = False
		self.win.destroy()
	    else:
		gtk.main_quit()
        else:
	    win = gtk.MessageDialog(self.win, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "At least ONE of them should be checked")
	    win.run()
	    win.destroy()

    def Selected(self):
	for i in range(5):
	    if self.returnValue[i]:
		return True
	return False

    def __init__(self, pair, mir):
	self.value = 0
	self.flag = True
	self.returnValue = {}
	self.returnValue[0] = False
	self.returnValue[1] = False
	self.returnValue[2] = False
	self.returnValue[3] = False
	self.returnValue[4] = False
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.win.set_title("Euler/X")
	self.win.set_default_size(250, 200)
        self.win.set_keep_above(True)
	self.vbox = gtk.VBox(gtk.TRUE,3)
        taxa = re.match("(.*),(.*)", pair)
	entry = gtk.Label("What is the relation between "+taxa.group(1)+" and "+taxa.group(2)+"?\n(Check those relations that are possible)?")
	self.vbox.pack_start(entry, gtk.TRUE, gtk.TRUE, 1)
        
	for i in range(5):
	    if mir & (1 << i):
                button = gtk.CheckButton(relstr[i])
		button.connect("toggled", self.toggle_handler, i)
	        button.set_active(True)
	        self.vbox.pack_start(button)

	button = gtk.Button("Done")
        button.connect("clicked", self.click_handler)
        self.vbox.pack_start(button)

	self.win.add(self.vbox)
	self.win.show_all()
	self.win.connect("destroy", self.click_handler)

    def main(self):
	gtk.main()
        val = 0
        for i in range(5):
            if self.returnValue[i]:
                val |= 1 << i
        return val
