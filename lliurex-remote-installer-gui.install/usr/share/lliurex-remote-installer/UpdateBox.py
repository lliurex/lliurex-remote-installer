import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

GObject.threads_init()
import copy
import gettext
import Core

import Dialog
import time
import threading
import sys
import os
import datetime

gettext.textdomain('lliurex-remote-installer-gui')
_=gettext.gettext

#Global Variables for thread
local_mirror=[False,'False']
net_mirror=[False,'False']

RSRC="./"

class WorkerThread(threading.Thread):
    def __init__(self, callback):
        
        self.core=Core.Core.get_core()
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
       # Simulate a long process, do your actual work here
        time.sleep(2)
        global local_mirror
        global net_mirror
        local_mirror=self.core.n4d.mirror_version()
        net_mirror=self.core.n4d.net_mirror_version()

        # The callback runs a GUI task, so wrap it!
        GObject.idle_add(self.callback)

#Class_WorkerThread


class UpdateBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-remote-installer-gui')
		ui_path=RSRC + "lliurex-remote-installer.ui"
		builder.add_from_file(ui_path)
		self.main_box=builder.get_object("update_data_box")
		self.update_current_box=builder.get_object("update_current_box")
		self.main_box=builder.get_object("update_data_box")
		self.update_sheduled_box=builder.get_object("update_sheduled_box")
		self.package_label=builder.get_object("package_label_update")
		self.update_frame=builder.get_object("update_frame")
		self.update_label_1=builder.get_object("update_label_1")
		self.update_label_2=builder.get_object("update_label_2")
		self.update_radiobutton_1=builder.get_object("update_radiobutton_1")
		self.update_radiobutton_2=builder.get_object("update_radiobutton_2")
		self.update_label_3=builder.get_object("update_label_3")
		self.update_label_4=builder.get_object("update_label_4")
		self.update_spinner_1=builder.get_object("update_spinner_1")
		self.update_spinner_2=builder.get_object("update_spinner_2")
		self.test_update_button=builder.get_object("test_update_mirrors")
		self.apply_update_button=builder.get_object("apply_update_button")
		
		

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
		self.update_label_1.set_name("OPTION_LABEL")
		self.update_label_2.set_name("OPTION_LABEL")
		
			
	#def set-css_info
	
	
	def set_info(self,info):
		
			
		self.core.var=info
		self.core.current_var=copy.deepcopy(self.core.var)
		self.update_spinner_1.start()
		self.update_spinner_2.start()
		
		#Make banner with information from n4d-var to sheduled update
		if self.core.var["update"]["activate"] == 'True':
			url_update=self.core.var["update"]["url"]
			version_update=self.core.var["update"]["version"].replace('Current version: ','')
			date_update=self.core.var["update"]["datetime"]
			self.new_package_button("True",url_update,version_update,date_update)
		else:
			self.new_package_button("False")
		
		#Asign information to radiobuttons
		self.update_radiobutton_1.set_label('Lliurex.net')
		self.update_radiobutton_2.set_label('Local Server Mirror')
		self.update_label_3.set_label('Current version: ')
		self.update_label_4.set_label('Current version: ')
		self.update_radiobutton_1.set_sensitive(False)
		self.update_radiobutton_2.set_sensitive(False)
		self.update_label_3.hide()
		self.update_label_4.hide()
		
		thread_spinner = WorkerThread(self.thread_stop)
		thread_spinner.start()

			
		#self.core.lri.main_window.connect("delete_event",self.check_changes,True)

	#def set_info
	
	def thread_stop(self):
		
		#When tread_start is finished this thread stop spinner and show the results
		
		global local_mirror
		global net_mirror
		
		self.update_spinner_1.stop()
		self.update_spinner_2.stop()
		
		#If local mirror exists show the version for it, if not exist is not avaiable from GUI
		if ( local_mirror[0] and local_mirror[1] not in ['False'] ):
			version=local_mirror[1]
			version='Current version: '+version
			self.update_label_4.set_label(version)
			self.update_label_4.show()
			self.update_radiobutton_2.set_sensitive(True)
			#self.update_spinner_2.hide()
		else:
			self.update_radiobutton_2.set_label('Mirror in Server is not avaiable')
			self.update_radiobutton_2.set_sensitive(False)
			self.update_label_4.hide()
			#self.update_spinner_2.hide()
			self.update_radiobutton_1.set_active(True)
			
		#If NET mirror exists show the version for it, if not exist is not avaiable from GUI
		if ( net_mirror[0] and net_mirror[1] not in ['False'] ):
			version=net_mirror[1]
			version='Current version: '+version
			self.update_label_3.set_label(version)
			self.update_label_3.show()
			self.update_radiobutton_1.set_sensitive(True)
			#self.update_spinner_1.hide()
		else:
			self.update_radiobutton_1.set_label('LliureX.net not avaiable')
			self.update_radiobutton_1.set_sensitive(False)
			self.update_label_3.hide()
			#self.update_spinner_1.hide()
			self.update_radiobutton_1.set_active(False)
			
	#def_thread_stop
	
	def new_package_button(self,activate='True',url_update='mirror',version_update='0',date_update='0'):
		
		hbox=Gtk.HBox()
		hbox.set_margin_left(15)
		hbox.set_margin_right(15)
		
		#Adding two or more line tags in hbox
		labels_box=Gtk.VBox()
		labels_box.set_valign(Gtk.Align.START)
		labels_box.set_halign(Gtk.Align.START)
		labels_box.set_margin_left(10)
		labels_box.set_margin_top(10)
		labels_box.set_margin_bottom(10)
		
		if activate=="True":
			sheduled="Sheduled on :"+date_update
			updated="Update to minimum version "+version_update+" from "+url_update+ " repository."
			
			label=Gtk.Label(sheduled)
			label.set_halign(Gtk.Align.START)
			label.set_valign(Gtk.Align.FILL)
			label2=Gtk.Label(updated)
			label2.set_halign(Gtk.Align.START)
			label2.set_valign(Gtk.Align.FILL)
			
			labels_box.pack_start(label,False,False,0)
			labels_box.pack_start(label2,False,False,0)
			
			b=Gtk.Button()
			i=Gtk.Image.new_from_file("trash.svg")
			b.add(i)
			b.set_halign(Gtk.Align.CENTER)
			b.set_valign(Gtk.Align.CENTER)
			b.set_name("DELETE_ITEM_BUTTON")
			b.connect("clicked",self.delete_update_clicked,hbox)
			
			hbox.pack_start(labels_box,False,False,0)
			
			
			hbox.pack_end(b,False,False,10)
			
		else:
			sheduled="Not sheduled updated activated"
			label=Gtk.Label(sheduled)
			label.set_halign(Gtk.Align.START)
			label.set_valign(Gtk.Align.FILL)
			labels_box.pack_start(label,False,False,0)
			hbox.pack_start(labels_box,False,False,0)
			
			
		hbox.show_all()
		
		hbox.set_name("PKG_BOX")
		self.update_current_box.pack_start(hbox,False,False,5)
		self.update_current_box.queue_draw()
		hbox.queue_draw()
		
	#def new_package_button
	
	
	def connect_signals(self):
		
		self.apply_update_button.connect("clicked",self.apply_update_button_clicked)
		self.test_update_button.connect("clicked",self.test_update_button_clicked)
		#self.add_deb_button.connect("clicked",self.add_update_button_clicked)
		
		#self.core.lri.main_window.connect("delete_event",self.check_changes,True)

	#def connect_signals

	
	
	# #### PACKAGE CHANGES ################### #
	
	
	def delete_update_clicked(self,button,hbox):
		
		
		if self.delete_update_dialog():
		
			self.update_current_box.remove(hbox)
			self.core.current_var["update"]["activate"]='False'
			self.new_package_button("False")
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.var)
			
	
	#def delete_update_clicked
	
	def apply_update_button_clicked(self,widget):
		
		if self.update_radiobutton_2.get_active():
			self.core.current_var["update"]["version"]=((self.update_label_4.get_label()).replace('Current version: ',''))
			if self.core.current_var["update"]["version"] == '':
				self.error_repos_dialog("Mirror")
				return True
		else:
			self.core.current_var["update"]["version"]=((self.update_label_3.get_label()).replace('Current version: ',''))
			if self.core.current_var["update"]["version"] == '':
				self.error_repos_dialog("Lliurex.net")
				return True
		
		self.thread=threading.Thread(target=self.apply_changes_thread)
		self.thread.daemon=True
		self.thread.start()
					
		#Se crea el mensaje de Apply segun:
		self.msg1=_("New sheduled are programed, applying changes.......")
		
		main_window=self.core.lri.main_window
		dialog=Dialog.ApplyingChangesDialog(main_window,title="Lliurex Remote Installer",msg=self.msg1)
		dialog.show()
		GLib.timeout_add(500,self.check_apply_thread,dialog)
		
	#def apply_changes_button_clicked
	
	
	def test_update_button_clicked(self,widget):
		
		self.update_spinner_1.start()
		self.update_spinner_2.start()
		self.update_radiobutton_1.set_label('Lliurex.net')
		self.update_radiobutton_2.set_label('Local Server Mirror')
		self.update_label_3.set_label('Current version: ')
		self.update_label_4.set_label('Current version: ')
		self.update_radiobutton_1.set_sensitive(False)
		self.update_radiobutton_2.set_sensitive(False)
		self.update_label_3.hide()
		self.update_label_4.hide()
		
		thread_spinner = WorkerThread(self.thread_stop)
		thread_spinner.start()
		
	#def apply_changes_button_clicked
	
	
	def apply_changes_thread(self):
		
		try:
			#'update':{'activate':'False', 'url':'Mirror', 'version':'0','datetime':'0'}
			self.core.dprint("Sheduled new update...")
			if self.update_radiobutton_2.get_active():
				self.core.current_var["update"]["activate"]='True'
				self.core.current_var["update"]["url"]='Mirror'
				self.core.current_var["update"]["version"]=((self.update_label_4.get_label()).replace('Current version: ',''))
				if self.core.current_var["update"]["version"] == '':
					dialog.destroy()
					self.error_repos_dialog()
					
				#datetime
				date=datetime.datetime.now()
				date_update=date.strftime("%d-%m-%Y %H:%M")
				self.core.current_var["update"]["datetime"]=date_update
			else:
				self.core.current_var["update"]["activate"]='True'
				self.core.current_var["update"]["url"]='Lliurex.net'
				self.core.current_var["update"]["version"]=((self.update_label_3.get_label()).replace('Current version: ',''))
				#datetime
				date=datetime.datetime.now()
				date_update=date.strftime("%d-%m-%Y %H:%M")
				self.core.current_var["update"]["datetime"]=date_update
			
			self.core.var=copy.deepcopy(self.core.current_var)
			self.core.n4d.set_variable(self.core.var)
			self.thread_ret={"status":True,"msg":"BROKEN"}

			
		except Exception as e:
			print(e)
			return False
		
		
	#def apply_changes_thread
	
	
	def check_apply_thread(self,dialog):
		
		
		if self.thread.is_alive():
			return True
		
		dialog.destroy()
		
		for child in self.update_current_box.get_children():
			self.update_current_box.remove(child)
		
		self.set_info(self.core.var)
		self.core.dprint("Done")
		
		if not self.thread_ret["status"]:
			mw=self.core.lri.main_window
			d=Dialog.ErrorDialog(mw,"",self.thread_ret["msg"])
			d.run()
			d.destroy()

		return False
		
	#def check_thread
	
	
	# #######  DIALOGS  ###############
	
	def delete_update_dialog(self):
		
		main_window=self.core.lri.main_window
		dialog=Dialog.QuestionDialog(main_window,_("Delete Update"),_("Do you want to delete scheduled update?"))
		response=dialog.run()
		dialog.destroy()
		
		if response== Gtk.ResponseType.OK:
			return True
		
		return False
		
	#def delete_update_dialog
	
	def error_repos_dialog(self, repo):
		comment=("%s repositorie not is accesible, please wait to connect with it or select other one"%repo)
		main_window=self.core.lri.main_window
		dialog=Dialog.ErrorDialog(main_window,_("Repositories Testing"),comment)
		response=dialog.run()
		dialog.destroy()
				
		return True
		
	#def remove_file_info_dialo
	