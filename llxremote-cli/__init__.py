#!/usr/bin/env python3
import ssl
import xmlrpc.client as x
import sys
import subprocess
import datetime
import os
import getpass
import n4d.client

class REMOTE(object):
	REMOTE_VAR="LLX_REMOTE_INSTALLER"
	programmed_apt=None
	programmed_deb=None
	programmed_sh=None
	programmed_zero=None
	programmed_update=None
	dbg=False


	def __init__(self,dbg,usr='netadmin',passwd='None'):
		context=ssl._create_unverified_context()
		self.proxy="https://server:9779"
		#New N4D
		#self.client=x.ServerProxy(proxy,allow_none=True,context=context)
		#self.user=usr
		#self.pswd=passwd
		if dbg:
			self.dbg=True
			print ("")
			print ("-----------------------------------------------------" )
			print ("")
			print ("[LLXRemoteInstallerCLI] DEBUG_MODE ACTIVATED" )
			print ("")
			print ("-----------------------------------------------------" )
			print ("")
		pass
	#def __init__




	def _debug(self,msg):
		if self.dbg:
			print("[LlxRemote Cli] %s"%msg)
	#def _debug



	def read_n4dkey(self):
		try:
			#f=open("/etc/n4d/key")
			#key=f.readline().strip("\n")
			#f.close()
			if self.pswd == 'None':
				self.user='netadmin'
				self.pswd = getpass.getpass('Please type NETADMIN password or cancel to change user: ')
				if self.pswd == 'cancel':
					self.user = getpass.getpass('Please type user with netadmin permissions: ')
					self.pswd = getpass.getpass('Please type password: ')
			#key=(self.user,self.pswd)
			print('testing user and passwd, please wait...')
			self.client = n4d.client.Client(self.proxy, self.user, self.pswd)
			#programmed=self.client.get_variable(key,"VariablesManager",self.REMOTE_VAR)
			#New N4D funcion
			ret=self.client.validate_user()
			programmed=self.client.get_variable(self.REMOTE_VAR)
			if programmed is None:
				self.client.test_var(key,"LliureXRemoteInstaller",self.REMOTE_VAR)
				programmed=self.client.get_variable(key,"VariablesManager",self.REMOTE_VAR)
			return [True,programmed]
		except Exception as e:
			self._debug ("(read_n4dkey): %s" %(str(e)))
			return [False,"ERROR: %s" %(str(e))]
	# def_read_n4dkey


	def programed_actions(self):
		try:
			u=self.read_n4dkey()
			if u[0]:
				#programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
				programmed=u[1]
			else:
				print(u[1])
				exit()
			self._debug(programmed)
			if len(programmed['deb']['packages'])>0:
				self.programmed_deb=programmed['deb']['packages']
			if len(programmed['sh']['packages'])>0:
				self.programmed_sh=[]
				for item in programmed['sh']['packages']:
					self.programmed_sh.append(item[0])
			if programmed['update']['activate']=='False':
				self.programmed_update=programmed['update']['activate']
			else:
				self.programmed_update=str(programmed['update']['version'])+' from '+str(programmed['update']['url'])
			if len(programmed['apt'])>0:
				resume=True
				for item in programmed['apt']:
					#self.programmed_apt=programmed['apt']['packages']
					if len(programmed['apt'][item]['packages'])>0:
						resume=('\n     -%s: %s')%(item,programmed['apt'][item]['packages'])
						if resume==True:
							pass
						else:
							if self.programmed_apt==None:
								self.programmed_apt=resume
							else:
								self.programmed_apt=self.programmed_apt+resume

			if len(programmed['epi']['packages'])>0:
				resume=True
				for item in programmed['epi']['packages']:
					#self.programmed_apt=programmed['apt']['packages']
					if len(programmed['epi']['packages'][item]['custom_name'])>0:
						resume=programmed['epi']['packages'][item]['custom_name']
						if resume==True:
							pass
						else:
							if self.programmed_zero==None:
								self.programmed_zero=[]
							self.programmed_zero.append(resume)

			solved_format=('LliureX Remote Programmed Actions\n'+'----------------------------------\n'+'Apt:%s\n'+'Deb:%s\n'+'Sh:%s\n'+'Zero:%s\n'+'Update:%s\n')%(self.programmed_apt,self.programmed_deb,self.programmed_sh,self.programmed_zero,self.programmed_update)
			return solved_format
		except Exception as e:
			self._debug ("(_programmed_actions): %s" %(str(e)))
			return [False,"(programed_actions): %s" %(str(e))]
	#def _programed_actions



	def list_repos(self):
		try:
			apt_repos=None
			u=self.read_n4dkey()
			if u[0]:
				#programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
				programmed=u[1]
			else:
				print(u[1])
				exit()
			if len(programmed['apt'])>0:
				apt_repos=''
				for item in programmed['apt']:
					resume=('\n     - %s: %s')%(item,programmed['apt'][item]['url'])
					if apt_repos==None:
						pass
					else:
						apt_repos=apt_repos+resume
			return apt_repos
		except Exception as e:
			self._debug ("(list_repos): %s" %(str(e)))
			return [False,"(list_update): %s" %(str(e))]
	# list_repos

	def list_apt(self):
		try:
			apt_repos=None
			u=self.read_n4dkey()
			if u[0]:
				#programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
				programmed=u[1]
			else:
				print(u[1])
				exit()
			if len(programmed['apt'])>0:
				apt_repos=''
				for item in programmed['apt']:
					resume=('\n     - %s: %s')%(item,programmed['apt'][item]['url'])
					packages=('\n         Pkgs: %s')%programmed['apt'][item]['packages']
					if apt_repos==None:
						pass
					else:
						apt_repos=apt_repos+resume
						apt_repos=apt_repos+packages
			return apt_repos
		except Exception as e:
			self._debug ("(list_repos): %s" %(str(e)))
			return [False,"(list_repos): %s" %(str(e))]
	# list_apt


	def add_repo(self,name,url):
		try:
			u=self.read_n4dkey()
			if u[0]:
				#programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
				programmed=u[1]
			else:
				print(u[1])
				exit()
			if len(programmed['apt'])>0:
				apt_repos=''
				for item in programmed['apt']:
					if item == name:
						return [False, "The NAME for this repositorie is in use."]
					else:
						if programmed['apt'][item]['url'] == url:
							return [False, "This URL repositorie is in use."]

			programmed['apt'][name]={}
			programmed['apt'][name]['url']=url
			programmed['apt'][name]['packages']=[]
			#set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
			#New N4D function
			set_programmed=self.client.LliureXRemoteInstaller.set_var_remote(self.REMOTE_VAR,programmed)
			if set_programmed[0]:
				return[True,'New repositorie %s is added to LliureX Remote Installer'%(name)]
			else:
				return[False, "Your repositorie can't be added becasuse you have an error adding new value to REMOTE_VAR"]
		except Exception as e:
			self._debug ("(add_repo): %s" %(str(e)))
			return [False,"(add_repo): %s" %(str(e))]
	# add_repo



	def del_repo(self,name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			if len(programmed['apt'])>0:
				apt_repos=''
				for item in programmed['apt']:
					programmed['apt'][item]['url']
					if item==name or programmed['apt'][item]['url']==name:
						# Delete this element before if the user consent it.
						try:
							packages_programmed=len(programmed['apt'][item]['packages'])
						except Exception as e:
							packages_programmed=0
						if packages_programmed>0:
							if (self.continue_question('Some package in your repositorie: %s\nContinue deleting repositorie and all programmed packages??'%programmed['apt'][item]['packages'])):
								programmed['apt'].pop(item)
								set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
								if set_programmed[0]:
									return[True,'%s repositorie has been deleted from LliureX Remote Installer'%(name)]
								else:
									return[False, "Your repositorie can't be deleted becasuse you have an error adding new value to REMOTE_VAR"]
							else:
								return[True,'Cancelled by the user.']
						else:
							programmed['apt'].pop(item)
							set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
							if set_programmed[0]:
								return[True,'Repo is empty, deleted without confirmation.']
							else:
								return[False, 'Error adding new value to REMOTE_VAR']
				
			return[False,'Repo not exists.']
		except Exception as e:
			self._debug ("(del_repo): %s"%str(e))
			return [False,"(del_repo): %s" %(str(e))]
	# del_repo



	def continue_question(self,question, default="yes"):
		try:
			valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
			if default is None:
				prompt = " [y/n] "
			elif default == "yes":
				prompt = " [Y/n] "
			elif default == "no":
				prompt = " [y/N] "
			else:
				raise ValueError("invalid default answer: '%s'" % default)

			while True:
				sys.stdout.write(question + prompt)
				choice = input().lower()
				if default is not None and choice == "":
					return valid[default]
				elif choice in valid:
					return valid[choice]
				else:
					sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
		except Exception as e:
			self._debug ("(continue_question): %s"%str(e))
			return [False,"(continue_question): %s" %(str(e))]
		# continue_question


	def add_apt(self,ppa,name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			if len(programmed['apt'])>0:
				apt_repos=''
				apt_programmed=False
				for item in programmed['apt']:
					if item==ppa or programmed['apt'][item]['url']==ppa:
						apt_programmed=True
						# Delete this element before if the user consent it.
						try:
							len_packages_programmed=len(programmed['apt'][item]['packages'])
							packages_programmed=programmed['apt'][item]['packages']
						except Exception as e:
							packages_programmed=[]
						if name in packages_programmed:
							return[False,'Package was already programmed before.\n%s : %s'%(item,packages_programmed)]
						else:
							programmed['apt'][item]['packages'].append(name)
							print('Testing new app in your repositories.... please wait')
							solved=self.client.test_apt_list(u,"LliureXRemoteInstaller",programmed)
							#solved=[True,dict,list_apt,list_apt_deleted,COMMENT]
							if solved[0]:
								if name in solved[3]:
									return[False, 'Error adding new value to REMOTE_VAR because your app is unavailable in this repositorie.\nPlease review it: %s'%name]
								else:
									set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
									if set_programmed[0]:
										return[True,'Package %s is added to ppa: %s.'%(name,ppa)]
									else:
										return[False, 'Your app can be added because you have an error adding new value to REMOTE_VAR']
							else:
								return[False, 'Error adding new value to REMOTE_VAR because your ppa is unavailable.']
							
				if not apt_programmed:
					return[False,'Your ppa is not available, please review it.']
			else:
				return[False,'No repositories availables at the  moment.']
				
		except Exception as e:
			self._debug ("(add_apt): %s" %(str(e)))
			return [False,"(add_apt): %s" %(str(e))]
	# add_apt




	def del_apt(self,name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			if len(programmed['apt'])>0:
				apt_repos=''
				apt_programmed=False
				for item in programmed['apt']:
					try:
						len_packages_programmed=len(programmed['apt'][item]['packages'])
						packages_programmed=programmed['apt'][item]['packages']
					except Exception as e:
						packages_programmed=[]
					if name in packages_programmed:
						item_deleted=item
						if (self.continue_question('You are deleting %s from %s. Are you sure??'%(name, item_deleted))):
							apt_programmed=True
							programmed['apt'][item]['packages'].remove(name)
						else:
							return[True,'Cancelled by the user.']

				if apt_programmed:
					set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
					if set_programmed[0]:
						return[True,'Package %s is deleted from ppa: %s.'%(name,item_deleted)]
					else:
						return[False, 'Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']
				else:
					return[False, 'Error deleting %s from LLiureX Remote Installer because not exists.'%name]
							
				if not apt_programmed:
					return[False,'Your ppa is not available, please review it.']
			else:
				return[False,'No repositories availables at the  moment.']
				
		except Exception as e:
			self._debug ("(del_apt): %s" %(str(e)))
			return [False,"(del_apt): %s" %(str(e))]
	# del_apt



	def list_update(self):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'update': {'url': 'Lliurex.net', 'activate': 'True', 'version': '19.220118', 'datetime': '21-01-2022 12:36'}
			if len(programmed['update'])>0:
				if programmed['update']['activate']=='True':
					resume=(' Update Programmed - %s: %s')%(programmed['update']['url'],programmed['update']['version'])
				else:
					resume=(' Update is not programmed.')
			return [True,resume]
		except Exception as e:
			self._debug ("(list_update): %s" %(str(e)))
			return [False,"(list_update): %s" %(str(e))]
	# list_update



	def op_update(self):
		try:
			u=self.read_n4dkey()
			mirror_version=self.client.mirror_version(u,"LliureXRemoteInstaller")
			net_mirror_version=self.client.net_mirror_version(u,"LliureXRemoteInstaller")
			if mirror_version[1]=='False':
				resume=(' 1 - Mirror Version: Not exists')
			else:
				resume=(' 1 - Mirror Version: %s')%(mirror_version[1])
			if net_mirror_version[0]:
				resume=resume+('\n 2 - LliureX.net Version: %s'%net_mirror_version[1])
			else:
				resume=resume+('\n 2 - LliureX.net is not available.')
				
			return[True,resume]
		except Exception as e:
			self._debug ("(op_update): %s"%str(e))
			return [False,"(op_update): %s" %(str(e))]
	# op_update



	def set_update(self,source_up):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			#mirror_version=self.client.mirror_version(u,"LliureXRemoteInstaller")
			#net_mirror_version=self.client.net_mirror_version(u,"LliureXRemoteInstaller")
			valid = ['Mirror','mirror','MIRROR','lliurex','lliurex.net','cancel', 'false']
			choice=source_up.lower()
			if choice in valid:
				pass
			else:
				test_fail=True
				while test_fail:
					sys.stdout.write("Please respond with 'mirror' or 'lliurex' or 'cancel: ")
					choice = input().lower()
					if choice in valid:
						test_fail=False
			if choice == 'cancel' or choice == 'false':
				programmed['update']['activate']='False'
			if choice == 'mirror':
				mirror_version=self.client.mirror_version(u,"LliureXRemoteInstaller")
				if mirror_version[1]=='False':
					resume=(' Mirror not exists, please select lliurex or generate mirror in LliureX Server.')
					return[True,resume]
				else:
					programmed['update']['activate']='True'
					programmed['update']['url']='Mirror'
					programmed['update']['version']=mirror_version[1]
					date=datetime.datetime.now()
					date_update=date.strftime("%d-%m-%Y %H:%M")
					programmed['update']['datetime']=date_update
			if choice in ['lliurex','lliurex.net']:
				net_mirror_version=self.client.net_mirror_version(u,"LliureXRemoteInstaller")
				if net_mirror_version[0]:
					programmed['update']['activate']='True'
					programmed['update']['url']='Lliurex.net'
					programmed['update']['version']=net_mirror_version[1]
					date=datetime.datetime.now()
					date_update=date.strftime("%d-%m-%Y %H:%M")
					programmed['update']['datetime']=date_update
				else:
					resume=(' LliureX.net is not available.')
					return[True,resume]
			resume='  Updated Resume'
			resume=resume+('\n------------------')
			if programmed['update']['activate']=='True':
				resume=resume+('\nSource: %s'%programmed['update']['url'])
				resume=resume+('\nVersion: %s'%programmed['update']['version'])
			else:
				resume=resume+('\nUpdate is not programmed.')

			if (self.continue_question('%s\n\nAre you sure with this configuration??'%(resume))):
				set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
				if set_programmed[0]:
					return[True,'Saved new options.']
				else:
					return[False, 'Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']
			else:
				return[True,'Cancelled by the user.']
		except Exception as e:
			self._debug ("(set_update): %s"%str(e))
			return [False,"(set_update): %s" %(str(e))]
	# set_update



	def list_zmd(self):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			if len(programmed['epi']['packages'])>0:
				resume=('  ZMDs Programmed   ')
				resume=resume+('\n----------------------')
				for item in programmed['epi']['packages']:
					resume=resume+('\n - %s'%programmed['epi']['packages'][item]['pkg_name'])
					if len(programmed['epi']['packages'][item]['custom_name'])>0:
						resume=resume+(' : %s'%programmed['epi']['packages'][item]['custom_name'])
			else:
				resume=('No zero programs are accesible.')
			return[True,resume]
		except Exception as e:
			self._debug ("(list_zmd): %s" %(str(e)))
			return [False,"(list_zmd): %s" %(str(e))]
	# list_zmd



	def del_zmd(self,del_name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			if len(programmed['epi']['packages'])>0:
				for item in programmed['epi']['packages']:
					if str(programmed['epi']['packages'][item]['pkg_name'])==str(del_name) or str(programmed['epi']['packages'][item]['custom_name'])==str(del_name):
						if (self.continue_question('You are deleting this ZMD:%s .Are you sure??'%(del_name))):
							programmed['epi']['packages'].pop(item)
							set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
							if set_programmed[0]:
								return[True,'Saved new options.']
							else:
								return[False, 'Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']
						else:
							return[True,'Cancelled by the user.']
			resume=('%s not exists in your LliureX Remote variable recorded.'%del_name)
			return[True,resume]
		except Exception as e:
			self._debug ("(del_zmd): %s" %(str(e)))
			return [False,"(del_zmd): %s" %(str(e))]
	# del_zmd



	def op_zmd(self):
		try:
			#'epi': {'packages': {'fonts.epi_fonts-ecolier-court': {'epi_deb_name': 'zero-lliurex-fonts', 'pkg_name': 'fonts-ecolier-court', 'epi_name': 'fonts.epi', 'custom_name': 'fonts-ecolier-court', 'check': True}}}
			u=self.read_n4dkey()
			print('Testing ZMDs availables in server, please wait...')
			self.list_available=self.client.list_available_epis(u,"LliureXRemoteInstaller")
			list_zmd_programmed=self.list_zmd()
			if list_zmd_programmed[0]:
				if list_zmd_programmed[1]=='None':
					list_zmd_programmed=[]
				else:
					list_zmd_programmed=list_zmd_programmed[1]
			else:
				return[True,"Can't check ZMDs programmed at the server"]
			if self.list_available[0]:
				list_zmd=('\n   Available ZMD    ')
				list_zmd=list_zmd+('\n--------------------')
				for element in self.list_available[1]:
					for key in element:
						#Dentro del EPI hay listas, si las hay debo ver todos sus elementos.
						if element[key]['selection_enabled']['active']:
							for pkg in element[key]['pkg_list']:
								pkg_added=pkg['name']
								if len(pkg['custom_name'])>0:
									pkg_added=pkg_added+' : '+pkg['custom_name']							
						else:
							pkg=element[key]['pkg_list'][0]
							pkg_added=pkg['name']
							if len(pkg['custom_name'])>0:
								pkg_added=pkg_added+' : '+pkg['custom_name']

						list_zmd=list_zmd+('\n - %s'%pkg_added)	
				resume=list_zmd
			else:
				resume=('ZMDs list is not available, please review the server.')
			return[True,resume]
		except Exception as e:
			self._debug ("(op_zmd): %s" %(str(e)))
			return [False,"(op_zmd): %s" %(str(e))]
	# op_zmd



	def add_zmd(self,epi_del):
		try:
			#'epi': {'packages': {'fonts.epi_fonts-ecolier-court': {'epi_deb_name': 'zero-lliurex-fonts', 'pkg_name': 'fonts-ecolier-court', 'epi_name': 'fonts.epi', 'custom_name': 'fonts-ecolier-court', 'check': True}}}
			u=self.read_n4dkey()
			print('Testing ZMDs availables in server, please wait...')
			
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			for item in programmed['epi']['packages']:
				if str(programmed['epi']['packages'][item]['pkg_name'])==str(epi_del) or str(programmed['epi']['packages'][item]['custom_name'])==str(epi_del):
					return[True, 'Impossible to programmed. You has programmed this app before, review it.']
			self.list_available=self.client.list_available_epis(u,"LliureXRemoteInstaller")
			list_zmd_programmed=self.list_zmd()
			if list_zmd_programmed[0]:
				if list_zmd_programmed[1]=='None':
					list_zmd_programmed=[]
				else:
					list_zmd_programmed=list_zmd_programmed[1]
			else:
				return[True,"Can't check ZMDs programmed at the server"]
			if self.list_available[0]:
				for element in self.list_available[1]:
					for key in element:
						#Dentro del EPI hay listas, si las hay debo ver todos sus elementos.
						if element[key]['selection_enabled']['active']:
							for pkg in element[key]['pkg_list']:
								if str(pkg['name']) == str(epi_del) or str(pkg['custom_name']) == str(epi_del):
									clave_name=str(key)+'_'+pkg['name']
									epi_name=key
									pkg_name=pkg['name']
									custom_name=pkg['custom_name']
									epi_deb_name=''
									check=True
									break
						else:
							pkg=element[key]['pkg_list'][0]
							if str(pkg['name']) == str(epi_del) or str(pkg['custom_name']) == str(epi_del):
								clave_name=str(key)+'_'+pkg['name']
								epi_name=key
								pkg_name=pkg['name']
								custom_name=pkg['custom_name']
								epi_deb_name=''
								check=True
								break

				if check:
					programmed['epi']['packages'][clave_name]={}
					programmed['epi']['packages'][clave_name]['epi_name']=epi_name
					programmed['epi']['packages'][clave_name]['pkg_name']=pkg_name
					programmed['epi']['packages'][clave_name]['custom_name']=custom_name
					programmed['epi']['packages'][clave_name]['check']=check
					print('Testing if package is available, please wait...')
					epi_deb=self.client.epi_deb(u,"LliureXRemoteInstaller",epi_name)
					if epi_deb[0]:
						epi_deb_name=epi_deb[1]
						programmed['epi']['packages'][clave_name]['epi_deb_name']=epi_deb_name
						set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
						if set_programmed[0]:
							self._debug(programmed)
							return[True,'ZMD %s is programmed to install in all clients.'%(epi_del)]
						else:
							self._debug(programmed)
							return[True, 'Impossible to programmed. Your server has an error adding new value to REMOTE_VAR']
					else:
						resume=("Can't solve Epi_Deb_Name, sorry your server has a problem.")
			else:
				resume=('ZMDs list is not available, please review the server.')
			return[True,resume]
		except Exception as e:
			self._debug ("(add_zmd): %s" %(str(e)))
			return [False,"(add_zmd): %s" %(str(e))]
	# add_zmd



	def list_deb(self):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			if len(programmed['deb']['packages'])>0:
				resume=('  DEBs Programmed   ')
				resume=resume+('\n----------------------')
				for item in programmed['deb']['packages']:
					resume=resume+('\n - %s'%item)
			else:
				resume=(' Debs packages are not programmed.')
			return [True,resume]
		except Exception as e:
			self._debug ("(list_deb): %s" %(str(e)))
			return [False,"(list_deb): %s" %(str(e))]
	# list_deb



	def del_deb(self,del_name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			if del_name in programmed['deb']['packages']:
				if (self.continue_question('You are deleting this DEB:%s .Are you sure??'%(del_name))):
					#Si queremos borrar la programacion del DEB tenemos que comprobar que existe en el servidor, borrar ese fichero y por último eliminar la programacion.
					exist_in_server=self.client.app_deb_exist(u,"LliureXRemoteInstaller",del_name,programmed['deb']['url'])
					if exist_in_server[0]:
						url_dest="/var/www/llx-remote/"+str(del_name)
						deb_deleted=self.client.remove_file(u,"LliureXRemoteInstaller",url_dest)
						if deb_deleted[0]:
							pass
						else:
							return[False, 'ERROR: The connection to server to delete the package name has failed.']

					programmed['deb']['packages'].remove(del_name)
					set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
					if set_programmed[0]:
						return[True,'Saved new options.']
					else:
						return[False, 'ERROR: Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']
				else:
					return[True,'Cancelled by the user.']
			else:
				resume=(' Review the name of deb, because this deb is not in LliureX Remote.')
			return [True,resume]
		except Exception as e:
			self._debug ("(del_deb): %s" %(str(e)))
			return [False,"(del_deb): %s" %(str(e))]
	# del_deb



	def add_deb(self,deb_name):
		try:
			pkg=os.path.basename(deb_name)
			deb_name=os.path.abspath(deb_name)
			pkg=(str(pkg))
			pkg_extension = os.path.splitext(pkg)[1]
			self._debug(pkg_extension)
			if pkg_extension.lower() not in ['.deb']:
				return[True,"Sorry but your DEB doesn't look like a package, review it."]

			if os.path.exists(deb_name):
				pass
			else:
				return[True,'Sorry but your path file not exist in your computer, review it.']
				
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			#Existe en el server??
			exist_in_server=self.client.app_deb_exist(u,"LliureXRemoteInstaller",pkg,programmed['deb']['url'])
			if exist_in_server[0]:
				pass
			else:
				print('NOT exists in server, adding it wait please...')
				url_dest=programmed["deb"]["url"].split('http://server/')[1]
				url_dest="/var/www/"+str(url_dest)
				ip_dest="server"
				file_sent=self.client.send_file(u,"ScpManager",u[0],u[1],ip_dest,deb_name,url_dest)
				if file_sent['status']:
					pass
				else:
					return[True,'Failed to send file to server...connection failed.']

			#Esta programado de antes??
			if pkg in programmed['deb']['packages']:
				return[True,'Your DEB had been added before to LliureX Remote, do nothing.']
			else:
				programmed['deb']['packages'].append(pkg)
				set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
				if set_programmed[0]:
					return[True,'Your DEB is added to LliureX Remote.']
				else:
					return[False, 'ERROR: Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']

			
		except Exception as e:
			self._debug ("(add_deb): %s" %(str(e)))
			return [False,"(add_deb): %s" %(str(e))]
	# add_deb



	def list_sh(self):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			if len(programmed['sh']['packages'])>0:
				resume=('  SH Programmed   ')
				resume=resume+('\n----------------------')
				for item in programmed['sh']['packages']:
					resume=resume+('\n - %s'%item[0])
			else:
				resume=(' SH packages are not programmed.')
			return [True,resume]
		except Exception as e:
			self._debug ("(list_sh): %s" %(str(e)))
			return [False,"(list_sh): %s" %(str(e))]
	# list_sh




	def del_sh(self,del_name):
		try:
			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			for item in programmed['sh']['packages']:
				if del_name in item[0]:
					if (self.continue_question('You are deleting this SH:%s .Are you sure??'%(del_name))):
						#Si queremos borrar la programacion del DEB tenemos que comprobar que existe en el servidor, borrar ese fichero y por último eliminar la programacion.
						exist_in_server=self.client.app_deb_exist(u,"LliureXRemoteInstaller",del_name,programmed['sh']['url'])
						if exist_in_server[0]:
							url_dest="/var/www/llx-remote/"+str(del_name)
							deb_deleted=self.client.remove_file(u,"LliureXRemoteInstaller",url_dest)
							if deb_deleted[0]:
								pass
							else:
								return[False, 'ERROR: The connection to server to delete the package name has failed.']

						programmed['sh']['packages'].remove(item)
						set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
						if set_programmed[0]:
							return[True,'Saved new options.']
						else:
							return[False, 'ERROR: Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']
					else:
						return[True,'Cancelled by the user.']
				else:
					resume=(' Review the name of SH, because is not in LliureX Remote.')
			return [True,resume]
		except Exception as e:
			self._debug ("(del_sh): %s" %(str(e)))
			return [False,"(del_sh): %s" %(str(e))]
	# del_sh



	
	def add_sh(self,deb_name):
		try:
			pkg=os.path.basename(deb_name)
			deb_name=os.path.abspath(deb_name)
			pkg=(str(pkg))
			if os.path.exists(deb_name):
				pass
			else:
				return[True,'Sorry but your path file not exist in your computer, review it.']

			u=self.read_n4dkey()
			programmed=self.client.get_variable(u,"VariablesManager",self.REMOTE_VAR)
			# 'deb': {'url': 'http://server/llx-remote/', 'packages': ['openprinting-ppds-postscript-ricoh_20161206-1lsb3.2_all.deb']}
			#Existe en el server??
			exist_in_server=self.client.app_deb_exist(u,"LliureXRemoteInstaller",pkg,programmed['sh']['url'])
			if exist_in_server[0]:
				pass
			else:
				print('NOT exists in server, adding it wait please...')
				url_dest=programmed["sh"]["url"].split('http://server/')[1]
				url_dest="/var/www/"+str(url_dest)
				ip_dest="server"
				file_sent=self.client.send_file(u,"ScpManager",u[0],u[1],ip_dest,deb_name,url_dest)
				if file_sent['status']:
					pass
				else:
					return[True,'Failed to send file to server...connection failed.']

			#Esta programado de antes??
			if pkg in programmed['sh']['packages']:
				return[True,'Your SH had been added before to LliureX Remote, do nothing.']
			else:
				lines=subprocess.Popen(["LAGUAGE=en_EN; md5sum %s | awk '{print $1}'"%deb_name],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
				for line in lines.splitlines():
					md5=line
				pkg_tupla=[pkg,md5]
				programmed['sh']['packages'].append(pkg_tupla)
				set_programmed=self.client.set_var_remote(u,"LliureXRemoteInstaller",self.REMOTE_VAR,programmed)
				if set_programmed[0]:
					return[True,'Your SH is added to LliureX Remote.']
				else:
					return[False, 'ERROR: Your app can be deleted becasuse you have an error adding new value to REMOTE_VAR']

			
		except Exception as e:
			self._debug ("(add_sh): %s" %(str(e)))
			return [False,"(add_sh): %s" %(str(e))]
	# add_deb