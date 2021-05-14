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
import os
import subprocess

_=gettext.gettext
gettext.textdomain('lliurex-remote-installer-gui')

RSRC="./"


class ExecBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"
		builder.add_from_file(ui_path)
		self.main_box=builder.get_object("exec_data_box")
		self.add_exec_button=builder.get_object("add_exec_button")
		self.package_label=builder.get_object("package_label_exec")
		self.package_list_box=builder.get_object("exec_list_box")
		self.package_list=builder.get_object("exec_list_box")
		self.data_vp=builder.get_object("exec_list_viewport")
		self.apply_exec_button=builder.get_object("apply_exec_button")
		
		

		self.add(self.main_box)
		
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
		
			
	#def set-css_info
	
	
	def set_info(self,info):
		
		#Empty list
		for c in self.package_list_box.get_children():
			self.package_list_box.remove(c)
			
		self.core.var=info
		self.core.current_var=copy.deepcopy(self.core.var)
		for (x,y) in self.core.var["sh"]["packages"]:
			self.new_package_button("%s"%x)
			
		
	#def set_info
	
	
	def connect_signals(self):
		
		
		self.add_exec_button.connect("clicked",self.add_exec_button_clicked)
		self.apply_exec_button.connect("clicked",self.apply_exec_button_clicked)
		
		
	#def connect_signals
	
	
	def exec_list_init(self):
		
		try:
			self.new_execs
			return True
		except Exception as e:
			#print "inicializando variables de listas"
			self.new_execs=[]
			self.list_new_execs=[]
			return True
		
	#def exec_list_init
	
	def check_user_desktop(self):
		
		path=os.path.expanduser("~/")
		
		try:
		
			f=open(os.path.expanduser("~/.config/user-dirs.dirs"))
			lines=f.readlines()
			f.close()
			
			for item in lines:
				if "XDG_DESKTOP_DIR" in item:
					first=item.find("/")+1
					last=item.rfind('"')
					path=path + item[first:last].strip("\n")
					
					
		except Exception as e:
			print(e,"!!!")
			
			
		return path
	
	
	def add_exec_button_clicked(self,widget):
		
		path=self.check_user_desktop()
		
		fcb=Dialog.FileDialog(self.core.lri.main_window,_("Please choose a file"), path)
		response=fcb.run()
		#Creo las listas de ayuda para anyadir paquetes si no existen antes
		self.exec_list_init()
		
		if response==Gtk.ResponseType.OK:
			exec_url=fcb.get_filename()
			fcb.destroy()
			pkg=os.path.basename(exec_url)
			lines=subprocess.Popen(["LAGUAGE=en_EN; md5sum %s | awk '{print $1}'"%exec_url],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
			for line in lines.splitlines():
				md5=line.decode('utf-8')
			pkg_tupla=[pkg,md5]
			#Compruebo si existe el paquete en la lista
			if any(pkg in element for element in self.core.current_var["sh"]["packages"]):
				#No es nuevo, compruebo si coincide su md5sum y lo apunto a subir de nuevo
				if pkg_tupla not in self.core.current_var["sh"]["packages"]:
					#he de eliminar la tupla de la lista que contiene mi elemento con mismo pkg pero con nuevo md5sum
					for i,[pkg_for,md5_for] in enumerate(self.core.current_var["sh"]["packages"]):
						if pkg == pkg_for:
							self.core.current_var["sh"]["packages"].pop(i)
					#self.core.current_var["sh"]["packages"].remove(pkg_tupla)
					self.core.current_var["sh"]["packages"].append(pkg_tupla)
					self.new_execs.append([pkg,exec_url])
					self.list_new_execs.append(pkg)
			else:
				self.core.current_var["sh"]["packages"].append(pkg_tupla)
				self.new_package_button(pkg)
				#print "paquete nuevo en lista, esta subido??"
				#Compruebo que es accesible via apache, sino lo apunto para copiar cuando aplique.
				exist_in_server=self.core.n4d.app_deb_exist(pkg, self.core.current_var["sh"]["url"])
				if not exist_in_server[0]:
					#print "No existe este exec lo debo de subir"
					self.new_execs.append([pkg,exec_url])
					self.list_new_execs.append(pkg)
					

			# ###### #
			#print self.core.current_var
			#print self.core.var
			return True
		else:
			fcb.destroy()
			return False
			
	#def add-exec_button_clicked
	
	
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
	
	
	
	# #### PACKAGE CHANGES ################### #
	
	
	def delete_package_clicked(self,button,hbox):
		
		pkg=hbox.get_children()[0].get_text()
		
		if self.delete_package_dialog(pkg):
			self.package_list_box.remove(hbox)
			
			for p in range(len(self.core.current_var["sh"]["packages"])-1,-1,-1):
				if self.core.current_var["sh"]["packages"][p][0]==pkg:
					self.core.current_var["sh"]["packages"].pop(p)
						
			#Compruebo que es accesible via apache, y pregunto si lo borro tambien del servidor
			exist_in_server=self.core.n4d.app_deb_exist(pkg, self.core.current_var["sh"]["url"])
			if exist_in_server[0]:
				if self.remove_file_dialog(pkg):
					self.thread=threading.Thread(target=self.delete_package_thread(pkg))
					self.thread.daemon=True
					self.thread.start()
					
					main_window=self.core.lri.main_window
					dialog=Dialog.ApplyingChangesDialog(main_window,title="Lliurex Remote Installer",msg=_("Deleting files......."))
					dialog.show()
					GLib.timeout_add(500,self.check_delete_thread,dialog)
			else:
				self.check_delete_thread
			
			# ######### #
	
	
	#def delete_package_clicked
	
	def delete_package_thread(self,pkg):
	
		try:
			self.core.dprint("Deleting file...")
	
			url_dest="/var/www/llx-remote/"+str(pkg)
			self.deleted=self.core.n4d.remove_file(url_dest)
			if not self.deleted[0]:
				comment=_("The file %s cannot be deleted")%pkg
				self.remove_file_info_dialog(comment)
				
			self.thread_ret={"status":True,"msg":"SE HA ROTO"}
			
		except Exception as e:
			print(e)
			return False
			
	#def delete_package_thread
	
	def check_delete_thread(self,dialog):
		
		if self.thread.is_alive():
			return True
		
		dialog.destroy()
		for c in self.package_list_box.get_children():
			self.package_list_box.remove(c)
		for (x,md5) in self.core.current_var["sh"]["packages"]:
			self.new_package_button("%s"%x)
		if self.deleted[0]:
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.var)
			
			
		
	#check_delete_thread
	
	
	def apply_exec_button_clicked(self,widget):
		
		self.exec_list_init()
		self.thread=threading.Thread(target=self.apply_changes_thread)
		self.thread.daemon=True
		self.thread.start()
		
		#Se crea el mensaje de Apply segun si sse suben ficheros o no.
		self.msg1=_("Applying changes.......")
		if  self.new_execs not in [None,"",[]]:
			self.msg1=_("Updating files and applying changes.......")
		else:
			self.msg1=_("Applying changes.......")
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ApplyingChangesDialog(main_window,title="Lliurex Remote Installer",msg=self.msg1)
		dialog.show()
		GLib.timeout_add(500,self.check_apply_thread,dialog)
		
	#def apply_changes_button_clicked
	
		
	
	def apply_changes_thread(self):
		
		try:
			
			print("(ExecBox)(apply_changes_thread) Testing.....")
			self.not_sended_execs=[]
			

			if  self.new_execs not in [None,"",[]]:
				self.core.dprint("Sending files to server...")
				for sh in self.new_execs:
					self.core.dprint("(ExecBox)(apply_changes_thread) Sending: %s"%sh)
					pkg=sh[0]
					exec_url=sh[1]
					if self.core.current_var["sh"]["url"] in [None,"",[]]:
						self.core.current_var["sh"]["url"]="http://server/llx-remote/"
					url_dest=self.core.current_var["sh"]["url"].split('http://server/')[1]
					url_dest="/var/www/"+str(url_dest)
					ip_dest=self.core.n4d.server_ip
					response=self.core.n4d.send_file(ip_dest,exec_url,url_dest)
					#Ha fallado la subida del fichero
					if not response:
						self.not_sended_execs.append(pkg)
						for (pkg_list,md5) in self.core.current_var["sh"]["packages"]:
							if pkg_list in {pkg}:
								self.core.current_var["sh"]["packages"].remove([pkg_list,md5])

				#Inicializo de nuevo la lista de paquetes, ya esta subido todo lo que se queria.
				self.new_execs=[]
				self.list_new_execs=[]
			
			self.core.dprint("(ExecBox)(apply_changes_thread) Applying changes...%s"%self.core.current_var)
			self.test_exec=self.core.n4d.test_list(self.core.current_var,'sh')
			self.core.var=copy.deepcopy(self.core.current_var)
			self.thread_ret={"status":True,"msg":"SE HA ROTO"}

			
		except Exception as e:
			print(e)
			return False
		
		
	#def apply_changes_thread
	
	def check_apply_thread(self,dialog):
		
		
		if self.thread.is_alive():
			return True
		
		dialog.destroy()
		#Se pudo testear la lista de execs, es un  [True,dict,list_execs_ok,list_execs_fail]
		if self.test_exec[0]:
			if self.test_exec[3] not in [None,"","[]",[]]:
				if self.delete_test_exec_dialog(self.test_exec[3]):
					self.core.n4d.set_variable(self.test_exec[1])
					self.core.var=copy.deepcopy(self.test_exec[1])
					self.core.current_var=copy.deepcopy(self.test_exec[1])
				else:
					self.core.var["sh"]["url"]="http://server/llx-remote/"
					self.core.n4d.set_variable(self.core.var)
			else:
					self.core.var["sh"]["url"]="http://server/llx-remote/"
					self.core.n4d.set_variable(self.core.var)
			
		else:
			self.core.dprint("Error en el test, no se guarda la variable")
			
		self.set_info(self.core.var)
		self.core.dprint("Done")
		
		if not self.thread_ret["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_ret["msg"])
			d.run()
			d.destroy()
		
		if self.not_sended_execs not in [None,"",[]]:
			self.error_send_dialog(self.not_sended_execs)
			
		return False
		
	#def check_thread
	
	
	# ######################################################### #
	
	
	# #### DIALOGS ################### #
	
	def error_send_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ErrorDialog(main_window,_("Sending Package Error"),_("This list %s cannot be sended to server\nPlease review your share directory\n\n/var/www/llx-remote")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		
		return True
		
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
	
	def remove_file_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Delete package"),_("IMPORTANT\nDo you want to delete this Executable from your server?\n'%s'")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def remove_file_dialog
	
	def remove_file_info_dialog(self,comment):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ErrorDialog(main_window,_("Delete package"),comment)
		response=dialog.run()
		dialog.destroy()
				
		return True
		
	#def remove_file_info_dialog
	
	def send_file_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Executable not in Server"),_("Do you want to send to the server this Executable '%s' ?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	def send_list_dialog(self,pkg_name_orig):
		main_window=self.core.lri.main_window
		pkg_name='\n'.join(pkg_name_orig)
		dialog=Dialog.QuestionDialog(main_window,_("Executable not in Server"),_("Do you want to send to the server this Executable list?\n%s\n")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def send_list_dialog
	
	
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
	
	
	
	def delete_test_exec_dialog(self,pkg_list_tupla):
		
		main_window=self.core.lri.main_window
		lista=[]
		for (pkg_name_orig,md5) in pkg_list_tupla:
			lista.append(pkg_name_orig)
		pkg_name='\n'.join(lista)
		dialog=Dialog.QuestionDialog(main_window,_("Delete Executable list"),_("This Executable list is unavaiable from your server:\n%s\nDo you want delete it?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	
#class execbox
