import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import gettext
gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext

class QuestionDialog(Gtk.Dialog):

	def __init__(self, parent, title, question):
		
		Gtk.Dialog.__init__(self, title, parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(150, 100)
		
		hbox=Gtk.HBox()
		label = Gtk.Label(question)
		label.set_margin_bottom(20)
		image=Gtk.Image.new_from_icon_name("dialog-warning",Gtk.IconSize.DIALOG)
		hbox.pack_start(image,True,True,5)
		hbox.pack_start(label,True,True,5)
		
		box = self.get_content_area()
		box.set_border_width(10)
		box.add(hbox)
		self.show_all()
		
	#def init

class ErrorDialog(Gtk.Dialog):

	def __init__(self, parent, title, msg):
		
		Gtk.Dialog.__init__(self, title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(150, 100)
		
		hbox=Gtk.HBox()
		label = Gtk.Label(msg)
		image=Gtk.Image.new_from_icon_name("dialog-error",Gtk.IconSize.DIALOG)
		hbox.pack_start(image,True,True,5)
		hbox.pack_start(label,True,True,5)
		
		box = self.get_content_area()
		box.set_border_width(10)
		box.add(hbox)
		self.show_all()
		
	#def init

class InfoDialog(Gtk.Dialog):

	def __init__(self, parent, title, msg):
		
		Gtk.Dialog.__init__(self, title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(150, 100)
		
		hbox=Gtk.HBox()
		label = Gtk.Label(msg)
		image=Gtk.Image.new_from_icon_name("dialog-info",Gtk.IconSize.DIALOG)
		hbox.pack_start(image,True,True,5)
		hbox.pack_start(label,True,True,5)
		
		box = self.get_content_area()
		box.set_border_width(10)
		box.add(hbox)
		self.show_all()
		
	#def init
	
class ApplyingChangesDialog(Gtk.Dialog):
	
	def __init__(self, parent,title="Lliurex Remote Installer",msg=_(u"Applying changes...")):
		
		Gtk.Dialog.__init__(self, title, parent, 0, ())
		#self.set_default_size(150, 100)
		
		self.set_modal(True)
		self.set_resizable(False)
		
		hbox=Gtk.HBox()
		label=Gtk.Label(msg)
		spinner=Gtk.Spinner()
		spinner.start()
		hbox.pack_start(spinner,True,True,5)
		hbox.pack_start(label,True,True,5)
		
		box = self.get_content_area()
		box.set_border_width(10)
		box.add(hbox)
		self.show_all()
		
	#def init
	
	
	
	
	
class FileDialog(Gtk.FileChooserDialog):
	
	
	def __init__(self,parent,title=_(u"Please choose a file"), path="/home"):
		

		Gtk.FileChooserDialog.__init__(self,title, parent, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.set_current_folder(path)
		
	#def init
