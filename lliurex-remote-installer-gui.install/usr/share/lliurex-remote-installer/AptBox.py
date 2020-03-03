import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core

import Dialog
import time
import threading
import sys


gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext


RSRC="./"


class AptBox(Gtk.VBox):
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"

		builder.add_from_file(ui_path)
		self.main_box=builder.get_object("section_box")
		self.list_box=builder.get_object("list_box")
		self.package_list_box=builder.get_object("package_list_box")
		self.package_list_vp=builder.get_object("package_list_viewport")
		self.add_package_button=builder.get_object("add_package_button")
		self.delete_apt_button=builder.get_object("delete_button")
		self.add_apt_button=builder.get_object("add_button")
		self.apply_button=builder.get_object("apply_button")
		self.url_entry=builder.get_object("url_entry")
		self.data_box=builder.get_object("apt_data_box")
		self.data_vp=builder.get_object("apt_data_viewport")
		self.package_label=builder.get_object("package_label")
		self.url_label=builder.get_object("url_label")
		self.new_package_window=builder.get_object("new_package_window")
		self.new_apt_window=builder.get_object("new_apt_window")
		self.cancel_apt_button=builder.get_object("cancel_apt_button")
		self.accept_apt_button=builder.get_object("accept_apt_button")
		self.cancel_add_package_button=builder.get_object("cancel_add_package_button")
		self.accept_add_package_button=builder.get_object("accept_add_package_button")
		self.apt_name_entry=builder.get_object("apt_name_entry")
		self.apt_url_entry=builder.get_object("apt_url_entry")
		self.apt_msg_label=builder.get_object("apt_msg_label")
		self.package_msg_label=builder.get_object("package_msg_label")
		self.apply_changes_button=builder.get_object("apply_changes_button")
		self.package_list_entry=builder.get_object("package_list_entry")
		
		
		self.stack=Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.stack.set_transition_duration(250)
		hbox=Gtk.HBox()
		hbox.show()
		self.stack.add_titled(hbox,"empty","Empty Box")
		self.stack.add_titled(self.data_box,"apt_data","Apt Data Box")
		self.data_vp.add(self.stack)
		
		self.pack_start(self.main_box,True,True,0)
		
		
		self.connect_signals()
		self.set_css_info()
		
		self.core.current_var=None
		self.current_id=None
		
		self.thread=threading.Thread()
		self.thread_ret=None
		
		
		
	#def __init__
	

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("lliurex-remote-installer.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.package_label.set_name("OPTION_LABEL")
		self.url_label.set_name("OPTION_LABEL")
		
			
	#def set-css_info
	
	
	def connect_signals(self):
		
		self.add_apt_button.connect("clicked",self.add_apt_button_clicked)
		self.delete_apt_button.connect("clicked",self.delete_apt_button_clicked)
		self.add_package_button.connect("clicked",self.add_package_clicked)
		
		self.accept_add_package_button.connect("clicked",self.accept_add_package_button_clicked)
		self.cancel_add_package_button.connect("clicked",self.cancel_add_package_button_clicked)
		
		self.accept_apt_button.connect("clicked",self.accept_apt_button_clicked)
		self.cancel_apt_button.connect("clicked",self.cancel_apt_button_clicked)
		
		self.apply_changes_button.connect("clicked",self.apply_changes_button_clicked)
		self.url_entry.connect("changed",self.url_entry_changed)
		
		self.new_package_window.connect("delete_event",self.hide_window)
		self.new_apt_window.connect("delete_event",self.hide_window)
		
	#def connect_signals
	
	
	def hide_window(self,widget,event):
		
		widget.hide()
		return True
		
	#def new_package_window


	def check_changes(self,widget=True,event=True,manage_dialog=False):
		
		
		if not manage_dialog:
			if self.core.current_var==None:
				return False
			return self.core.current_var != self.core.var
		
		
		if self.core.current_var!=None and self.core.current_var != self.core.var:
			if not self.changes_detected_dialog(False):
				return True
		
		sys.exit(0)
			

	#def check_changes
		
	
	def set_info(self,info):
		
		#Empty list
		for x in self.list_box.get_children():
			self.list_box.remove(x)
		
		self.core.var=info
		
		times=1
		
		for t in range(0,times):
			if self.core.var["apt"] not in [{},"",None,'{}']:
				for x in self.core.var["apt"]:
					#Only show Mirror if exist in server
					if x in ['Mirror']:
						exists=self.core.n4d.lliurex_mirror()
						exists=exists[1]
						if exists.strip() == 'True':
							self.new_apt_button(x)
					else:
						self.new_apt_button(x)
			
		self.core.current_var=copy.deepcopy(self.core.var)
		self.list_box.show_all()
		

	#def set_info
	

	def new_apt_button(self,source_name):
		
		new_source_name=source_name
		
		if len(source_name) > 8:
			
			new_source_name=source_name[0:7]+"..."
		
		b=Gtk.Button(new_source_name)
		b.connect("clicked",self.apt_clicked,source_name)
		b.set_size_request(100,100)
		b.set_halign(Gtk.Align.START)
		b.set_name("OPTION_BUTTON")
		b.show_all()
		self.list_box.pack_start(b,False,False,5)
		b.queue_draw()
		b.set_tooltip_text(source_name)
		
		return b
		
	#def new_apt_button

	
	def new_package_button(self,pkg_name):
		
		hbox=Gtk.HBox()
		label=Gtk.Label(pkg_name)
		b=Gtk.Button()
		i=Gtk.Image.new_from_file("trash.svg")
		b.add(i)
		b.set_halign(Gtk.Align.CENTER)
		b.set_valign(Gtk.Align.CENTER)
		b.set_name("DELETE_ITEM_BUTTON")
		b.connect("clicked",self.delete_package_clicked,hbox)
		hbox.pack_start(label,False,False,0)
		hbox.pack_end(b,False,False,10)
		hbox.show_all()
		label.set_margin_right(20)
		label.set_margin_left(20)
		label.set_margin_top(20)
		label.set_margin_bottom(20)
		hbox.set_name("PKG_BOX")
		self.package_list_box.pack_start(hbox,False,False,5)
		self.package_list_box.queue_draw()
		hbox.queue_draw()
		
	#def new_package_button
	
	
	# ## APT ### ################################################
	
	def apt_clicked(self,widget,apt_id,ignore_changes=False):
		
		
		if not ignore_changes:
			
			if self.core.current_var!=None:
				if self.check_changes():
					if not self.changes_detected_dialog(False):
						return
			
			if apt_id !=self.current_id:
				self.core.current_var=copy.deepcopy(self.core.var)
				
		self.current_id=apt_id
		
		self.stack.set_visible_child_name("apt_data")

		for b in self.list_box.get_children():
			b.set_name("OPTION_BUTTON")
			
		widget.set_name("SELECTED_OPTION_BUTTON")
			
		
		for x in self.package_list_box.get_children():
			self.package_list_box.remove(x)
			
		self.url_entry.set_text(self.core.current_var["apt"][apt_id]["url"])
			
		for x in self.core.current_var["apt"][apt_id]["packages"]:
			self.new_package_button("%s"%x)
				
				
		self.package_list_box.show_all()
		
		if not ignore_changes:
		
			for apt in self.list_box:
				if apt.get_tooltip_text() not in self.core.current_var["apt"]:
					self.list_box.remove(apt)
			
		
		
		#self.core.lri.main_window.connect("delete_event",self.check_changes,True)
		
		
	#def apt_clicked
	
	def add_apt_button_clicked(self,widget):
		
		self.apt_name_entry.set_text("")
		self.apt_url_entry.set_text("")
		self.apt_msg_label.set_text("")
		self.new_apt_window.show()
		
	#def add_button_clicked
	
	
	def delete_apt_button_clicked(self,widget):
		
		if self.current_id==None:
			return
			
		if self.current_id in ['LliureX', 'Mirror']:
			return
		
		if self.delete_apt_dialog(self.current_id):
			for apt_button in self.list_box.get_children():
				
				if apt_button.get_tooltip_text() == self.current_id:
					self.list_box.remove(apt_button)
					self.stack.set_visible_child_name("empty")
					self.core.var["apt"].pop(self.current_id)
					self.current_id=None
					self.core.current_var=None
					self.core.n4d.set_variable(self.core.var)
		
	#def add_button_clicked
	
	def accept_apt_button_clicked(self,widget):
		
		
		name=self.apt_name_entry.get_text()
		source=self.apt_url_entry.get_text()
		
		if len(name) < 1 or len(source) < 8:
			self.apt_msg_label.set_markup("<span foreground='red'>"+"Invalid values"+"</span>")
			return
		if name in self.core.var["apt"]:
			self.apt_msg_label.set_markup("<span foreground='red'>"+"Apt name already exists"+"</span>")
			return
		
		if len(name) > 0 and len(source)>0 and name not in self.core.var:
			name=(name.lower())
			b=self.new_apt_button(name)
			
			if self.core.current_var ==None:
				self.core.current_var=copy.deepcopy(self.core.var)
				
			self.core.current_var["apt"][name]={}
			self.core.current_var["apt"][name]["packages"]=[]
			self.core.current_var["apt"][name]["url"]=source
			self.new_apt_window.hide()
			
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.var)
			
			self.apt_clicked(b,name,True)
			

		
	#def accept_apt_button_clicked
	
	
	def cancel_apt_button_clicked(self,widget):
		
		self.new_apt_window.hide()
		
	#def cancel_apt_button_clicked
	
	# #################################################### #####
	
	
	
	# #### PACKAGE CHANGES ################### #
	
	
	def add_package_clicked(self,widget):
		
		self.package_list_entry.set_text("")
		self.new_package_window.show()
		
	#def add_package_clicked
	
	
	def delete_package_clicked(self,button,hbox):
		
		pkg=hbox.get_children()[0].get_text()
		
		if self.delete_package_dialog(pkg):
		
			self.package_list_box.remove(hbox)
				
			for p in range(len(self.core.current_var["apt"][self.current_id]["packages"])-1,-1,-1):
				if self.core.current_var["apt"][self.current_id]["packages"][p]==pkg:
					self.core.current_var["apt"][self.current_id]["packages"].pop(p)
					self.core.var=self.core.current_var
					self.core.n4d.set_variable(self.core.var)
					
			# STORE VALUE IN N4D HERE IF NEEDED
			
			# ######### #
	
	#def delete_package_clicked
	
	
	def url_entry_changed(self,widget):
		
		if self.current_id in ['LliureX', 'Mirror']:
			return
		
		if self.core.current_var !=None:
			txt=widget.get_text()
			if len(txt)>6:
				self.core.current_var["apt"][self.current_id]["url"]=txt

	#def url_entry_changed	
	
	
	def accept_add_package_button_clicked(self,widget):
		
		
		self.package_list_entry.grab_focus()
		txt=self.package_list_entry.get_text()
		
		for pkg in txt.split(","):
			
			pkg=pkg.strip(" ")
			if pkg not in self.core.current_var["apt"][self.current_id]["packages"]:
				self.core.current_var["apt"][self.current_id]["packages"].append(pkg)
			self.new_package_button(pkg)
			
		self.new_package_window.hide()
		
	#def accept_add_package_button_clicked
	
	
	def cancel_add_package_button_clicked(self,widget):
		
		self.new_package_window.hide()
		
	#def cancel_add_package_button_clicked
	
	
	def apply_changes_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.apply_changes_thread)
		self.thread.daemon=True
		self.thread.start()
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ApplyingChangesDialog(main_window,"Lliurex Remote installer",_("Updating repositories and testing packages..."))
		dialog.show()
		GLib.timeout_add(500,self.check_apply_thread,dialog)
		
	#def apply_changes_button_clicked
	
	
	def apply_changes_thread(self):
		
		try:
			self.core.dprint("Updating repositories and testing packages...")
		
			# SAMPLE CODE
			
			#self.core.n4d.lliurex_version()
			#print "testeando....."
			#time.sleep(1.5)
			# ######### #
			#self.core.current_var=copy.deepcopy(self.core.var)
			self.core.var=copy.deepcopy(self.core.current_var)
			self.test_apt=self.core.n4d.test_apt_list(self.core.var)
			self.thread_ret={"status":True,"msg":"BROKEN"}
	
			# store return value here
			
			
			
		except Exception as e:
			print(e)
			return False
		
		
	#def apply_changes_thread
	
	def check_apply_thread(self,dialog):
		
		
		if self.thread.is_alive():
			return True
		
		dialog.destroy()
		
		#self.test_apt=[True,False, n4d_var, listado_apt_accesibles, listado_apt_no_instalbles, comentario]
		if self.test_apt[0]:
			if self.test_apt[3] not in [None,"","[]",[]]:
				if self.delete_test_apt_dialog(self.test_apt[3]):
					self.core.n4d.set_variable(self.test_apt[1])
					self.core.var=copy.deepcopy(self.test_apt[1])
					self.core.current_var=copy.deepcopy(self.test_apt[1])
				else:
					self.core.n4d.set_variable(self.core.var)
			else:
				self.core.n4d.set_variable(self.core.var)
			self.core.dprint("Done")
		else:
			self.core.dprint("Test Error: variable remains unset")
		
		
		for b in self.list_box:
			if b.get_tooltip_text()==self.current_id:
				break
		
		
		self.apt_clicked(b,self.current_id)
		
		
		
		if not self.thread_ret["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_ret["msg"])
			d.run()
			d.destroy()
		

		return False
		
	#def check_thread
	
	
	# ######################################################### #
	

	# ### DIALOGS ##### ##################
	
	def delete_apt_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		
		dialog=Dialog.QuestionDialog(main_window,_("Delete apt list"),_("Do you want to delete '%s' packages list?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	def delete_test_apt_dialog(self,pkg_name_orig):
		
		main_window=self.core.lri.main_window
		pkg_name='\n'.join(pkg_name_orig)
		dialog=Dialog.QuestionDialog(main_window,_("Delete apt list"),_("This pakage list is unavaiable from your repos:\n%s\nDo you want delete it?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	def delete_package_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Delete package"),_("Do you want to delete '%s'?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	def changes_detected_dialog(self,force_exit=False):
		
		main_window=self.core.lri.main_window
		
		dialog=Dialog.QuestionDialog(main_window,_("Changes detected"),_("There are unsaved changes. Do you want to discard them?"))
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			if force_exit:
				sys.exit(0)
				
			return True
		
		return False
		
	#def changes_detected_dialog
	
	# #####################################################
		
	
	
	
#class aptbox
