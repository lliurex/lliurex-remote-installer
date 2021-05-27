import subprocess
import os
import os.path
import logging
import shutil
import re
import datetime
import json
#from urllib.request import urlopen
import urllib.request as ur
import requests

import n4d.server.core as n4dcore
import n4d.responses



class LliureXRemoteInstaller:
	
	N4D_VAR="LLX_REMOTE_INSTALLER"
	initial_dict={'deb': {'url': 'http://server/llx-remote/', 'packages': []}, 'epi': {'packages': {}}, 'sh': {'url': 'http://server/llx-remote/', 'packages': []}, 'apt': {'Mirror':{'url':'mirror', 'packages': []},'LliureX':{'url':'lliurex', 'packages': []}},'update':{'activate':'False', 'url':'Mirror', 'version':'0','datetime':'0'}}
	
	MIRROR_VERSION_ERROR=-20


	logging.basicConfig(format = '%(asctime)s %(message)s',datefmt = '%m/%d/%Y %I:%M:%S %p',filename = '/var/log/lliurex-remote-installer.log',level=logging.DEBUG)

	#VALOR VARIABLE DEL REPO ADDAPLICATION_SOURCES
	dir_sources="/etc/apt/sources.list.d/"
	file_sources="llxremoteinstaller_sources.list"
	file_sources=str(dir_sources)+str(file_sources)
	
	
	#VALORES DE LOS DICCIONARIOS
	DEB='deb'
	APT='apt'
	SH='sh'
	LIST='packages'
	URL='url'
	UPDATE='update'
	SHARE_DIRECTORY='/var/www/llx-remote'
	MIRROR_DIRECTORY='/net/mirror/llx21'
	NET_MIRROR_DIRECTORY='http://lliurex.net/focal'
	TIMESTAMP_DIRECTORY='/pool/main/l/lliurex-version-timestamp/'
	LOG_FILE='/var/log/lliurex-remote-installer.log'
	
	
	def __init__(self):

		self.core=n4dcore.Core.get_core()

		self.dbg=0
		if self.dbg==1:
			print ("-----------------------------------------------------" )
			print ("-----------------------------------------------------" )
			print ("")
			print ("[LLXRemoteInstaller] DEBUG_MODE ACTIVATED" )
			print ("")
			print ("-----------------------------------------------------" )
			print ("-----------------------------------------------------" )
		pass
		
	#def __init__
	


	def _log(self, message):
		try:
			logging.debug(message)
			return n4d.responses.build_successful_call_response(0)
		except Exception as e:
			print ("[LLXRemoteInstaller] (_log) %s" %(str(e)))
			return n4d.responses.build_successful_call_response([False,str(e),0])
	
	#def__log
	


	def _debug(self,message):
		try:
			self._log(message)
			if self.dbg==1:
				print(str(message))
				self._log(message)
			
		except Exception as e:
			print ("[LLXRemoteInstaller] (_debug) %s" %(str(e)))
			
	#def__debug
	
	
	def read_n4dkey(self):

		try:
			f=open("/etc/n4d/key")
			key=f.readline().strip("\n")
			f.close()
		
			#return key
			return n4d.responses.build_successful_call_response(key)
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (read_n4dkey) %s" %(str(e)))
			#return None
			return n4d.responses.build_successful_call_response(None)
		
	# def_read_n4dkey
	
	
	
	def set_var_remote(self,namevar=None,data=None,user=None,passwd=None ):
		try:
			#import xmlrpclib as x
			#c=x.ServerProxy("https://server:9779")
			#u=(user,passwd)
			#u=self.read_n4dkey()
			#VALOR=c.set_variable(u,"VariablesManager",namevar,data)
			namevar_reset=self.core.set_variable(namevar,data)
			if namevar_reset['status']==0:
				VALOR=namevar_reset['return']
			else:
				VALOR=[False]

			if VALOR[0]:
				COMMENT=("[LLXRemoteInstaller] (set_var_remote) %s = %s" %(namevar,data))
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			else:
				COMMENT=("[LLXRemoteInstaller] (set_var_remote) %s" %(VALOR[1]))
				#return [False,str(COMMENT)]
				return n4d.responses.build_successful_call_response([False,str(COMMENT)])
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (set_var_remote) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			
	# def_set_var_remote
	
	
	def test_var (self,namevar=None):
		try:
			# Method to test LLIUREXREMOTEINSTALLER var if exists in system
			self._debug ("------------------------------------")
			self._debug ("Lliurex Remote Installer Test Var")
			self._debug ("------------------------------------")

			ppa_lliurex=False
			ppa_mirror=False

			VALOR=self.core.get_variable(namevar)['return']
			self._debug ("[LLXRemoteInstaller] (test_var) Value for variable %s: %s"%(namevar,VALOR))
			if not os.path.exists(self.SHARE_DIRECTORY):
				os.makedirs(self.SHARE_DIRECTORY)
				#proc=subprocess.Popen(["LANGUAGE=en_EN; chown 775 %s; sudo setfacl -m g:adm:rwx -d -m g:adm:rwx %s" %self.SHARE_DIRECTORY],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
				#proc.wait()
				os.system("chmod 775 %s"%self.SHARE_DIRECTORY)
				os.system("setfacl -m g:adm:rwx -d -m g:adm:rwx %s"%self.SHARE_DIRECTORY)
				os.system("setfacl -m g:admins:rwx -d -m g:admins:rwx %s"%self.SHARE_DIRECTORY)
				self._debug("[LLXRemoteInstaller] (test_var) New directory to shared files is created: %s"%(self.SHARE_DIRECTORY))
			else:
				self._debug ("[LLXRemoteInstaller] (test_var) Directory to shared files exists: %s"%(self.SHARE_DIRECTORY))
				os.system("setfacl -m g:adm:rwx -d -m g:adm:rwx %s"%self.SHARE_DIRECTORY)
				os.system("setfacl -m g:admins:rwx -d -m g:admins:rwx %s"%self.SHARE_DIRECTORY)
				#os.chmod(self.SHARE_DIRECTORY, 755)
			#print "[LLXRemoteInstaller] (test_var) Value for variable %s: %s"%(namevar,VALOR)
			if  VALOR in ["",None,'None','']:
				#objects["VariablesManager"].add_variable(namevar,self.initial_dict,"",namevar,[],False,False)
				#c.add_variable(u,"VariablesManager",namevar,self.initial_dict,"",namevar,[],False,False)
				self.core.set_variable(namevar,self.initial_dict)
				COMMENT = ("[LLXRemoteInstaller] (test_var) Added variable %s to VariablesManager" %namevar)
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])


			else:
				for x in VALOR[self.APT]:
					if x in ["LliureX"]:
						ppa_lliurex=True
					elif x in ["Mirror"]:
						ppa_mirror=True
				if not ppa_lliurex:
					self._debug ("No tiene lliurex.net")
					VALOR[self.APT].update({'LliureX':{'url':'lliurex', 'packages': []}})
					#objects["VariablesManager"].set_variable(namevar,VALOR)
					#c.set_variable(u,"VariablesManager",namevar,VALOR)
					self.core.set_variable(namevar,self.initial_dict)
				if not ppa_mirror:
					self._debug ("No tiene mirror")
					VALOR[self.APT].update({'Mirror':{'url':'mirror', 'packages': []}})
					#objects["VariablesManager"].set_variable(namevar,VALOR)
					#c.set_variable(u,"VariablesManager",namevar,VALOR)
					self.core.set_variable(namevar,self.initial_dict)
				try:
					exists=VALOR[self.UPDATE]
				except Exception as e:
					self._debug ("[LLXRemoteInstaller] (test_var) Creating new values to variable[update].......")
					VALOR[self.UPDATE]={}
					VALOR[self.UPDATE]['activate']='False'
					VALOR[self.UPDATE]['url']='mirror'
					VALOR[self.UPDATE]['version']='0'
					VALOR[self.UPDATE]['datetime']='0'
					#objects["VariablesManager"].set_variable(namevar,VALOR)
					#c.set_variable(u,"VariablesManager",namevar,VALOR)
					self.core.set_variable(namevar,self.initial_dict)
				COMMENT=("[LLXRemoteInstaller] (test_var) %s Variable exists in your system, it hasn't been created again" %namevar)
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (test_var) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
			
	#def_test_var
	
	
	def reset_var (self,namevar=None):
		try:
			
			#import xmlrpclib as x
			#c=x.ServerProxy("https://server:9779")
			data=None
			#u=self.read_n4dkey()
			#objects["VariablesManager"].set_variable(namevar,data)
			#c.set_variable(u,"VariablesManager",namevar,data)
			namevar_reset=self.core.set_variable(namevar,data)
			if namevar_reset['status']==0:
				COMMENT=("[LLXRemoteInstaller] (reset_var) %s has been reset" %namevar)
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				exito=True
			else:
				COMMENT=("[LLXRemoteInstaller] (reset_var) %s has FAILED to been reset" %namevar)
				self._debug ("%s" %COMMENT)
				exito=False

			return n4d.responses.build_successful_call_response([exito,str(COMMENT)])
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (reset_var) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_reset_var




	def mirror_version(self):
		# Method to discover mirror version if exists.
		try:
			mirror_version_exists=self.core.get_plugin("LliurexVersion").lliurex_version("-m")
			self._debug ("[LLXRemoteInstaller] (mirror_version) mirror_version_exists = %s" %(mirror_version_exists))
			version='False'
			if mirror_version_exists['status']==0:
				if mirror_version_exists['return']=='True':
					DIRECTORY=self.MIRROR_DIRECTORY+self.TIMESTAMP_DIRECTORY
					lst=os.listdir(DIRECTORY)
					lst_ordered=sorted([f for f in lst])
					version=re.search(r'\_(.*)\_', lst_ordered[-1]).group(1)
			return n4d.responses.build_successful_call_response([True,version])

		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (mirror_version) %s" %(str(e)))
			return n4d.responses.build_successful_call_response([False,str(e)])
	
	#def_mirror_version
	



	
	def net_mirror_version(self):
		try:
			
			DIRECTORY=self.NET_MIRROR_DIRECTORY+self.TIMESTAMP_DIRECTORY
			urlpath =ur.urlopen(DIRECTORY)
			net_mirror_info= urlpath.read().decode('utf-8')
			info=re.findall('<a href="?\'?([^"\'>]*)deb', net_mirror_info)
			lst_ordered=sorted([f for f in info])
			version=re.search(r'\_(.*)\_', lst_ordered[-1]).group(1)
					
			#return [True,version]
			return n4d.responses.build_successful_call_response([True,version])

		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (net_mirror_version) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
	#def_mirror_version
	
	
	def write_log(self, dict_var,dict_orig):
		try:
			if os.path.exists(self.LOG_FILE):
				option='a'
			else :
				option='w'
			#self._debug ('[LLXRemoteInstaller] (write_log) Option to write_log is.......%s'%option)
			date=datetime.datetime.now()
			date_update=date.strftime("%d-%m-%Y %H:%M")
			d1_keys = set(dict_var.keys())
			d2_keys = set(dict_orig.keys())
			intersect_keys = d1_keys.intersection(d2_keys)
			added = d1_keys - d2_keys
			removed = d2_keys - d1_keys
			modified = {o : (dict_var[o]) for o in intersect_keys if dict_var[o] != dict_orig[o]}
			#self._debug ('[LLXRemoteInstaller] (write_log) New data to write_log is.......%s'%modified)
			f=open(self.LOG_FILE,option)
			#f.write('### User: %s \n'%(user))
			f.write('### Date: %s \n'%date_update)
			f.write('### Data modified: %s \n'%modified)
			#f.write(json.dumps(new_data))
			f.write('------------------------------------\n')
			f.write('** New variable plublished: ')
			f.write(json.dumps(dict_var))
			f.write('\n')
			f.write('\n')
			f.close
			#return [True]
			return n4d.responses.build_successful_call_response([True])
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (write_log) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_write_log

	def update_var_dict (self,namevar=None,dict_var={},user=None,passwd=None):
		try:
			self._debug ("[LLXRemoteInstaller] (update_var_list) Test if_exists variable %s"%namevar)
			if self.test_var(namevar,user, passwd)[0]:
				self._debug ("[LLXRemoteInstaller] (update_var_list) Variable %s is now in your system"%namevar)
				#import xmlrpclib as x
				#c=x.ServerProxy("https://server:9779")
				#if objects["VariablesManager"].set_variable(namevar,dict_var)[0]:
				#if c.set_variable(u,"VariablesManager",namevar,dict_var)[0]:
				namevar_reset=self.core.set_variable(namevar,dict_var)
				if namevar_reset['status']==0:
					if os.path.exists(self.LOG_FILE):
						option='w'
					else :
						option='a'
					date=datetime.datetime.now()
					date_update=datestrftime("%d-%m-%Y %H:%M")
					f=open(self.LOG_FILE,option)
					f.write('### User: %s has modificated LLX-Remote at: %s'%(user,date_update))
					f.write(dict_var)
					f.close
					COMMENT="[LLXRemoteInstaller] (update_var_list) %s has been updated with this list of APP %s" %(namevar,dict_var)
					self._debug ("%s" %COMMENT)
					#return [True,str(COMMENT)]
					return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			else:
				COMMENT="[LLXRemoteInstaller] (update_var_list) Cannot updated variable"
				self._debug ("%s" %COMMENT)
				#return [False,str(COMMENT)]
				return n4d.responses.build_successful_call_response([False,str(COMMENT)])
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (update_var_list) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_add_list
	
	
	def update2version (self,Mirror=False):
		try:
			update_version="Ninguna"
			if Mirror:
				update_version=subprocess.Popen(["LANGUAGE=en_EN; find /net/mirror/llx16/pool/main/l/lliurex-version-timestamp -name 'lliurex-version-timestamp*.deb' | tail -n 1 | cut -d_ -f2" ],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
			else:
				pass
			
			
			COMMENT="Update_version is: %s" %update_version
			self._debug ("%s" %COMMENT)	
			#return [True,str(COMMENT)]
			return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (update2version) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_update2version
	
	
	
	def app_repo_exist (self,app=None):
		try:
			#exist=os.system("LANGUAGE=en_EN; apt-cache policy %s | grep -i candidate" %app)
			exist=subprocess.Popen(["LANGUAGE=en_EN; apt-cache policy %s | grep -i candidate" %app],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
			exist=exist.decode('utf-8')
			self._debug ("[LLXRemoteInstaller] (app_repo_exist) APP candidate in your repo is: %s"%exist)
			if exist in [None,"None","none",""]:
				COMMENT="[LLXRemoteInstaller] (app_repo_exist) APP: %s doesn't exist in your repository, you can't add it to install list" %app
				self._debug ("%s" %COMMENT)
				#return [False,str(COMMENT)]
				return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			else:
				COMMENT="[LLXRemoteInstaller] (app_repo_exist) APP: %s is avaiable from your repo, it has been added to your install list" %app
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (app_repo_exist) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_app_repo_exist
	
	
	
	def app_deb_exist (self,app=None, url=None):
		try:
			url_all=str(url)+str(app)
			self._debug ("[LLXRemoteInstaller] (app_deb_exist) VAR URL_ALL: %s"%url_all)
			#if ur.urlopen(url_all).code == 200:
			if requests.get(url_all).status_code == 200:
				COMMENT="[LLXRemoteInstaller](app_deb_exist) APP: %s is avaiable and added to list to install it" %app
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			else:
				COMMENT="[LLXRemoteInstaller] (app_deb_exist) Can't find APP: %s to download it from URL %s, you would have uploaded to install it" %(app,url)
				self._debug ("%s" %COMMENT)
				#return [False,str(COMMENT)]
				return n4d.responses.build_successful_call_response([False,str(COMMENT)])
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (app_deb_exist) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_app_deb_exist
	
	
	
	def repo_add (self,sources_private=None):
		try:
			if sources_private not in ["",None,[]]:
				COMMENT="[LLXRemoteInstaller](repo_add) REPO IS PARTICULAR %s" %sources_private
				self._debug ("%s" %COMMENT)
				self._debug ("[LLXRemoteInstaller](repo_add) Creating new file %s" %self.file_sources)
				mode = 'a' if os.path.exists(self.file_sources) else 'w'
				f_used=open(self.file_sources,mode)
				self._debug ("open(%s,%s)"%(self.file_sources,mode))
				f_used.write(sources_private+'\n')
				f_used.close()
				self._debug ("[LLXRemoteInstaller](repo_add) File created now read it" )
				#NOW READ THE NEW SOURCES.LIST
				sources=[]
				file=open(self.file_sources)
				f=file.read().splitlines()
				for line in f:
					sources.append(line)
					self._debug ("[LLXRemoteInstaller](repo_add) Line added: %s" %line)
				file.close()
			
			COMMENT="[LLXRemoteInstaller](repo_add) Your repo LLXRemoteInstaller has new lines %s"%sources	
			self._debug ("%s" %COMMENT)
			#return [True,str(COMMENT),sources]
			return n4d.responses.build_successful_call_response([True,str(COMMENT),sources])
	
				
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (repo_add) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_repo_update
	
	def remove_file (self,file=None):
		try:
			
			COMMENT="[LLXRemoteInstaller](remove_file) Reemoving file %s"%file	
			self._debug ("%s" %COMMENT)
			if os.path.exists(file):
				#print "Borrandoooooooooooooooooooooooooooooo"
				os.remove(file)
			
				COMMENT="[LLXRemoteInstaller](remove_file) File %s has been deleted from server"%file
				self._debug ("%s" %COMMENT)
				#return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			else:
				COMMENT="[LLXRemoteInstaller](remove_file) ERROR: Cannot delete file %s from server"%file
				self._debug ("%s" %COMMENT)
				#return [False,str(COMMENT)]
				return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (remove_file) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_repo_restore
	
	def repo_restore (self,file=None):
		try:
			
			COMMENT="[LLXRemoteInstaller](repo_restore) Repo %s to test APT Aplications is deleted and restore to initial state"%file	
			self._debug ("%s" %COMMENT)
			if os.path.exists(file):
				#print "Borrandoooooooooooooooooooooooooooooo"
				os.remove(file)
				
			self.repo_update()
			
			COMMENT="[LLXRemoteInstaller](repo_restore) Repo from AddApplications has deleted"	
			self._debug ("%s" %COMMENT)
			#return [True,str(COMMENT)]
			return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (repo_restore) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_repo_restore
	
	
	def repo_update (self):
		try:
			COMMENT="[LLXRemoteInstaller](repo_restore) Actualizando los indices, espera........"
			self._debug ("%s" %COMMENT)
			proc = subprocess.Popen('apt-get update', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			proc.wait()
			COMMENT="[LLXRemoteInstaller](repo_restore) Se han actualizado los indices"
			self._debug ("%s" %COMMENT)
			#return [True,str(COMMENT)]
			return n4d.responses.build_successful_call_response([True,str(COMMENT)])
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (repo_update) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_repo_restore
	
	
	def test_apt_list (self,dict_var=None):
		
		try:
			self._debug ("[LLXRemoteInstaller](test_apt_list)")
			list_apt=[]
			list_apt_ok=[]
			list_apt_testing=[]
			restore=False
			ubuntu=["deb http://archive.ubuntu.com/ubuntu focal main restricted universe multiverse","deb http://archive.ubuntu.com/ubuntu focal-security main restricted universe multiverse","deb http://archive.ubuntu.com/ubuntu focal-updates main restricted universe multiverse"]
			lliurex_net=["deb http://lliurex.net/focal focal main restricted universe multiverse","deb http://lliurex.net/focal focal-security main restricted universe multiverse","deb http://lliurex.net/focal focal-updates main restricted universe multiverse"]
			lliurex_mirror=["deb http://mirror/llx21 focal main restricted universe multiverse","deb http://mirror/llx21 focal-security main restricted universe multiverse","deb http://mirror/llx21 focal-updates main restricted universe multiverse"]
			
			self._debug ("[LLXRemoteInstaller](test_apt_list) dict_var[self.APT]: %s"%dict_var[self.APT])
			for x in dict_var[self.APT]:
				self._debug ("[LLXRemoteInstaller](test_apt_list) Comprobando el PPA: %s"%x)
				#print "[LLXRemoteInstaller](dict_ok) Comprobando el listado de APP: %s"%list_apt
				url=dict_var[self.APT][x][self.URL]
				list_apt_testing=dict_var[self.APT][x][self.LIST]
				if url not in ["",None] and list_apt_testing not in ["",[],None]:
					for line in ubuntu:
						self.repo_add(line)
					if x in ["LliureX"]:
						for line in lliurex_net:
							self.repo_add(line)
						COMMENT="[LLXRemoteInstaller](test_apt_list) Repo LliureX esta ADDED"
						self._debug (COMMENT)
						list_apt=list_apt+list_apt_testing
						restore=True
						self._debug ("[LLXRemoteInstaller](test_apt_list) Anyadimos las APT del repo LliureX, nueva lista: %s"%(list_apt))
					elif x in ["Mirror"]:
						for line in lliurex_mirror:
							self.repo_add(line)
						COMMENT="[LLXRemoteInstaller](test_apt_list) Repo Mirror esta ADDED"
						self._debug (COMMENT)
						list_apt=list_apt+list_apt_testing
						restore=True
						self._debug ("[LLXRemoteInstaller](test_apt_list) Anyadimos las APT del repo Mirror, nueva lista: %s"%(list_apt))
					else:
						if self.repo_add(url)['return'][0]:
							COMMENT="[LLXRemoteInstaller](test_apt_list) Repo %s esta ADDED"%url
							self._debug (COMMENT)
							list_apt=list_apt+list_apt_testing
							restore=True
							self._debug ("[LLXRemoteInstaller](test_apt_list) Anyadimos las APT del repo %s, nueva lista: %s"%(url[0],list_apt))
						else:
							self.repo_restore(self.file_sources)
							COMMENT="[LLXRemoteInstaller](test_apt_list) Repo %s no se puede ADDED - PROBLEM"%url
							#return [False,list_apt,COMMENT]
							return n4d.responses.build_successful_call_response([False,list_apt,str(COMMENT)])
			
			if list_apt not in ["",None,[]] :
				if self.repo_update()['return'][0]:
					for app in list_apt:
						self._debug ("[LLXRemoteInstaller](test_apt_list) Comprobando si es avaiable el APT: %s"%app)
						if self.app_repo_exist(app)['return'][0]:
							list_apt_ok.append(app)
					list_apt=list_apt_ok
					COMMENT="[LLXRemoteInstaller](test_apt_list) El listado de APT disponibles en el repo es: %s"%(list_apt)
					self._debug (COMMENT)
				else:
					self.repo_restore(self.file_sources)
					COMMENT="[LLXRemoteInstaller](test_apt_list) No se puede actualizar el repo - PROBLEM"
					#return [False,list_apt,COMMENT]
					return n4d.responses.build_successful_call_response([False,list_apt,str(COMMENT)])
					
				
			else:
				COMMENT="[LLXRemoteInstaller](test_apt_list) No hacemos nada con este REPO esta vacio de contenido"
				self._debug (COMMENT)
				
			#UPDATE DICT
			list_apt_deleted=[]
			for x in dict_var[self.APT]:
				list_apt_testing=[]
				for app in dict_var[self.APT][x][self.LIST]:
					if app in list_apt:
						list_apt_testing.append(app)
					else:
						list_apt_deleted.append(app)
				dict_var[self.APT][x][self.LIST]=list_apt_testing
				
			#Solo hago un update y restore del sources si este ha sido cambiado anteriormente.
			if restore:	
				self.repo_restore(self.file_sources)
			#return [True,dict,list_apt,list_apt_deleted,COMMENT]
			return n4d.responses.build_successful_call_response([True,dict_var,list_apt,list_apt_deleted,str(COMMENT)])
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (test_apt_list) Error: %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
		
	#def test_apt_list
	
	def test_deb_list (self,dict_var=None):
		
		try:
		
			#TEST DE LOS DEBS
			list_debs=dict_var[self.DEB][self.LIST]
			url=dict_var[self.DEB][self.URL]
			#url=self.SHARE_DIRECTORY
			os.system('chmod +r %s/*'%self.SHARE_DIRECTORY)
			self._debug ("[LLXRemoteInstaller](test_deb_list) El listado de DEBS es %s i lo comprobaremos en la URL: %s"%(list_debs,url))
			list_debs_ok=[]
			list_debs_fail=[]
			for app in list_debs:
				self._debug ("[LLXRemoteInstaller](test_deb_list) Comprobando si es avaiable el DEB: %s"%app)
				if self.app_deb_exist(app,url)['return'][0]:
					list_debs_ok.append(app)
				else:
					list_debs_fail.append(app)
			list_debs=list_debs_ok
			dict_var[self.DEB][self.LIST]=list_debs
			self._debug ("[LLXRemoteInstaller](test_deb_list) Listado avaiable de DEBS: %s"%list_debs_ok)
			self._debug ("[LLXRemoteInstaller](test_deb_list) Listado Unavaiable de DEBS: %s"%list_debs_fail)
			#return [True,dict_var,list_debs_ok,list_debs_fail]
			return n4d.responses.build_successful_call_response([True,dict_var,list_debs_ok,list_debs_fail])
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (test_deb_list) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
		
	#def test_deb_list
	
	def test_list (self,dict_var=None,type=None):
		
		try:
		
			#TEST DE LOS DEBS
			list_debs=dict_var[type][self.LIST]
			url=dict_var[type][self.URL]
			#url=self.SHARE_DIRECTORY
			os.system('chmod +r %s/*'%self.SHARE_DIRECTORY)
			self._debug ("[LLXRemoteInstaller](test_list) El listado de SH es %s y lo comprobaremos en la URL: %s"%(list_debs,url))
			list_debs_ok=[]
			list_debs_fail=[]
			list_tupla_ok=[]
			for app_tupla in list_debs:
				app=app_tupla[0]
				md5=app_tupla[1]
				self._debug ("[LLXRemoteInstaller](test_list) Comprobando si es avaiable el SH: %s"%app)
				if self.app_deb_exist(app,url)['return'][0]:
					list_debs_ok.append(app)
					list_tupla_ok.append([app,md5])
				else:
					list_debs_fail.append(app)
			list_debs=list_tupla_ok
			dict_var[type][self.LIST]=list_debs
			self._debug ("[LLXRemoteInstaller](test_list) Listado avaiable de SH: %s"%list_debs_ok)
			self._debug ("[LLXRemoteInstaller](test_list) Listado Unavaiable de SH: %s"%list_debs_fail)
			#return [True,dict_var,list_debs_ok,list_debs_fail]
			return n4d.responses.build_successful_call_response([True,dict_var,list_debs_ok,list_debs_fail])
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (test_list) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
		
	#def test_deb_list
	
	
		#initial_dict_var={'deb': {'url': 'http://server/llx-remote/', 'packages': []}, 'update':{'activate':'False', 'url':'Mirror', 'version':'0'}}

	
	
	
	def dict_ok (self, dict_var={}):
		try:
			if os.path.exists(self.file_sources):
				os.remove(self.file_sources)
			COMMENT="[LLXRemoteInstaller](dict_ok) Comprobando la lista de la GUI........"
			self._debug ("%s" %COMMENT)
			
			#TEST DEL UPDATE
			activate_update=dict_var[self.UPDATE]['activate']
			url_update=dict_var[self.UPDATE][self.URL]
			version_update=dict_var[self.UPDATE]['version']
			datetime_update=dict_var[self.UPDATE]['datetime']
			
			self._debug ("[LLXRemoteInstaller](dict_ok) El update posee activate:%s - url:%s - version:%s - datetime:%s  "%(activate_update,url_update,version_update,datetime_update))
			if activate_update or url_update or  version_update or datetime_update == None:
				dict_var[self.UPDATE]['activate']='False'
				
			self._debug ("[LLXRemoteInstaller](dict_ok) Finalmente UPDATE posee activate:%s - url:%s - version:%s - datetime:%s  "%(activate_update,url_update,version_update,datetime_update))
			
			
			#TEST DE LOS DEBS
			list_debs=dict_var[self.DEB][self.LIST]
			#url=dict_var[self.DEB][self.URL]
			
			self._debug ("[LLXRemoteInstaller](dict_ok) El listado de DEBS es %s i lo comprobaremos en la URL: %s"%(list_debs,url))
			list_debs_ok=[]
			for app in list_debs:
				self._debug ("[LLXRemoteInstaller](dict_ok) Comprobando si es avaiable el DEB: %s"%app)
				if self.app_deb_exist(app,url)[0]:
					list_debs_ok.append(app)
			list_debs=list_debs_ok
			dict_var[self.DEB][self.LIST]=list_debs
			self._debug ("[LLXRemoteInstaller](dict_ok) El listado de DEBS disponibles es: %s"%list_debs)
			
			#TEST DE LOS SH
			list_sh=dict_var[self.SH][self.LIST]
			url=dict_var[self.SH][self.URL]
			self._debug ("[LLXRemoteInstaller](dict_ok) El listado de SCRIPTS es %s i lo comprobaremos en la URL: %s"%(list_debs,url))
			list_sh_ok=[]
			for app_tupla in list_sh:
				app=app_tupla[0]
				md5=app_tupla[1]
				self._debug ("[LLXRemoteInstaller](dict_ok) Comprobando si es avaiable el SCRIPTS: %s"%app)
				if self.app_deb_exist(app,url)[0]:
					list_sh_ok.append([app,md5])
			list_sh=list_sh_ok
			dict_var[self.SH][self.LIST]=list_sh
			self._debug ("[LLXRemoteInstaller](dict_ok) El listado de SCRIPTS disponibles es: %s"%list_sh)
			
			
			list_apt_resume=[]
			#TEST DE LAS APT
			for x in dict_var[self.APT]:
				list_apt=None
				list_apt_ok=[]
				self._debug ("[LLXRemoteInstaller](dict_ok) Comprobando el PPA: %s"%x)
				list_apt=dict_var[self.APT][x][self.LIST]
				#self._debug "[LLXRemoteInstaller](dict_ok) Comprobando el listado de APP: %s"%list_apt
				url=dict_var[self.APT][x][self.URL]
				self._debug ("[LLXRemoteInstaller](dict_ok) El listado de APT es %s lo comprobaremos en la URL: %s"%(list_apt,url))
				
				if list_apt not in ["",None,[]] or url not in ["",None]:
					#print "entro aqui dos"
					if self.repo_add(url)[0]:
						self._debug ("[LLXRemoteInstaller](dict_ok) Repo esta ADDED")
						if self.repo_update()[0]:
							self._debug ("[LLXRemoteInstaller](dict_ok) Repo is UPDATED")
							pass
						else:
							#return [False,"false el repo_update"]
							return n4d.responses.build_successful_call_response(False,"false el repo_update")
							#return [False,self.repo_update()[1]]
					else:
						#return [False,self.repo_add()[1]]
						#return [False,"false el repo_add"]
						return n4d.responses.build_successful_call_response(False,"false el repo_add")
					
					for app in list_apt:
						self._debug ("[LLXRemoteInstaller](dict_ok) Comprobando si es avaiable el APT: %s"%app)
						if self.app_repo_exist(app)[0]:
							list_apt_ok.append(app)
							list_apt_resume.append(app)
					list_apt=list_apt_ok
					dict_var[self.APT][x][self.LIST]=list_apt
					self._debug ("[LLXRemoteInstaller](dict_ok) El listado de APT disponibles en el repo %s es: %s"%(x,list_apt))
				else:
					self._debug ("[LLXRemoteInstaller](dict_ok) No hacemos nada con este REPO %s esta vacio de contenido"%x)
			
			self.repo_restore(self.file_sources)	
			COMMENT="[LLXRemoteInstaller](dict_ok) El listado de disponibles es ** DEBS: %s  ** SH: %s  **  APT: %s"%(list_debs,list_sh,list_apt_resume)
			self._debug ("%s" %COMMENT)
			#return [True,str(COMMENT),dict_var,list_apt_resume]
			return n4d.responses.build_successful_call_response(True,str(COMMENT),dict_var,list_apt_resume)
			
		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (dict_ok) %s" %(str(e)))
			#return [False,str(e)]
			return n4d.responses.build_successful_call_response([False,str(e)])
		
	#def_dict_ok



	# Functions for Epi Installers

	def list_available_epis(self):
		try:
			epi_list=[]
			zmds=[]
			custom_names=[]

			output=subprocess.Popen(['python3 /usr/share/lliurex-remote-installer/helper_epi.py "remote_available_epis"'],shell=True,stdout=subprocess.PIPE).communicate()[0]
			self._debug ("[LLXRemoteInstaller] (list_available_epis) %s" %(str(output)))
			#output=json.loads(output)
			if 'False' in str(output):
				#return [False,epi_list]
				return n4d.responses.build_successful_call_response([False,epi_list])
			epi_list_dict=json.loads(output)
			#epi_list_dict=sorted(epi_list_dict, key=lambda d: list(d.keys()))
			#return [True,epi_list_dict]
			return n4d.responses.build_successful_call_response([True,epi_list_dict])

		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (list_available_epis) %s" %(str(e)))
			#return [False,"[LLXRemoteInstaller] (list_available_epis) %s" %(str(e))]
			return n4d.responses.build_successful_call_response([False,str(e)])

	#list_available_epis


	def epi_deb(self,epi_pkg):
		try:
			output=subprocess.Popen(['python3 /usr/share/lliurex-remote-installer/helper_epi.py "get_epi_deb(\''+epi_pkg+'\')"'],shell=True,stdout=subprocess.PIPE).communicate()[0]
			result=str(output,'utf-8').strip('\n')
			result=result.replace('"','')
			result=result.split()[0]
			#return [True,result]
			return n4d.responses.build_successful_call_response([True,result])

		except Exception as e:
			self._debug ("[LLXRemoteInstaller] (epi_deb) %s" %(str(e)))
			#return [False,"[LLXRemoteInstaller] (epi_deb) %s" %(str(e))]
			return n4d.responses.build_successful_call_response([False,str(e)])
	#epi_deb

	
	
