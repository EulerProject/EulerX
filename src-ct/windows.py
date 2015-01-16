# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
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

import pygtk
pygtk.require('2.0')
import gtk

class Window():
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

    def __init__(self, goal, rel):
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
	self.vbox = gtk.VBox(gtk.TRUE,3)
	entry = gtk.Label("What is the relation between "+goal[0]+" and "+goal[1]+"?\n(Check those relations that are possible)?")
	self.vbox.pack_start(entry, gtk.TRUE, gtk.TRUE, 1)
        
	for i in range(len(rel)):
	    if rel[i] == "is_included_in":
                button = gtk.CheckButton("is_included_in (<)")
		button.connect("toggled", self.toggle_handler, 0)
	    elif rel[i] == "includes":
                button = gtk.CheckButton("includes (>)")
		button.connect("toggled", self.toggle_handler, 1)
	    elif rel[i] == "equals":
                button = gtk.CheckButton("equals (=)")
		button.connect("toggled", self.toggle_handler, 2)
	    elif rel[i] == "overlaps":
                button = gtk.CheckButton("overlaps (><)")
		button.connect("toggled", self.toggle_handler, 3)
	    elif rel[i] == "disjoint":
                button = gtk.CheckButton("disjoint (!)")
		button.connect("toggled", self.toggle_handler, 4)
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
	str = ""
	if self.returnValue[0] == True:
	    str += "is_included_in "
	if self.returnValue[1] == True:
	    str += "includes "
	if self.returnValue[2] == True:
	    str += "equals "
	if self.returnValue[3] == True:
	    str += "overlaps "
	if self.returnValue[4] == True:
	    str += "disjoint "
	return str.rstrip()
