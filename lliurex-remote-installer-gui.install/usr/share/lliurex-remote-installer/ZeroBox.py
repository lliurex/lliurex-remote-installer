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
		self.epi_list_dict={}
		try:
			for key in self.core.current_var["epi"]["packages"]:
				#generamos los botones con la info de la variable {epi:{packages:{nombre_epi.epi:[nombre.deb,custom_name]}}}
				self.new_package_button(self.core.current_var["epi"]["packages"][key]['custom_name'],key)
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
			self.search_activate=False
			self.entry_zero.set_text('')
			#Borramos los elementos del Hbox de la pantalla principal
			for i in self.zero_list_available_box:
				self.zero_list_available_box.remove(i)
		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](generate_element_list) Error: %s"%e)
			return False

		self.search_activate=True

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
			# SOLUTION -> self.list_availabe=[True,epi_list_dict]
			# epi_list_dict -> Dictionary {'openboard.epi': {'selection_enabled': {'active': False, 'all_selected': False}, 'zomando': 'zero-lliurex-openboard', 'pkg_list': [{'custom_icon': '/usr/share/icons/lliurex/apps/48/openboard.svg', 'name': 'openboard', 'custom_name': 'openboard', 'default_pkg': False}]}}]

			#print (self.list_available[1])
			
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


		if self.list_available[0]:
			for element in self.list_available[1]:
				for key in element:
					#Dentro del EPI hay listas, si las hay debo ver todos sus elementos.
					if element[key]['selection_enabled']['active']:
						for pkg in element[key]['pkg_list']:
							clave_name=str(key)+'_'+pkg['name']
							epi_name=key
							pkg_name=pkg['name']
							custom_name=pkg['custom_name']
							self.add_element_to_epi_list_dict(clave_name,epi_name,pkg_name,custom_name)
							zmd_value=[clave_name,pkg_name,custom_name,epi_name]
							self.generate_element_list(zmd_value)
							#### Ahora tengo que modificar generate element_list y todo lo que conlleva llevando como referencia self.list_available CUIDADO con esto.
					else:
						pkg=element[key]['pkg_list'][0]
						clave_name=str(key)+'_'+pkg['name']
						epi_name=key
						pkg_name=pkg['name']
						custom_name=pkg['custom_name']
						self.add_element_to_epi_list_dict(clave_name,epi_name,pkg_name,custom_name)
						zmd_value=[clave_name,pkg_name,custom_name,epi_name]
						self.generate_element_list(zmd_value)

			self.new_zero_window.show()

		else:
			#show error dialog
			#implement
			self.core.dprint("Test Error: variable remains unset")
		

		if not self.thread_ret_zero["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_ret_zero["msg"])
			d.run()
			d.destroy()

		return False
		
	#def check_add_zero_button_clicked_thread





	def add_element_to_epi_list_dict(self,clave_name,epi_name,pkg_name,custom_name):
		try:
			self.epi_list_dict[clave_name]={}
			self.epi_list_dict[clave_name]['epi_name']=epi_name
			self.epi_list_dict[clave_name]['pkg_name']=pkg_name
			self.epi_list_dict[clave_name]['custom_name']=custom_name
			self.epi_list_dict[clave_name]['epi_deb_name']=''
			self.epi_list_dict[clave_name]['check']=''

		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](add_element_to_epi_list_dict) Error: %s"%e)
			return False


	# add_element_to_epi_list_dict



	def entry_zero_changed(self,widget):
		try:
			#Si estamos en la pantalla de busqueda sobre el listado cualquier cambio en la entrada debe hacer la acotacion de la busqueda sino no hara nada.
			if self.search_activate:
				#Borramos los elementos del Hbox de la pantalla principal
				for i in self.zero_list_available_box:
					self.zero_list_available_box.remove(i)

				search_txt=self.entry_zero.get_text().lower().strip()
				
				#self.epi_list_dict[clave_name]={epi_name,pkg_name,custom_name,epi_deb_name,check}
				if self.list_available[0]:
					for key in self.epi_list_dict:
						clave_name=key
						epi_name=self.epi_list_dict[key]['epi_name']
						pkg_name=self.epi_list_dict[key]['pkg_name']
						custom_name=self.epi_list_dict[key]['custom_name']
						custom_name_searched=custom_name.lower().strip()
						checking=self.epi_list_dict[key]['check']
						zmd_value=[clave_name,pkg_name,custom_name,epi_name,checking]
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
		#zmd_value=[clave_name,pkg_name,custom_name,epi_name,checking]
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
			cb.connect("clicked",self.check_clicked)
			hbox.pack_start(label,True,True,0)
			hbox.pack_end(cb,True,True,0)
			hbox.set_margin_left(10)
			hbox.set_margin_right(10)
			hbox.show_all()
			if zmd_value[0] in self.core.current_var["epi"]["packages"]:
				cb.set_active(True)
				self.epi_list_dict[zmd_value[0]]['check']=True
			else:
				try:
					if self.epi_list_dict[zmd_value[0]]['check']:
						cb.set_active(True)
					else:
						cb.set_active(False)
				except Exception as e:
					cb.set_active(False)

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

	
	def check_clicked(self,widget):

		if widget.get_active():
			self.epi_list_dict[widget.data]['check']=True
		else:
			self.epi_list_dict[widget.data]['check']=False
			if widget.data in self.core.current_var["epi"]["packages"]:
				del self.core.current_var["epi"]["packages"][widget.data]

	#def check_clicked




	def mouse_over_zmd(self,eb,event):

		eb.set_name("MOUSE_OVER")

	#def mouse_over_zmd



	def mouse_left_zmd(self,eb,event):

		eb.set_name("MOUSE_LEFT")

	#def mouse_left_zmd


	def cancel_add_zero_button_clicked(self,widget):

		self.search_activate=False
		self.new_zero_window.hide()
		
	#def cancel_add_package_button_clicked


	def accept_add_zero_button_clicked(self,widget):
		
		try:
			for c in self.package_list_box.get_children():
				self.package_list_box.remove(c)

			for key in self.epi_list_dict:
				clave_name=key
				zomando=self.epi_list_dict[key]['pkg_name']
				custom_name=self.epi_list_dict[key]['custom_name']
				epi_name=self.epi_list_dict[key]['epi_name']
				zmd_check=self.epi_list_dict[key]['check']
				#Add or delete items from dictionary
				if zmd_check:
					self.new_package_button(custom_name,clave_name)
					self.core.current_var['epi']['packages'][clave_name]=self.epi_list_dict[clave_name]
				else:
					if clave_name in self.core.current_var['epi']['packages']:
						del self.core.current_var['epi']['packages'][clave_name]

			self.search_activate=False
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
		
		try:
			pkg=hbox.get_children()[0].get_text()
		
			#Si borramos un zomando deberemos tambien de borrarlo de la lista inicial
			if self.delete_package_dialog(pkg):
				epi_pkg=hbox.epi
				self.package_list_box.remove(hbox)
				if epi_pkg in self.epi_list_dict:
					self.epi_list_dict[epi_pkg]['check']=False
				del self.core.current_var['epi']['packages'][epi_pkg]
			#Una vez eliminado el paquete debemos de bloquear el cambio de pantalla hasta el apply o regresar al estado inicial que se tenia.
		except Exception as e:
			self.core.dprint("[LliureXRemoteInstaller][ZeroBox](delete_package_clicked) Error: %s"%e)	
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
			#self.list_epi_deb_failed['stellarium.epi_stellarium']=False
			for item in self.core.current_var['epi']['packages']:
				epi_name=self.core.current_var['epi']['packages'][item]['epi_name']
				epi_deb=self.core.n4d.epi_deb(epi_name)
				#epi_deb[TRUE/FALSE,"Nomb_paquete"\n]
				if epi_deb[0]:
					self.list_epi_deb_selecteds[item]=epi_deb[1]
					self.core.current_var['epi']['packages'][item]['epi_deb_name']=epi_deb[1]
				else:
					self.list_epi_deb_failed[item]=False
					self.core.current_var['epi']['packages'][item]['epi_deb_name']=False
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

		try:
			#Si hubo elementos fallidos	deberemos eliminar los zomandos que no se puden publicar
			#Mostramos un mensaje de fallo comunicandolo y preguntamos que hacer.
			if bool(self.list_epi_deb_failed):
				delete_epi_list=[]
				for key in self.list_epi_deb_failed:
					delete_epi_list.append(key)
				comment=_("This package list can't be published '%s'\nCan I delete it?")%delete_epi_list
				#Si se aceptan borrar los zomandos que no se pueden publicar deberemos borrarlos de la box principal y de la secundaria en la current_var
				if self.error_epi_deb_dialog(comment):
					for c in self.package_list_box.get_children():
						if c.epi in self.list_epi_deb_failed:
							self.package_list_box.remove(c)
							del self.core.current_var['epi']['packages'][c.epi]

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