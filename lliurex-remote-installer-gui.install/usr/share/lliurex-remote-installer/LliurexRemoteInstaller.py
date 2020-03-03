import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib


import gettext
import signal

import Core
import Dialog
import sys
import time
import threading

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext


RSRC="./"



class LliurexRemoteInstaller:
	
	
	#VALORES DE LOS DICCIONARIOS
	DEB='deb'
	APT='apt'
	SH='sh'
	LIST='lista'
	URL='url'
	
	def __init__(self):
		
		self.core=Core.Core.get_core()
		
	#def init
	
	def load_gui(self):
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"
		builder.add_from_file(ui_path)
		
		self.main_window=builder.get_object("main_window")
		self.main_box=builder.get_object("main_box")
		self.apt_button=builder.get_object("apt_button")
		self.debs_button=builder.get_object("debs_button")
		self.exes_button=builder.get_object("exes_button")
		self.update_button=builder.get_object("update_button")
		
		
		#PANTALLA LOGIN
		self.login_da_box=builder.get_object("login_da_box")
		self.login_da=builder.get_object("login_drawingarea")
		#self.login_da.connect("draw",self.draw_login)
		
		self.login_overlay=Gtk.Overlay()
		self.login_overlay.add(self.login_da_box)
		
		self.login_box=builder.get_object("login_box")
		self.login_button=builder.get_object("login_button")
		self.user_entry=builder.get_object("user_entry")
		self.password_entry=builder.get_object("password_entry")
		self.login_eb_box=builder.get_object("login_eb_box")
		self.login_msg_label=builder.get_object("login_msg_label")
		self.server_ip_entry=builder.get_object("server_ip_entry")
		self.validate_spinner=builder.get_object("validate_spinner")
	
		self.login_overlay.add_overlay(self.login_box)
		self.login_overlay.show_all()
		
		
		#FIN LOGIN
		
		
		self.separator1=builder.get_object("separator1")
		self.separator3=builder.get_object("separator3")
		self.main_button_box=builder.get_object("box1")
		


		
		self.stack=Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_DOWN)
		self.stack.set_transition_duration(500)
		self.main_box.pack_start(self.stack,True,True,5)
		
		# Add components
		
		self.apt_box=self.core.apt_box
		self.stack.add_titled(self.apt_box,"apt","Apt")
		self.deb_box=self.core.deb_box
		self.stack.add_titled(self.deb_box,"debs","Debs")
		self.exec_box=self.core.exec_box
		self.stack.add_titled(self.exec_box,"exes","Executables")
		self.update_box=self.core.update_box
		self.stack.add_titled(self.update_box,"update","Update")
		
		self.stack.add_titled(self.login_overlay,"login","Login")
		
		self.set_css_info()
		self.connect_signals()
		#self.load_values()
		
		self.not_validate=True
		
		self.main_window.show_all()
		self.show_main_controls(False)
		self.validate_spinner.hide()
		
		
		
	#def load_gui
	
	
	def show_main_controls(self,status):
		
		if status:
			self.separator1.show()
			self.separator3.show()
			self.main_button_box.show()
		else:
			self.separator1.hide()
			self.separator3.hide()
			self.main_button_box.hide()
		
	#def show_main_controls
	
	
	
	def load_values(self):
		
		
		
		self.core.n4d.test_var()
		var_init=self.core.n4d.get_variable()
		if var_init[0]:
			variable=var_init[1]
		else:
			pass
			# #### LA VARIABLE NO EXISTE DEBEMOS DE INCIALIZARLA INICIALMENTE PARA QUE NO DE ERROR, AUNQUE CREO QUE ESO YA LO HACE LA API.
		
		var={}
		var=variable
		
		self.apt_box.set_info(var)
		self.deb_box.set_info(var)
		self.exec_box.set_info(var)
		self.update_box.set_info(var)
		
		
		
	#def load_values
	
	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("lliurex-remote-installer.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.main_window.set_name("WINDOW")
		
		self.apt_button.set_name("SELECTED_OPTION_BUTTON")
		self.debs_button.set_name("OPTION_BUTTON")
		self.exes_button.set_name("OPTION_BUTTON")
		self.update_button.set_name("OPTION_BUTTON")
		self.login_msg_label.set_name("ERROR_LABEL")
			
	#def set-css_info
	
	def connect_signals(self):
		
		self.main_window.connect("destroy",self.check_changes)
		#self.main_window.connect("destroy",Gtk.main_quit)
		self.apt_button.connect("clicked",self.apt_button_clicked)
		self.debs_button.connect("clicked",self.debs_button_clicked)
		self.exes_button.connect("clicked",self.exes_button_clicked)
		self.update_button.connect("clicked",self.update_button_clicked)
		self.main_window.connect("delete_event",self.check_changes)
		
		self.user_entry.connect("activate",self.entries_press_event)
		self.password_entry.connect("activate",self.entries_press_event)
		self.server_ip_entry.connect("activate",self.entries_press_event)
		self.login_button.connect("clicked",self.validate_user)
		
	#def connect_signals
	
	def entries_press_event(self,widget):
		
		self.validate_user(None)
		
	#def entries_press_event

	
	
	def validate_user_thread(self):
		
		user=self.user_entry.get_text()
		password=self.password_entry.get_text()
		
		
		# DELETE ME
		'''if user=="":
			user="lliurex"
		if password=="":
			password="lliurex"
		'''
		self.login_ret=self.core.n4d.validate_user(user,password,self.server_ip_entry.get_text())
		
	#def validate_user_thread
		
	
	def validate_user(self,widget):
		
		self.login_msg_label.hide()
		self.validate_spinner.show()
		
		self.login_button.set_sensitive(False)
		
		self.thread=threading.Thread(target=self.validate_user_thread)
		self.thread.daemon=True
		self.thread.start()

		GLib.timeout_add(500,self.validate_user_thread_listener)
		
		
	#def validate_user
	
	def validate_user_thread_listener(self):
		
		if self.thread.is_alive():
			return True
		
		if not self.login_ret[0]:
			self.login_msg_label.set_text("%s"%self.login_ret[1])
			self.validate_spinner.hide()
			self.login_msg_label.show()
			self.login_button.set_sensitive(True)

		else:
			
			self.load_values()
			self.stack.set_visible_child_name("apt")
			self.show_main_controls(True)
			self.not_validate=False
		
		return False
		
		
		
	#def validate_user_thread
	
	def check_changes(self,widget,event):
		
		
		if self.not_validate:
			sys.exit(0)
		
		if self.core.current_var!=None and self.core.current_var != self.core.var:
			if not self.changes_detected_dialog():
				return True
		#Listamos lo que se ha publicado:
		COMMENT=[]

		apt_list=False
		list_apt_pub=[]
		for id in self.core.var['apt']:
			if self.core.var['apt'][id]['packages'] not in [None,"",[],"[]"]:
				apt_list=True
				for pkg in self.core.var['apt'][id]['packages']:
					list_apt_pub.append(pkg)
		if apt_list:
			COMMENT.append("APT:")
			COMMENT=COMMENT+list_apt_pub
			COMMENT.append("")
		if self.core.var['deb']['packages'] not in [None,"",[],"[]"]:
			COMMENT.append("DEB:")
			COMMENT=COMMENT+self.core.var['deb']['packages']
			COMMENT.append("")
		if self.core.var['sh']['packages'] not in [None,"",[],"[]"]:
			COMMENT.append("EXECUTABLES:")
			pkg_list=[]
			for (pkg,md5) in self.core.var['sh']['packages']:
				pkg_list.append(pkg)
			COMMENT=COMMENT+pkg_list
		if self.core.var['update']['activate'] == "True":
			COMMENT.append("UPDATE: Sheduled from "+self.core.var['update']['url'])
			COMMENT.append("Minimum update version: "+(self.core.var['update']['version']))
			#COMMENT.append(self.core.var['update']['url'])
			COMMENT.append("")
		if COMMENT not in [None,"",[]]:
			COMMENT='\n'.join(COMMENT)
			dialog=Dialog.InfoDialog(self.main_window,_("LliureX Remote Installer Summary"),_("You published this list to install:\n\n%s")%(COMMENT))
			response=dialog.run()
			dialog.destroy()
		
		
		sys.exit(0)
		
	#def check_changes
	
	
	def changes_detected_dialog(self):
		
		
		dialog=Dialog.QuestionDialog(self.main_window,_("Changes detected"),_("There are unsaved changes. Do you want to discard them?"))
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def changes_detected_dialog
		
	
	
	def start_gui(self):
		
		GObject.threads_init()
		Gtk.main()
		
	#def start_gui
	
	def apt_button_clicked(self,widget):
		
		change_child=True
		if self.stack.get_visible_child_name()=="debs":
			selected="deb"
		if self.stack.get_visible_child_name()=="exes":
			selected="sh"
		if self.stack.get_visible_child_name()=="update":
			selected="update"
			
			
		if self.stack.get_visible_child_name()=="debs":
			if self.deb_box.check_changes():
				change_child=self.deb_box.changes_detected_dialog()
				if change_child:
					self.deb_box.set_info(self.core.var)
					
					for c in self.deb_box.package_list_box.get_children():
						self.deb_box.package_list_box.remove(c)
			
					for x in self.core.var[selected]["packages"]:
						self.deb_box.new_package_button("%s"%x)
						
		if self.stack.get_visible_child_name()=="exes":
			if self.exec_box.check_changes():
				change_child=self.exec_box.changes_detected_dialog()
				if change_child:
					self.exec_box.set_info(self.core.var)
					
					for c in self.exec_box.package_list_box.get_children():
						self.exec_box.package_list_box.remove(c)
			
					for x in self.core.var[selected]["packages"]:
						self.exec_box.new_package_button("%s"%x)
					
					
					#self.apt_box.stack.set_visible_child_name("empty
		if change_child:
			self.apt_box.set_info(self.core.var)
			self.stack.set_visible_child_name("apt")
			self.apt_button.set_name("SELECTED_OPTION_BUTTON")
			self.debs_button.set_name("OPTION_BUTTON")
			self.exes_button.set_name("OPTION_BUTTON")
			self.update_button.set_name("OPTION_BUTTON")
		
	#def apt_button_clicked
	
	def debs_button_clicked(self,widget):
		
		change_child=True
		
		if self.stack.get_visible_child_name()=="apt":
			if self.apt_box.check_changes():
				change_child=self.apt_box.changes_detected_dialog()
				if change_child:
					self.apt_box.set_info(self.core.var)
					apt_id=self.apt_box.current_id
					self.apt_box.url_entry.set_text(self.core.var["apt"][apt_id]["url"])
					
					for x in self.apt_box.package_list_box.get_children():
						self.apt_box.package_list_box.remove(x)
			
					for x in self.core.var["apt"][apt_id]["packages"]:
						self.apt_box.new_package_button("%s"%x)
						
		if self.stack.get_visible_child_name()=="exes":
			if self.exec_box.check_changes():
				change_child=self.exec_box.changes_detected_dialog()
				if change_child:
					self.exec_box.set_info(self.core.var)
					
					for c in self.exec_box.package_list_box.get_children():
						self.exec_box.package_list_box.remove(c)
			
					for x in self.core.var["sh"]["packages"]:
						self.exec_box.new_package_button("%s"%x)
			
					
					
					#self.apt_box.stack.set_visible_child_name("empty")
			
			
		
		if change_child:
			self.deb_box.set_info(self.core.var)
			self.stack.set_visible_child_name("debs")
			self.apt_button.set_name("OPTION_BUTTON")
			self.debs_button.set_name("SELECTED_OPTION_BUTTON")
			self.exes_button.set_name("OPTION_BUTTON")
			self.update_button.set_name("OPTION_BUTTON")
		
	#def debs_button_clicked
	
	def exes_button_clicked(self,widget):
		
		change_child=True
		
		if self.stack.get_visible_child_name()=="apt":
			if self.apt_box.check_changes():
				change_child=self.apt_box.changes_detected_dialog()
				if change_child:
					self.apt_box.set_info(self.core.var)
					apt_id=self.apt_box.current_id
					self.apt_box.url_entry.set_text(self.core.var["apt"][apt_id]["url"])
					
					for x in self.apt_box.package_list_box.get_children():
						self.apt_box.package_list_box.remove(x)
			
					for x in self.core.var["apt"][apt_id]["packages"]:
						self.apt_box.new_package_button("%s"%x)
						
		if self.stack.get_visible_child_name()=="debs":
			if self.deb_box.check_changes():
				change_child=self.deb_box.changes_detected_dialog()
				if change_child:
					self.deb_box.set_info(self.core.var)
					
					for c in self.deb_box.package_list_box.get_children():
						self.deb_box.package_list_box.remove(c)
			
					for x in self.core.var["deb"]["packages"]:
						self.deb_box.new_package_button("%s"%x)
			
					
					
					#self.apt_box.stack.set_visible_child_name("empty")
			
			
		
		if change_child:
		
			self.stack.set_visible_child_name("exes")
			self.apt_button.set_name("OPTION_BUTTON")
			self.debs_button.set_name("OPTION_BUTTON")
			self.exes_button.set_name("SELECTED_OPTION_BUTTON")
			self.update_button.set_name("OPTION_BUTTON")
		
	#def exes_button_clicked
	
	
	def update_button_clicked(self,widget):
		
		change_child=True
		
		if self.stack.get_visible_child_name()=="apt":
			if self.apt_box.check_changes():
				change_child=self.apt_box.changes_detected_dialog()
				if change_child:
					self.apt_box.set_info(self.core.var)
					apt_id=self.apt_box.current_id
					self.apt_box.url_entry.set_text(self.core.var["apt"][apt_id]["url"])
					
					for x in self.apt_box.package_list_box.get_children():
						self.apt_box.package_list_box.remove(x)
			
					for x in self.core.var["apt"][apt_id]["packages"]:
						self.apt_box.new_package_button("%s"%x)
		
		if self.stack.get_visible_child_name()=="debs":
			if self.deb_box.check_changes():
				change_child=self.deb_box.changes_detected_dialog()
				if change_child:
					self.deb_box.set_info(self.core.var)
					
					for c in self.deb_box.package_list_box.get_children():
						self.deb_box.package_list_box.remove(c)
			
					for x in self.core.var["deb"]["packages"]:
						self.deb_box.new_package_button("%s"%x)
						
		if self.stack.get_visible_child_name()=="exes":
			if self.exec_box.check_changes():
				change_child=self.exec_box.changes_detected_dialog()
				if change_child:
					self.exec_box.set_info(self.core.var)
					
					for c in self.exec_box.package_list_box.get_children():
						self.exec_box.package_list_box.remove(c)
			
					for x in self.core.var["sh"]["packages"]:
						self.exec_box.new_package_button("%s"%x)
			
					
					
					#self.apt_box.stack.set_visible_child_name("empty")
			
			
		
		if change_child:
			#self.update_box.set_info(self.core.var)
			self.stack.set_visible_child_name("update")
			self.apt_button.set_name("OPTION_BUTTON")
			self.debs_button.set_name("OPTION_BUTTON")
			self.exes_button.set_name("OPTION_BUTTON")
			self.update_button.set_name("SELECTED_OPTION_BUTTON")
		
	#def update_button_clicked
	
#class LliurexRemoteInstaller


if __name__=="__main__":
	
	lri=LliurexRemoteInstaller()
	lri.start_gui()
	
