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
import re
from relations import *
from helper2 import *

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
                button = gtk.CheckButton(relationstr[i])
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
