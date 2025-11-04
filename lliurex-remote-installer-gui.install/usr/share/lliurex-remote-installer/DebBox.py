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

import xmlrpc.client
import ssl

gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext


RSRC="./"


class DebBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"
		builder.add_from_file(ui_path)
		self.main_box=builder.get_object("deb_data_box")
		self.add_deb_button=builder.get_object("add_deb_button")
		self.package_label=builder.get_object("package_label_deb")
		self.package_list_box=builder.get_object("deb_list_box")
		self.package_list=builder.get_object("deb_list_box")
		self.data_vp=builder.get_object("deb_list_viewport")
		self.apply_deb_button=builder.get_object("apply_deb_button")
		
		
		self.server="localhost"
		self.context=ssl._create_unverified_context()
		self.client=xmlrpc.client.ServerProxy("https://%s:9779"%self.server,allow_none=True,context=self.context)

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
		for x in self.core.var["deb"]["packages"]:
			self.new_package_button("%s"%x)
			
		#self.core.lri.main_window.connect("delete_event",self.check_changes,True)

	#def set_info
	
	
	def connect_signals(self):
		
		
		self.add_deb_button.connect("clicked",self.add_deb_button_clicked)
		self.apply_deb_button.connect("clicked",self.apply_deb_button_clicked)
		#self.core.lri.main_window.connect("delete_event",self.check_changes,True)
		
	#def connect_signals
	
	
	def deb_list_init(self):
		
		try:
			self.new_debs
			return True
		except Exception as e:
			#print "inicializando variables de listas"
			self.new_debs=[]
			self.list_new_debs=[]
			return True
		
	#def deb_list_init
	
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
	
	
	def add_deb_button_clicked(self,widget):
		
		path=self.check_user_desktop()
		#print path
		fcb=Dialog.FileDialog(self.core.lri.main_window,_("Please choose a file"), path)
		response=fcb.run()
		
		self.deb_list_init()
		
		if response==Gtk.ResponseType.OK:
			deb_url=fcb.get_filename()
			fcb.destroy()
			pkg=os.path.basename(deb_url)
			extension=os.path.splitext(pkg)[1]
			if extension not in [".deb",".DEB"]:
				self.error_extension_dialog(pkg)
				fcb.destroy()
				return False
			#Compruebo si es un paquete nuevo de la lista
			if pkg not in self.core.current_var["deb"]["packages"]:
				self.core.current_var["deb"]["packages"].append(pkg)
				self.new_package_button(pkg)
				#print "paquete nuevo en lista, esta subido??"
				#Compruebo que es accesible via apache, sino lo apunto para copiar cuando aplique.
				exist_in_server=self.core.n4d.app_deb_exist(pkg, self.core.current_var["deb"]["url"])
				self.core.dprint("(DebBox)(add_deb_button_clicked) self.core.n4d.app_deb_exist: %s"%exist_in_server)
				if not exist_in_server[0]:
					#print "No existe este deb lo debo de subir"
					self.core.dprint("(DebBox)(add_deb_button_clicked) Package %s marked to upload to server"%pkg)
					self.new_debs.append([pkg,deb_url])
					self.list_new_debs.append(pkg)
					

			# ###### #
			
			return True
		else:
			fcb.destroy()
			return False
			
	#def add-deb_button_clicked
	
	
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
			
			for p in range(len(self.core.current_var["deb"]["packages"])-1,-1,-1):
				if self.core.current_var["deb"]["packages"][p]==pkg:
					self.core.current_var["deb"]["packages"].pop(p)
			#Compruebo que es accesible via apache, y pregunto si lo borro tambien del servidor
			exist_in_server=self.core.n4d.app_deb_exist(pkg, self.core.current_var["deb"]["url"])
			if exist_in_server[0]:
				self.thread=threading.Thread(target=self.delete_package_thread(pkg))
				self.thread.daemon=True
				self.thread.start()
				
				main_window=self.core.lri.main_window
				dialog=Dialog.ApplyingChangesDialog(main_window,title="Lliurex Remote Installer",msg=_("Deleting files......."))
				dialog.show()
				GLib.timeout_add(500,self.check_delete_thread,dialog)
			
			# ######### #
	
	
	#def delete_package_clicked
	
	def delete_package_thread(self,pkg):
	
		try:
			self.core.dprint("Deleting file...")

			#OLD DELETE MODE
			#url_dest="/var/www/llx-remote/"+str(pkg)
			#self.deleted=self.core.n4d.remove_file(url_dest)

			var_dest="llx-remote"
			package_list=self.client.get_download_list()
			self.core.dprint("[DebBox][delete_package_thread] Package to delete:%s"%pkg)
			self.core.dprint("[DebBox][delete_package_thread] Reading shared package_list:%s"%package_list)
			url_dest=""
			for elem in package_list['return'][var_dest]:
				if pkg in elem:
					self.core.dprint("[DebBox][delete_package_thread] Deleting elem:%s"%elem)
					url_dest=elem

			self.deleted=self.core.n4d.delete_download(var_dest,url_dest)


			if not self.deleted["return"]:
				comment=_("The file %s cannot be deleted")%pkg
				self.remove_file_info_dialog(comment)
			else:
				self.core.dprint("[DebBox][delete_package_thread] Removing file :%s"%url_dest)
				os.remove(url_dest)

				
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
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
			
		for x in self.core.current_var["deb"]["packages"]:
			self.new_package_button("%s"%x)
		if self.deleted["return"]:
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.var)
			
			
		
	#check_delete_thread
	
	
	def apply_deb_button_clicked(self,widget):
		
		self.deb_list_init()
		self.thread=threading.Thread(target=self.apply_changes_thread)
		self.thread.daemon=True
		self.thread.start()
		
		#Se crea el mensaje de Apply segun si sse suben ficheros o no.
		self.msg1=_("Applying changes.......")
		if  self.new_debs not in [None,"",[]]:
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
			
			print("[DebBox] Testing.....")
			if  self.new_debs not in [None,"",[]]:
				self.core.dprint("[DebBox] Sending files to server...")
				for deb in self.new_debs:

					pkg=deb[0]
					deb_url=deb[1]
					url_dest="/var/www/"
					var_dest="llx-remote"

					#OLD UPLOAD FILES
					#if self.core.current_var["deb"]["url"] in [None,"",[]]:
					#	self.core.current_var["deb"]["url"]=url_dest
					#url_dest=self.core.current_var["deb"]["url"].split('http://server/')[1]
					#ip_dest=self.core.n4d.server_ip
					

					url_dest=url_dest+str(var_dest)
					uploaded=self.core.n4d.send_file(self.server,deb_url,url_dest)
					self.core.dprint("[DebBox][apply_changes_thread] CORE:N4D.SEND_FILE: %s"%uploaded)

					if uploaded:
						url_deb=url_dest+'/'+str(pkg)
						self.core.dprint("[DebBox][apply_changes_thread] URL_DEB to share with add download: %s"%url_deb)
						uploaded=self.core.n4d.add_download(var_dest,url_deb)
						self.core.dprint("[DebBox][apply_changes_thread] N4D Uploaded: %s"%uploaded)

					if not uploaded["return"]:
						self.error_up_dialog(pkg)


				#Inicializo de nuevo la lista de paquetes, ya esta subido todo lo que se queria.
				self.new_debs=[]
				self.list_new_debs=[]
			self.core.dprint("Applying changes...")
			self.core.var=copy.deepcopy(self.core.current_var)
			self.test_deb=self.core.n4d.test_deb_list(self.core.var)
			self.thread_ret={"status":True,"msg":"BROKEN"}

			
		except Exception as e:
			print(e)
			return False
		
		
	#def apply_changes_thread
	
	def check_apply_thread(self,dialog):
		
		
		if self.thread.is_alive():
			return True
		
		dialog.destroy()
		#Se pudo testear la lista de debs, es un  [True,dict,list_debs_ok,list_debs_fail]
		self.core.dprint("[DebBox][check_apply_thread] test_deb: %s"%self.test_deb)
		self.core.dprint("[DebBox][check_apply_thread] DEBS to add: %s"%self.test_deb[2])
		self.core.dprint("[DebBox][check_apply_thread] DEBS fail: %s"%self.test_deb[3])
		if self.test_deb[0]:
			if self.test_deb[3] not in [None,"","[]",[]]:
				if self.delete_test_deb_dialog(self.test_deb[3]):
					self.core.n4d.set_variable(self.test_deb[1])
					self.core.var=copy.deepcopy(self.test_deb[1])
					self.core.current_var=copy.deepcopy(self.test_deb[1])
				else:
					self.core.var["deb"]["url"]="https://server:9779/llx-remote/"
					self.core.n4d.set_variable(self.core.var)
			else:
					self.core.var["deb"]["url"]="https://server:9779/llx-remote/"
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
		

		return False
		
	#def check_thread
	
	
	# ######################################################### #
	
	
	# #### DIALOGS ################### #
	
	def error_extension_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ErrorDialog(main_window,_("Error in Extension"),_("This %s package has not the extension required.\nPlease only DEB packages in this list.")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		
		return True
		
	#def delete_package_dialog


	def error_up_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ErrorDialog(main_window,_("Error in publishing"),_("This %s package can't be uploaded to server.\nPlease review the parameters or inform to LliureX Team.")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		
		return True
		
	#def error_up_dialog
	
	
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
		dialog=Dialog.QuestionDialog(main_window,_("Delete package"),_("IMPORTANT\nDo you want to delete this DEB from your server?\n'%s'")%pkg_name)
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
		dialog=Dialog.QuestionDialog(main_window,_("DEB not in Server"),_("Do you want to send to the server this DEB '%s' ?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	def send_list_dialog(self,pkg_name_orig):
		main_window=self.core.lri.main_window
		pkg_name='\n'.join(pkg_name_orig)
		dialog=Dialog.QuestionDialog(main_window,_("DEB not in Server"),_("Do you want to send to the server this DEB list?\n%s\n")%pkg_name)
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
	
	
	
	def delete_test_deb_dialog(self,pkg_name_orig):
		
		main_window=self.core.lri.main_window
		pkg_name='\n'.join(pkg_name_orig)
		dialog=Dialog.QuestionDialog(main_window,_("Delete deb list"),_("This DEB list is unavaiable from your server:\n%s\nDo you want delete it?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog
	
	
#class debbox
