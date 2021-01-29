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
import textwrap

gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext


RSRC="./"


class ZeroBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"
		builder.add_from_file(ui_path)
		self.main_box=builder.get_object("zero_data_box")
		self.add_zero_button=builder.get_object("add_zero_button")
		self.package_label=builder.get_object("package_label_zero")
		self.package_list_box=builder.get_object("zero_list_box")
		self.package_list=builder.get_object("zero_list_box")
		self.data_vp=builder.get_object("zero_list_viewport")
		self.apply_zero_button=builder.get_object("apply_zero_button")

		self.new_zero_window=builder.get_object("new_zero_window")
		self.available_label_zero=builder.get_object("available_label_zero")
		self.entry_zero=builder.get_object("entry_zero")
		self.accept_add_zero_button=builder.get_object("accept_add_zero_button")
		self.cancel_add_zero_button=builder.get_object("cancel_add_zero_button")
		self.zero_list_available_viewport=builder.get_object("zero_list_available_viewport")
		self.zero_list_available_box=builder.get_object("zero_list_available_box")


		self.add(self.main_box)
		
		self.connect_signals()
		self.set_css_info()
		
		# Inicializamos la lista pero debe tener los valores que posee la variable global.
		self.zero_list_selected={}
		self.core.current_var=None
		self.current_id=None
		
		self.thread_zero=threading.Thread()
		self.thread_ret_zero=None
	#def __init__


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("lliurex-remote-installer.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.package_label.set_name("OPTION_LABEL")
		self.available_label_zero.set_name("OPTION_LABEL")
			
	#def set-css_info



	def connect_signals(self):
		
		self.add_zero_button.connect("clicked",self.add_zero_button_clicked)
		self.apply_zero_button.connect("clicked",self.apply_changes_button_clicked)
		self.entry_zero.connect("changed",self.entry_zero_changed)

		self.new_zero_window.connect("delete_event",self.hide_window)
		self.accept_add_zero_button.connect("clicked",self.accept_add_zero_button_clicked)
		self.cancel_add_zero_button.connect("clicked",self.cancel_add_zero_button_clicked)
		
		
	#def connect_signals





	def set_info(self,info):
		
		#Borramos la lista
		for c in self.package_list_box.get_children():
			self.package_list_box.remove(c)
			
		self.core.var=info
		self.core.current_var=copy.deepcopy(self.core.var)
		try:
			for key in self.core.current_var["epi"]["packages"]:
				#Esta lista contiene los paquetes preseleccionados para la ventana del add zmds
				self.zero_list_selected[key]=key
				#generamos los botonoes con la info de la variable {epi:{packages:{nombre_epi.epi:[nombre.deb,custom_name]}}}
				self.new_package_button(self.core.current_var["epi"]["packages"][key][1],key)
		except Exception as e:
			self.core.dprint("Global variable has error, delete & initialize it in ZMD values.")
			self.core.current_var["epi"]={}
			self.core.current_var["epi"]["packages"]={}
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.current_var)
			return False
		
	#def set_info


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



	def exec_list_init(self):
		
		try:
			self.new_zero
			return True
		except Exception as e:
			#print "inicializando variables de listas"
			self.new_zero=[]
			self.list_new_zero=[]
			return True
		
	#def exec_list_init


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


	# ##########################################
	# GENERACION VENTANA ADDONS ZERO INSTALLERS
	# ##########################################

	def hide_window(self,widget,event):
		
		widget.hide()
		return True
		
	#def new_package_window



	def add_zero_button_clicked(self,widget):
		
		try:
			#Borramos los elementos del Hbox de la pantalla principal
			for i in self.zero_list_available_box:
				self.zero_list_available_box.remove(i)
		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](generate_element_list) Error: %s"%e)
			return False

		self.thread_zero=threading.Thread(target=self.add_zero_button_clicked_thread)
		self.thread_zero.daemon=True
		self.thread_zero.start()

		
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ApplyingChangesDialog(main_window,"Lliurex Remote installer",_("Generating list ZMDs availables..."))
		dialog.show()
		GLib.timeout_add(500,self.check_add_zero_button_clicked_thread,dialog)		
	#def add_zero_button_clicked


	def add_zero_button_clicked_thread(self):
		
		try:
			self.core.dprint("Generating list ZMDs availables...")

			self.list_available=self.core.n4d.list_available_epis()
			# SOLUTION -> self.list_availabe=[True,epi_list,zmds,custom_names,zero_epi_dict]
			# zero_epi_dict -> Dictionary {epi_name{'zomando':"Name_zomando", 'custom_name':"Custon_name_zomando"}}
			
			self.thread_ret_zero={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](generate_element_list) Error: %s"%e)
			return False		
	#def add_zero_button_clicked_thread


	def check_add_zero_button_clicked_thread(self,dialog):
		
		
		if self.thread_zero.is_alive():
			return True
		#if thread ends dialog is destroyed
		dialog.destroy()

		if not self.thread_ret_zero["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_ret_zero["msg"])
			d.run()
			d.destroy()


		if self.list_available[0]:
			for key in self.list_available[4]:
				epi_name=key
				zomando=self.list_available[4][key]['zomando']
				custom_name=self.list_available[4][key]['custom_name']
				zmd_value=[epi_name,zomando,custom_name]
				self.generate_element_list(zmd_value)
			self.new_zero_window.show()
		else:
			#show error dialog
			#implement
			self.core.dprint("Test Error: variable remains unset")
		

		return False
		
	#def check_add_zero_button_clicked_thread





	def entry_zero_changed(self,widget):
		try:
			#Borramos los elementos del Hbox de la pantalla principal
			for i in self.zero_list_available_box:
				self.zero_list_available_box.remove(i)

			search_txt=self.entry_zero.get_text().lower().strip()

			if self.list_available[0]:
				for key in self.list_available[4]:
					epi_name=key
					zomando=self.list_available[4][key]['zomando']
					custom_name=self.list_available[4][key]['custom_name']
					custom_name_searched=custom_name.lower().strip()
					zmd_value=[epi_name,zomando,custom_name]
					if search_txt in custom_name_searched:
						self.generate_element_list(zmd_value)
				self.new_zero_window.show()
			else:
				#show error dialog
				#implement
				self.core.dprint("[LliureXRemoteInstaller][ZeroBox](entry_zero_changed) self.list_available variable remains unset")

		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](entry_zero_changed) Error: %s"%e)
			return False


	#def self.entry_zero_changed






	def generate_element_list(self,zmd_value):
		try:
			hbox=Gtk.HBox()
			zomando=zmd_value[2]
			if len(zomando) > 60:
				label_name=textwrap.wrap(zomando, width=60)[0]+'...'
				label=Gtk.Label(label_name)
			else:
				label=Gtk.Label(zomando)
			label.set_alignment(0,0)
			cb=Gtk.CheckButton()
			cb.set_halign(Gtk.Align.END)
			#cb.label=label.get_text()
			cb.data=zmd_value[0]
			hbox.pack_start(label,True,True,0)
			hbox.pack_end(cb,True,True,0)
			hbox.set_margin_left(10)
			hbox.set_margin_right(10)
			hbox.show_all()
			if zmd_value[0] in self.core.current_var["epi"]["packages"]:
				cb.set_active(True)

						
			tmp=Gtk.EventBox()
			tmp.add(hbox)
			tmp.show_all()
			tmp.add_events( Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK )
			tmp.connect("motion-notify-event",self.mouse_over_zmd)
			tmp.connect("leave_notify_event",self.mouse_left_zmd)
			self.zero_list_available_box.pack_start(tmp,False,False,5)

		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](generate_element_list) Error: %s"%e)
	#def generate_element_list



	def mouse_over_zmd(self,eb,event):

		eb.set_name("MOUSE_OVER")

	#def mouse_over_zmd


	def mouse_left_zmd(self,eb,event):

		eb.set_name("MOUSE_LEFT")

	#def mouse_left_zmd


	def cancel_add_zero_button_clicked(self,widget):
		
		self.new_zero_window.hide()
		
	#def cancel_add_package_button_clicked


	def accept_add_zero_button_clicked(self,widget):
		
		try:
			count=0
			#Borrar package_list_box antes de introducir los EPIS seleccionados.
			for c in self.package_list_box.get_children():
				self.package_list_box.remove(c)

			for i in self.zero_list_available_box:
				#print(self.zero_list_available_box.child_get(i))
				hbox=i.get_children()[0]
				label,cbox=hbox.get_children()
				#Add or delete items from dictionary
				if cbox.get_active():
					self.zero_list_selected[cbox.data]=[label.get_text()]
					self.new_package_button(label.get_text(),cbox.data)
					self.core.current_var['epi']['packages'][cbox.data]=['',label.get_text()]
				elif cbox.data in self.zero_list_selected:
					del self.zero_list_selected[cbox.data]
					del self.core.current_var['epi']['packages'][cbox.data]
			self.new_zero_window.hide()

		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](accept_add_zero_button_clicked) Error: %s"%e)
		
	#def accept_add_zero_button_clicked



	# #######################################################################
	# GENERACION HBOX EN PANEL PRINCIPAL CON LOS ZOMANDOS/EPI SELECCIONADOS
	# #######################################################################


	def new_package_button(self,pkg_name,epi_pkg):
		
		self.hbox_epi=Gtk.HBox()
		self.hbox_epi.epi=epi_pkg
		label=Gtk.Label(pkg_name)
		b=Gtk.Button()
		i=Gtk.Image.new_from_file("trash.svg")
		b.add(i)
		b.set_halign(Gtk.Align.CENTER)
		b.set_valign(Gtk.Align.CENTER)
		b.set_name("DELETE_ITEM_BUTTON")
		b.connect("clicked",self.delete_package_clicked,self.hbox_epi)
		self.hbox_epi.pack_start(label,False,False,0)
		self.hbox_epi.pack_end(b,False,False,10)
		self.hbox_epi.show_all()
		label.set_margin_right(20)
		label.set_margin_left(20)
		label.set_margin_top(20)
		label.set_margin_bottom(20)
		self.hbox_epi.set_name("PKG_BOX")
		self.package_list_box.pack_start(self.hbox_epi,False,False,5)
		self.package_list_box.queue_draw()
		self.hbox_epi.queue_draw()
		
	#def new_package_button


	# #### PACKAGE CHANGES ################### #
	
	
	def delete_package_clicked(self,button,hbox):
		
		pkg=hbox.get_children()[0].get_text()
		
		#Si borramos un zomando deberemos tambien de borrarlo de la lista inicial
		if self.delete_package_dialog(pkg):
			epi_pkg=hbox.epi
			self.package_list_box.remove(hbox)
			del self.zero_list_selected[epi_pkg]
			del self.core.current_var['epi']['packages'][epi_pkg]
		#Una vez eliminado el paquete debemos de bloquear el cambio de pantalla hasta el apply o regresar al estado inicial que se tenia.
			
			# ######### #
	#def delete_package_clicked




	def apply_changes_button_clicked(self,widget):
		
		self.thread_changes=threading.Thread(target=self.apply_changes_thread)
		self.thread_changes.daemon=True
		self.thread_changes.start()
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ApplyingChangesDialog(main_window,"Lliurex Remote installer",_("LlX Remote is adding zero-packages.\nUpdating variable,please wait..."))
		dialog.show()
		GLib.timeout_add(500,self.check_apply_thread,dialog)
	#def apply_changes_button_clicked
	



	def apply_changes_thread(self):
		
		try:
			self.core.dprint("LlX Remote is adding zero-packages. Updating variable,please wait...")
			self.list_epi_deb_selecteds={}
			self.list_epi_deb_failed={}
			#Para probar que falla la publicacion de la variable por fallo de un paquete uso la instruccion siguiente
			#self.list_epi_deb_failed['highschool.epi']=False
			for item in self.zero_list_selected:
				epi_deb=self.core.n4d.epi_deb(item)
				#epi_deb[TRUE/FALSE,"Nomb_paquete"\n]
				if epi_deb[0]:
					self.list_epi_deb_selecteds[item]=epi_deb[1]
					self.core.current_var['epi']['packages'][item][0]=epi_deb[1]
				else:
					self.list_epi_deb_failed[item]=False
					self.core.current_var['epi']['packages'][item][0]=False
			#Si no hay elementos fallidos publicamos la variable	
			if not self.list_epi_deb_failed:
				#print('Añadimos esto a la variable global en la seccion de epi-packages: %s'%self.list_epi_deb_selecteds)
				self.core.var=copy.deepcopy(self.core.current_var)
				self.core.n4d.set_variable(self.core.var)
			else:
				self.core.dprint("Sorry any ZMD can't determinate the DEB file %s"%self.list_epi_deb_failed)
			self.thread_changes_ret={"status":True,"msg":"BROKEN"}	
			
		except Exception as e:
			print(e)
			return False
	#def apply_changes_thread




	
	def check_apply_thread(self,dialog):
		
		if self.thread_changes.is_alive():
			return True
		
		dialog.destroy()		
		
		if not self.thread_changes_ret["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_changes_ret["msg"])
			d.run()
			d.destroy()

		print ('Thread del apply terminado')

		try:
			#Si hubo elementos fallidos	deberemos eliminar los zomandos que no se puden publicar
			#Mostramos un mensaje de fallo comunicandolo y preguntamos que hacer.
			if bool(self.list_epi_deb_failed):
				delete_epi_list=[]
				for key in self.list_epi_deb_failed:
					delete_epi_list.append(key)
				comment=_("This package list can't be published '%s'\nCan I delete it?")%delete_epi_list
				#Si se aceptan borrar los zomandos que no se pueden publicar deberemos borrarlos de la box principal y de la secundaria
				if self.error_epi_deb_dialog(comment):
					for c in self.package_list_box.get_children():
						if c.epi in self.list_epi_deb_failed:
							self.package_list_box.remove(c)
				#Box secundaria... quitando el checking, necesito un backup del diccionario para poder borrar los elementos.
					zero_list_selected_backup=self.zero_list_selected
					for d in self.list_epi_deb_failed:
						if d in zero_list_selected_backup:
							del self.zero_list_selected[d]
				# Una vez borrados podemos actualizar la variabel global.
				# Daremos un mensaje como que la hemos actualizado.
				else:
					#no publicar la variable y dejarla bloqueada hasta que se borren estos paquetes a mano
					#en la parte de borrado de paquetes deberemos comprobar que esto se ha hecho
					pass
		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](check_apply_thread) Error: %s"%e)
			
		return False
	#def check_thread
	

	# ######################################################### #
	
	
	# #### DIALOGS ################### #
	
	def delete_package_dialog(self,pkg_name):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Delete package"),_("Do you want to delete '%s'?")%pkg_name)
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_package_dialog



	def error_epi_deb_dialog(self,comment):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Delete package list"),comment)
		response=dialog.run()
		dialog.destroy()
				
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def error_epi_deb_dialog