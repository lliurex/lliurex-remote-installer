import subprocess
import os

import apt
import apt.debfile
import types
import datetime
import threading
import datetime
import shlex

import urllib
import requests

import n4d.server.core as n4dcore
import n4d.responses
import xmlrpc.client as n4dclient
import ssl

class LliureXRemoteInstallerClient:
	
	dir_tmp="/tmp/.LLXRemoteInstallerClient"
	N4D_VAR="LLX_REMOTE_INSTALLER"
	N4D_INSTALLED="LLX_REMOTE_INSTALLER_INSTALLED"
	logFile="/var/log/remoteInstaller.log"
	NATFREE_STARTUP=True
	
	#REPO ADDAPLICATION_SOURCES value
	dir_sources="/etc/apt/sources.list.d/"
	file_sources="llxremoteinstaller_sources.list"
	file_sources=str(dir_sources)+str(file_sources)
	
	#Dict values
	DEB='deb'
	APT='apt'
	SH='sh'
	LIST='packages'
	URL='url'
	UPDATE='update'
	EPI='epi'
	
	#Essential package for provides
	pack_provide="dctrl-tools"
	
	#Installed apps
	LIST_APP_FINAL=[]
	
	def __init__(self):
		
		self.core=n4dcore.Core.get_core()
		
		self.dbg=1
		
		#Delete file_sources if exists
		if os.path.isfile(self.file_sources):
			os.remove(self.file_sources)
		
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

	def _print_info(self,message):
		print("[RemoteInstallerClient] "+str(message))

	def _debug(self,message):
		self._log(message)
		if self.dbg==1:
			print("RemoteInstallerClient: "+str(message))

	def _log(self, message):
		
		if os.path.exists(self.logFile):
			f=open (self.logFile,"a")
		else:
			#os.system(touch /tmp/remoteInstall.log)
			f=open (self.logFile,"w")
		f.write(str(message)+"\n")
		f.close()

	def startup(self,options):
		COMMENT="[LLXRemoteInstallerClient] (startup) Process startup, do nothing don't worry"
		self._debug(COMMENT)
		return True
		# update process moved to lliurex-remote-installer-client.service in systemd

	#def startup
	
	
	def read_n4dkey(self):

		try:
			f=open("/etc/n4d/key")
			key=f.readline().strip("\n")
			f.close()
		
			return key
			
		except Exception as e:
			
			return None
		
	# def_read_n4dke
	
	
	
	def create_dict (self,mode=[]):
		try:
			#Installed apps dict
			dic={}
			for mod in mode:
				dic[mod]=[]
			COMMENT="[LLXRemoteInstallerClient] (create_dict) Dictionary is created %s"%(dic)
			self._debug(COMMENT)
			#return [True,str(COMMENT),dic]
			return n4d.responses.build_successful_call_response([True,str(COMMENT),dic])
		except Exception as e:
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (create_dict) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#def_create_dict
	
	def read_var (self,namevar=None,localhost=None):
		try:
			'''if not localhost:
				proxy="https://server:9779"
			else:
				proxy="https://localhost:9779"
			import xmlrpclib as x
			c=x.ServerProxy(proxy)
			DICT=c.get_variable("","VariablesManager",namevar)'''

			proxy=False
			COMMENT="[LLXRemoteInstallerClient] (read_var)Testing VAR: %s in localhost: %s"%(namevar,localhost)
			self._debug(COMMENT)
			if not localhost:
				self._debug("[LLXRemoteInstallerClient] (read_var) SERVER reading....")
				context=ssl._create_unverified_context()
				client=n4dclient.ServerProxy('https://server:9779',context=context,allow_none=True)
				DICT=client.get_variable(namevar)['return']
			else:
				self._debug("[LLXRemoteInstallerClient] (read_var) LOCALHOST reading....")
				DICT=self.core.get_variable(namevar)['return']
			COMMENT="[LLXRemoteInstallerClient] (read_var) Value of N4D var %s of proxy:%s is %s"%(namevar,proxy,DICT)
			self._debug(COMMENT)
			return_n4d= [True,str(COMMENT),DICT]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (read_var) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#def_read_list
	
	def initialize_n4dvar(self,list_dict):
		self._debug("FNC: initialize_n4dvar")		
		try:
			dic={}
			for x in list_dict:
				dic[x]={}
				if x == self.APT:
					self._debug("Apt mode")
					dic[x]['lliurex']={}
					dic[x]['lliurex'][self.LIST]=[]
					dic[x]['lliurex'][self.URL]=[]
				else:
					dic[x][self.URL]=[]
					dic[x][self.LIST]=[]
			COMMENT=("[LLXRemoteInstallerClient] (initialize_n4dvar) Dict initialized")
			self._debug(COMMENT)
			return_n4d= [True,str(COMMENT),dic]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (initialize_n4dvar) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	
	#def_initialize_var
	
	#def test_var (self,namevar=None,localhost=None,user=None,passwd=None):
	def test_var (self,namevar=None,localhost=None):
		self._debug("test_var")
		try:
#			if localhost in ["",None]:
			'''if not localhost:
				proxy="https://server:9779"
			else:
				proxy="https://localhost:9779"
			self._debug("Proxy: "+pr
			self._debug("Localhost: "+str(localhost))
			self._debug("Namevar: "+str(namevar))
			import xmlrpclib as x
			c=x.ServerProxy(proxy)
			u=self.read_n4dkey()
			VALOR=c.get_variable("","VariablesManager",namevar)'''
			VALOR=self.core.get_variable(namevar)['return']
			self._debug("[LLXRemoteInstallerClient] (test_var) Value of N4d var "+str(namevar)+" is: "+str(VALOR))
#			if  VALOR in [None,'','None']:
			if  not VALOR:
				list_dict=[self.APT,self.DEB,self.SH,self.UPDATE]
				VALOR=self.create_dict ([self.APT,self.DEB,self.EPI,self.SH,self.UPDATE])['return'][2]
				#if objects["VariablesManager"].add_variable(namevar,VALOR,"",namevar,[],False,False)[0]:
				#if c.add_variable(u,"VariablesManager",namevar,VALOR,"",namevar,[],False,False)[0]:

				if self.core.set_variable(namevar,VALOR)['return']:
					COMMENT = ("[LLXRemoteInstallerClient] (test_var) Added variable %s to VariablesManager with valor %s" %(namevar,VALOR))
					self._debug(COMMENT)
					return_n4d= [True,str(COMMENT)]
					return n4d.responses.build_successful_call_response(return_n4d)
				else:
					COMMENT = ("[LLXRemoteInstallerClient] (test_var) Cannot create %s again in VariablesManager" %namevar)
					self._debug(COMMENT)
					return_n4d= [True,str(COMMENT)]
					return n4d.responses.build_successful_call_response(return_n4d)
			else:
				COMMENT=("[LLXRemoteInstallerClient] (test_var) %s Variable exists in your system, it hasn't been created again" %namevar)
				self._debug(COMMENT)
				return_n4d= [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response(return_n4d)
				
		except Exception as e:
			self._debug("ERROR test_var" + str(e))
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (test_var) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#def_test_var
	
	def reset_var (self,namevar=None,localhost=None):
		self._debug("reset_var")
		try:
#			if localhost in ["",None]:
			'''if not localhost:
				proxy="https://server:9779"
			else:
				proxy="https://localhost:9779"
			import xmlrpclib as x
			c=x.ServerProxy(proxy)
			data=None
			u=self.read_n4dkey()
			#objects["VariablesManager"].set_variable(namevar,data)
			c.set_variable(u,"VariablesManager",namevar,data)'''
			self.core.set_variable(namevar,data)
			COMMENT=("[LLXRemoteInstallerClient] (reset_var) %s has been updated" %namevar)
			self._debug(COMMENT)
			return_n4d=[True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
				
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (reset_var) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
		
	#def_reset_var

	def update_var_dict (self,namevar=None,dict_var={},localhost=None):
		self._debug("[LLXRemoteInstallerClient] (update_var dict) start function....")
		try:
			value_test=self.test_var(namevar,localhost)['return']
			if value_test[0]:
				'''if localhost in ["",None]:
					proxy="https://server:9779"
				else:
					proxy="https://localhost:9779"
				import xmlrpclib as x
				c=x.ServerProxy(proxy)
				u=self.read_n4dkey()
				#objects["VariablesManager"].set_variable(namevar,dict)
				c.set_variable(u,"VariablesManager",namevar,dict)'''
				result=self.core.set_variable(namevar,dict_var)
				if result['status']==0:
					result=result['return']
					self._debug("[LLXRemoteInstallerClient] (update_var_dict) core.set_variable: %s"%result)
					COMMENT="[LLXRemoteInstallerClient] (update_var_dict) %s has been updated with this list of APP %s" %(namevar,dict_var)
					self._debug(COMMENT)
					return_n4d=[True,str(COMMENT)]
					testing_operation=self.core.get_variable(namevar,localhost)
					self._debug("[LLXRemoteInstallerClient] (update_var_dict) testing_operation: %s"%testing_operation)
				else:
					COMMENT="[LLXRemoteInstallerClient] (update_var_dict) Has errors: %s"%result
					self._debug(COMMENT)
					return_n4d=[False,str(COMMENT)]

				
				return n4d.responses.build_successful_call_response(return_n4d)
			else:
				COMMENT="[LLXRemoteInstallerClient] (update_var_dict) Can't update variable"
				self._debug(COMMENT)
				return_n4d=[False,str(COMMENT)]
				return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (update_var_dict) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
		
	#def_add_list
	
	def download(self, apps=[],url=None,source_dir=None):
		try:
			#CREATE AUX_SOURCES IF IT'S NECESSARY
			if not os.path.exists(source_dir):
				os.makedirs(source_dir)
			for app in apps:
				file_app=str(source_dir)+"/"+app
				url_complete=str(url)+str(app)
				if os.path.exists(file_app):
					self._debug("(download) The FILE: "+file_app+" has been donwloaded before, it will be deleted now.")
					os.remove(file_app)
				self._debug("(download) The FILE: "+app+" is downloading now to directory "+file_app+" .....")
				ssl._create_default_https_context = ssl._create_unverified_context
				urllib.request.urlretrieve(url_complete,file_app)
				os.chmod(file_app,755)
				
			COMMENT="Your FILES: %s has been downloaded in %s"%(apps,source_dir)
			return_n4d=[True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (download) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	
	#def_download
	
	
	def repo_add (self,sources_private=None):
		try:
			if sources_private not in ["",None,[]]:
				COMMENT="(repo_add) REPO IS PARTICULAR %s" %sources_private
				self._debug(COMMENT)
				mode = 'a'if os.path.exists(self.file_sources) else 'w'
				f_used=open(self.file_sources,mode)
				self._debug("open("+self.file_sources+","+mode+")")
				f_used.write(sources_private+'\n')
				f_used.close()
				self._debug("[LLXRemoteInstaller](repo_add) File created now read it")
				#NOW READ THE NEW SOURCES.LIST
				sources=[]
				sfile=open(self.file_sources)
				f=sfile.read().splitlines()
				for line in f:
					sources.append(line)
				sfile.close()
			
			COMMENT="[LLXRemoteInstallerClient](repo_add) Your repo LLXRemoteInstallerClient has new lines %s"%sources	
			self._debug(COMMENT)

			return_n4d=[True,str(COMMENT),sources]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (repo_add) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
		
	#def_repo_add
	
	def repo_restore (self,f=None):
		self._debug("repo_restore DO NOTHING:::::::::::::::::::::::::")
		try:
			self._debug("repo_restore")
			COMMENT="(repo_restore) Repo %s to test APT Aplications is deleted and restore to initial state"%f
			self._debug(COMMENT)
			if os.path.exists(f):
				os.remove(f)
			self.repo_update()
			#Delete proxy settings
			#if os.path.exists("/etc/apt/apt.conf.d/98proxySettings"):
			#	os.remove("/etc/apt/apt.conf.d/98proxySettings")
			COMMENT="[LLXRemoteInstallerClient](repo_restore) Repo from AddApplications has been deleted"	
			#self._debug(COMMENT)
			return_n4d= [True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
			
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (repo_restore) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			
		
	#def_repo_restore
	
	def repo_update (self):
		self._debug("repo_update")
		try:
			#if os.path.exists(self.file_sources):
			#	COMMENT="[LLXRemoteInstallerClient] (repo_update) Exists %s CORRECTOOOOOOOOO!!!"%(self.file_sources)
			#	os.path.copy(self.file_sources,'/home')
			self._debug("(repo_update) Updating indices, please wait........")
			#proc = subprocess.Popen('apt-get update', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			proc = subprocess.Popen('apt-get update', shell=True, stdin=None, stderr=None, executable="/bin/bash")
			proc.wait()
			#self.cache.update()
			self._debug('(repo_update) Updating indices, process finished****')
			self.cache=apt.Cache()
			#self.cache.update()
			self._debug('(repo_update) Apt.cache updated')
			#self.cache.update()
			COMMENT="[LLXRemoteInstallerClient](repo_update) Your APT CACHE has updated with new indices"
			#self._debug(COMMENT)
			return_n4d=[True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
			
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (repo_update) Error: %e"%(e)
			self._debug(COMMENT)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
		
	#def_repo_update

	def repo_customize_apt(self,repos=[]):
		pinFile="/etc/apt/preferences.d/lliurex-pinning"
		if os.path.exists(pinFile):
			f=open(pinFile,'a')
			f.write("###\n")
			for repo in repos:
				arrayRepoDir=repo.split(' ')
				repoOrig=arrayRepoDir[1]
				pinLine="Package: *\nPin: origin "+repoOrig+"\nPin-Priority:700\n"
				f.write(pinLine)
			f.close()
		#Setup proxy in apt.config.d
		#prefFile=open("/etc/apt/apt.conf.d/98proxySettings","w")
		#prefFile.write('Acquire::http::proxy "http://proxy:3128";')
		#prefFile.close()
	#def repo_customize_apt

	def repo_restore_config(self):
		pinFile="/etc/apt/preferences.d/lliurex-pinning"
		if os.path.exists(pinFile):
			f=open(pinFile,'r')
			lines=f.readlines()
			f.close()
			defaultPin=[]
			continueReading=1
			for line in lines:
				if continueReading:
					if line!="###\n":
						defaultPin.append(line)
					else:
						continueReading=0
				else:
					break
			f=open(pinFile,'w')
			f.writelines(defaultPin)
			f.close()
		if os.path.exists("/etc/apt/apt.conf.d/98proxySettings"):
			os.remove("/etc/apt/apt.conf.d/98proxySettings")
		self._debug("Default config restored")
	#def repo_restore_config
		
	def deb_solvedDependency (self,deb=None,l=[]):
		try:
			for s in l:
				name_deb=s[0]
				version_deb=s[1]
				test_deb=s[2]
				self._debug("(deb_solvedDependency) DEB: "+deb+" depends on package: "+name_deb+" -- version: "+test_deb+" "+version_deb+" -- ")
				#Check if exists in cache. If not abort process
				if name_deb in self.cache:
					#self._debug("[LLXRemoteInstallerClient](deb_solvedDependency) Dependence is avaible")
					pkg=self.cache[name_deb]
					#Check if installed or install dependency
					if pkg.is_installed:
						self._debug("(deb_solvedDependency) Dependency IS INSTALLED in your system DO NOTHING WITH IT")
					else:
						self._debug("(deb_solvedDependency) Dependency "+name_deb+" is being installed ......")
						list_deb_aux=[]
						list_deb_aux.append(name_deb)
						self.apt_install(list_deb_aux)
				else:
					#Check if it's a virtual package from a provides 
					self._debug("(deb_solvedDependency) Testing if dependency "+name_deb+" is a virtual package")
					result=subprocess.Popen(["LAGUAGE=en_EN; grep-status -FProvides,Package -sPackage,Provides,Status %s"%name_deb],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
					virtual_deb=False
					for line in result.splitlines():
						if "install" in line:
							self._debug("(deb_solvedDependency) Dependence: "+name_deb+" is a virtual package installed in my system")
							virtual_deb=True
					#Abort the process only if dependencies doesn't resolv and it's not a virtual package
					if not virtual_deb:
						COMMENT="[LLXRemoteInstallerClient](deb_solvedDependency) Your DEB: %s has unreliable dependencies: %s can not been installed"%(deb,name_deb)
						#self._debug(COMMENT)
						return_n4d=[False,str(COMMENT)]
						return n4d.responses.build_successful_call_response(return_n4d)
			
			COMMENT="[LLXRemoteInstallerClient](deb_solvedDependency) Your DEPENDENCIES has been resolved. Now will continue installing: %s"%(deb)
			#self._debug(COMMENT)
			return_n4d=[True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (deb_solvedDependency) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
		
	#def_debsolvedependence
	
	
	def deb_testDependencies(self,deb=None,dependsList=[]):
		try:
			#Check if dependencies are installed
			self._debug("(deb_testDependencies) Testing your DEB: "+deb+" against this dependencies list "+str(dependsList))
			for x in dependsList:
				self._debug("[LLXRemoteInstallerClient](deb_testDependencies) -------------- Testing this tupla "+str(x)+" ------------------")
				#If dependency has more than one element is an "OR" dependency. Must resolv one of them
				if len(x)<2:
					if self.deb_solvedDependency(deb,x)['return'][0] == 'False':
						name_deb=x[0]
						COMMENT="[LLXRemoteInstallerClient](deb_testDependencies) Your DEB: %s has dependences without solution with your actual repos, APP: %s can not been installed"%(deb,name_deb)
						#self._debug(COMMENT)
						return_n4d=[False,str(COMMENT)]
						return n4d.responses.build_successful_call_response(return_n4d)
				else:
					#"OR" Dependency, one "True" is enough
					OK=False
					self._debug("(deb_testDependencies) Initializing test for *OR* tupla")
					for s in x:
						s=[s]
						name_deb=s[0][0]
						if self.deb_solvedDependency(deb,s)['return'][0]:
							self._debug("(deb_testDependencies) Testing OR tupla: this dependency "+str(name_deb)+" can be installed, as solves the conflict")
							OK=True
							ok_solved=s
					if not OK:
						COMMENT="[LLXRemoteInstallerClient](deb_testDependencies) Testing OR tupla: can not resolve this OR dependency for %s"%(x)
						#self._debug(COMMENT)
						return_n4d=[False,str(COMMENT)]
						return n4d.responses.build_successful_call_response(return_n4d)
					else:
						pass
						self._debug("(deb_testDependencies) Testing OR tupla, can install this dependency: "+str(ok_solved)+" and can resolve OR dependency for "+str(x))
			
			COMMENT="[LLXRemoteInstallerClient](deb_testDependencies) Dependencies are resolved. Now you can install your DEB: %s"%(deb)
			#self._debug(COMMENT)
			return_n4d=[True,str(COMMENT)]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			self._debug("ERROR deb_testDependencies: "+str(e))
			#return [False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (deb_testDependencies) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#deb_testDependencies
	
	def deb_install(self,list_deb=[],dir_deb=None):
		try:
			list_ok=[]
			list_not=[]
			#Load apt cache
			self.cache=apt.Cache()
			self._debug("(deb_install) CACHE updated")
			#Check each deb marked to install
			for deb in list_deb:
				file_deb=str(dir_deb)+"/"+str(deb)
				self._debug("(deb_install) Test first deb to install: "+deb+" in dir: "+file_deb)
				app=apt.debfile.DebPackage(file_deb,self.cache)
				#Check if it's installable
				if app.check():
					self._debug("(deb_install) The deb can be installed, now will proceed to check dependencies, please wait....")
					if self.deb_testDependencies(deb,app.depends)['return'][0]:
						#Install if all is OK
						self._debug("(deb_install) The system are ready to install the DEB: "+deb)
						app.install()
						list_ok.append(deb)
					else:
						#Failed dependencies
						self._debug("(deb_install) The system cannot resolve the dependencies for your deb, review your repos or your DEB if you want to install it: "+deb)
						
				else:
					#There's any reason that makes deb uninstallable
					self._debug("(deb_install) Your DEB: "+deb+" cannot be installed in your system")
					list_not.append(deb)
				
			COMMENT="DEBS installed: %s . DEBS with problems:%s"%(list_ok, list_not)
			return_n4d=[True,str(COMMENT),list_ok,list_not]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			self._debug("(deb_install) ERROR: "+str(e))
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (deb_install) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#deb_install
	
	def sh_install(self,list_sh=[],file_dir=""):
		try:
			list_ok=[]
			list_not=[]
			for app in list_sh:
				self._debug("(sh_install) Working with SCRIPT: "+app)
				file_app=str(file_dir)+"/"+app
				if os.path.exists(file_app):
					self._debug("(sh_install) Executing it, please wait..........")
					proc = subprocess.Popen(file_app, shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
					proc.wait()
					lines=subprocess.Popen(["LAGUAGE=en_EN; md5sum %s | awk '{print $1}'"%file_app],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
					for line in lines.splitlines():
						md5=line.decode('utf-8')
					list_ok.append([app,md5])
				else:
					self._debug("(sh_install) The script "+file_app+" not exists in your system.")
					list_not.append(app)
			
#			if list_ok not in ["",None,[]]:
			if list_ok:
				COMMENT="Your SCRIPTS: %s had been executed"%(list_ok)
				return_n4d=[True,str(COMMENT),list_ok,list_not]
				return n4d.responses.build_successful_call_response(return_n4d)
			else:
				COMMENT="Some scripts failed to execute, please check them %s"%(list_not)
				return_n4d=[True,str(COMMENT),list_ok,list_not]
				return n4d.responses.build_successful_call_response(return_n4d)
			
		except Exception as e:
			r#eturn[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (sh_install) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			
	#sh_install
	
	def apt_install(self,list_apt=[]):
		self._debug("App List: "+str(list_apt))
		try:
			list_apt_ok=[]
			list_apt_not=[]
			list_apt_system=[]
			list_apt_installed_total=[]
			self._debug("[LLXRemoteInstallerClient](apt_install) Apps list: "+str(list_apt))
			for app in list_apt:
				self._debug("[LLXRemoteInstallerClient](apt_install) Checking if app "+app+" is available and installable")
				if app in self.cache:
					pkg=self.cache[app]
					self._debug("[LLXRemoteInstallerClient](apt_install) %s"%pkg.is_installed)
					if pkg.is_installed:
						self._debug("[LLXRemoteInstallerClient](apt_install) The APP: "+app+" is intalled in your system")
						list_apt_system.append(app)
						list_apt_installed_total.append(app)
					else:
						self._debug("[LLXRemoteInstallerClient](apt_install) The APP: "+app+" will be installed soon")
						versiones=self.cache[app].versions
						self._debug("[LLXRemoteInstallerClient](apt_install) Versions:%s"%versiones)
						pkg.mark_install()
						list_apt_ok.append(app)
						list_apt_installed_total.append(app)
#						list_apt_system.append(app)
				else:
					self._debug("[LLXRemoteInstallerClient](apt_install) The APP: "+app+" is not in your repositories")
					list_apt_not.append(app)
						
			if list_apt_ok:
					#				self._debug("(apt_install) Please wait while installing: "+str(list_apt_ok))
				self._debug("[LLXRemoteInstallerClient](apt_install) Please wait while installing: "+str(list_apt_ok))
				self.cache.commit()
				self._debug("[LLXRemoteInstallerClient](apt_install) cache.commit Finished.")
#				if list_apt_not in ["",None,[]]:
				if not list_apt_not:
					COMMENT="[LLXRemoteInstallerClient](apt_install) The system has been updated with this APP list: %s"%(list_apt_system)
				else:
					COMMENT="[LLXRemoteInstallerClient](apt_install) The system has been updated with this APP list: %s but this list cann't be installed:%s"%(list_apt_ok, list_apt_not)
			else:
#				if list_apt_not in ["",None,[]]:
				if not list_apt_not:
					COMMENT="[LLXRemoteInstallerClient](apt_install) Do nothing, because your system has installed all APP in list: %s"%(list_apt)
				else:
					COMMENT="[LLXRemoteInstallerClient](apt_install) Do nothing, because your system has installed all APP in list: %s and this list cannot be installed because your REPO do not have it:%s"%(list_apt_system, list_apt_not)
			
#			if list_apt_system not in ["",None,[]]:
			if list_apt_ok:
				for app in list_apt_ok:
					self._debug("[LLXRemoteInstallerClient](apt_install) The APP: "+app+" is intalled in your system.....Adding to installed list")
#					list_apt_ok.append(app)
			self._debug(COMMENT)
			self._debug("APT installed:"+str(list_apt_ok)+"  ---  APT not installed"+str(list_apt_not)+"  ---  APT in system:"+str(list_apt_system)+"  ---  APT TOTAL in system:"+str(list_apt_installed_total))
			return_n4d=[True,str(COMMENT),list_apt_ok,list_apt_not,list_apt_system,list_apt_installed_total]
			return n4d.responses.build_successful_call_response(return_n4d)
				
		except Exception as e:
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (apt_install) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
			
	#apt_install

	def deb_test(self,appDict,dictOrig):
		self._debug("deb_test")
		#Get dict values
		list_deb=appDict[self.LIST]
		url_deb=appDict[self.URL]

		#Create download path
		dir_deb=str(self.dir_tmp)+"/"+"deb"
		#Check if the deb is installed
		deb_aux=[]
		self._debug("(deb_test) Checking if any deb on the list is already installed "+str(list_deb))
		for deb in list_deb:
			if deb not in dictOrig:
				self._debug("(deb_test)DEB: "+deb+" marked for install")
				deb_aux.append(deb)
			else:
				pass
				self._debug("(deb_test)DEB: "+deb+" is already installed")
		list_deb=deb_aux
		#Download needed debs
#		if list_deb not in ["",None,[]]:
		if list_deb:
			#Create token to indicator
			self._manage_indicator_token("deb","create")
			self._debug("(deb_test) Debs list is "+str(list_deb)+" Download path is: "+url_deb)
			self.download(list_deb,url_deb,dir_deb)
			result_deb=self.deb_install(list_deb,dir_deb)['return']
			#Delete token to indicator
			self._manage_indicator_token("deb","delete")
			
		else:
			self._debug("(deb_test) Deb list is empty")
			result_deb=["","","","",""]
		return_n4d=(result_deb)
		return n4d.responses.build_successful_call_response(return_n4d)
	#def deb_test

	def epi_test(self,appDict,dictOrig):
		try:
			self._debug("epi_test")
			#Get dict values
			list_epi=appDict['packages']

			#Check if the EPI is installed
			epi_aux=[]
			epi_deb_aux=[]
			epi_unavailable=[]
			epi_installed=[]
			result_epi=[]

			self._debug("(epi_test) Checking if all EPI on the list are already installed "+str(list_epi))
			for key in list_epi:
				if key not in dictOrig:
					self._debug("(epi_test)EPI: "+key+" marked for install")
					epi_aux.append(key)
					epi_deb_aux.append(list_epi[key]['epi_deb_name'])
				else:
					self._debug("(epi_test)EPI: "+key+" is already installed")
					pass
			#Install needed debs
			#if list_deb not in ["",None,[]]:
			if epi_aux:
				#Create token to indicator
				self._manage_indicator_token("epi","create")
				self._debug("(epi_test) EPI list to install is: %s "%epi_aux)
				#Compruebo que los EPI no instalados existen en el sistema sino tendre que instalar el DEB que los provee
				self._debug("(test_system) EPI DEBS list to install is: %s "%epi_deb_aux)
				epi_deb_aux_solved=self.apt_install(epi_deb_aux)['return']
				#return [True,str(COMMENT),list_apt_ok,list_apt_not,list_apt_system]

				#Si el resultado ha sido satisfactorio, tendremos una solucion factible
				self._debug("(epi_test) epi_deb_aux_solved: %s "%epi_deb_aux_solved)
				if epi_deb_aux_solved[0]:
					#Cada Epi programado para instalarse, si esta en la lista de debs instalados se istala con EPIC, el resto se marca como no instalados
					for key in list_epi:
						if list_epi[key]['epi_deb_name'] in epi_deb_aux_solved[4]:
							self._debug("(epi_test)EPI: Installing EPI: %s"%key)
							#epic install -u <nombre_epi> <pkg1> <pkg2>
							epi_name=list_epi[key]['epi_name']
							pkg_name=list_epi[key]['pkg_name']
							command="HOME='/root' epic install -u %s %s" %(epi_name,pkg_name)
							self._debug('Command: %s'%(command))

							self._debug(command)
							#p=subprocess.call(command,shell=True)
							# La libreria EPIC necesita conocer el usuario dentro del entorno, se lo pasamos
							my_env=os.environ.copy()
							my_env["USER"]="root"
							p=subprocess.run([command], env=my_env, capture_output=True,shell=True)
							solved_code =p
							self._debug('Epic instruction solved_code: %s '%(solved_code.returncode))
							#self._debug('Epic instruction solved_code: %s - stdout: %s - Error: %s'%(solved_code.returncode,solved_code.stdout,solved_code.stderr))

							if str(solved_code.returncode)=="0" :
								epi_installed.append(key)
							else:
								epi_unavailable.append(key)
							#Descomentar esto cuando lo tengamos todo claro.
							#dictOrig.append(key)
							#epi_install_solved=self.epi_install_epic(key)
						else:
							epi_unavailable.append(key)
				else:
					self._debug("(epi_test)EPI: Sorry but some EPI-deb has been problems and crash funcion")
					

				#Delete token to indicator
				self._manage_indicator_token("epi","delete")
				
			else:
				self._debug("(epi_test) EPI list is empty")
				result_epi=['']

			self._debug("(epi_test) EPI Epi Installed: %s and Epi unavailable: %s"%(epi_installed,epi_unavailable))
			dictOrig=epi_installed
			self._debug('epi_installed_system: %s'%dictOrig)
			return_n4d=(dictOrig)
			return n4d.responses.build_successful_call_response(return_n4d)

		except Exception as e:
			self._debug("(epi_test) EPI error %s"%e)
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (epi_test) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	#def epi_test

	def sh_test(self,appDict,dictOrig):
		self._debug("sh_test")
		#Get dict values
		list_sh=appDict[self.LIST]
		url_sh=appDict[self.URL]
		#Create donwload path and download needed scripts
		dir_sh=str(self.dir_tmp)+"/"+"scripts"
		self._debug("Created tmp dir "+dir_sh)
#		if list_sh not in ["",None,[]]:
		if list_sh:
			#Create token to indicator
			self._manage_indicator_token("sh","create")
			sh_aux=[]
			for sh_tupla in list_sh:
				sh=sh_tupla[0]
				md5=sh_tupla[1]
				if sh_tupla not in dictOrig:
					self._debug("(sh_test) SH: must install "+sh)
					sh_aux.append(sh)
				else:
					self._debug("(sh_test) SH: "+sh+" already installed")
			#Download and execute the scripts
			list_sh=sh_aux	
			self._debug("(sh_test) Script list is "+str(list_sh)+" Download to: "+url_sh)
			self.download(list_sh,url_sh,dir_sh)
			if list_sh not in ["",None,[]]:
				result_sh=self.sh_install(list_sh,dir_sh)['return']
			else:
				self._debug("(sh_test) Script list is empty")
				result_sh=["","","","",""]
			#Create token to indicator
			self._manage_indicator_token("sh","delete")		
			
		else:
			self._debug("(sh_test) Script list is empty")
			result_sh=["","","","",""]
		return_n4d=(result_sh)
		return n4d.responses.build_successful_call_response(return_n4d)
	#def sh_test
	
	
	
	
	def update_test(self,appDict,dictOrig):
		
		self._debug("update_test")
		updated="False"
		#Get dict values
		try:
			updateDict=appDict[self.UPDATE]
		except:
			self._debug("[LLXRemoteInstallerClient](update_test) Update Test: Creating new dictionary")
			version_installed=subprocess.Popen(["lliurex-version -n"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
			version_installed=version_installed.split()[0]
			updateDict={'version':version_installed,'datetime':"None",'url':"Mirror"}
		
		self._debug("[LLXRemoteInstallerClient](update_test) Update Test: Starting......")
			
		version_installed=subprocess.Popen(["lliurex-version -n"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
		version_installed=version_installed.split()[0].decode('utf-8')
		version_installed=str(version_installed)
		version_programed=appDict[self.UPDATE]['version']
		version_programed=version_programed.split()[0]
		version_programed=str(version_programed)
		
		self._debug("[LLXRemoteInstallerClient](update_test) Update Test: Version installed %s"%version_installed)
		self._debug("[LLXRemoteInstallerClient](update_test) Update Test: Version programed %s"%version_programed)
		updated="False"
		
		if ( version_installed < version_programed ):
			updated="True"
			#actualizo repos y updateo
			if appDict[self.UPDATE]['url']=='Lliurex.net':
				self._debug("[LLXRemoteInstallerClient](update_test) Updating your system to Lliurex.net, please wait........")
				#proc = subprocess.Popen(["lliurex-upgrade -u -r"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
				#ret=os.system("http_proxy=http://proxy:3128 /usr/sbin/lliurex-upgrade -u -r 2>/dev/null 1>/dev/null")
				#ret=int(ret)
				#proc = subprocess.Popen('http_proxy=http://proxy:3128 /usr/sbin/lliurex-upgrade -u -r', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
				proc = subprocess.Popen('/usr/sbin/lliurex-upgrade -u -r', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
				proc.wait()
				date=datetime.datetime.now()
				date_update=date.strftime("%d-%m-%Y %H:%M:%S")
				self._debug("[LLXRemoteInstallerClient](update_test) Actualizacion terminada...... %s"%date_update)
				if proc.returncode == 1:
					self._debug("[LLXRemoteInstallerClient](update_test) Fallo actulalizacion")
					updated="False"
			else:
				#proc = subprocess.Popen('http_proxy=http://proxy:3128 /usr/sbin/lliurex-upgrade -u', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
				proc = subprocess.Popen('/usr/sbin/lliurex-upgrade -u', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
				proc.wait()
				date=datetime.datetime.now()
				date_update=date.strftime("%d-%m-%Y %H:%M:%S")
				self._debug("[LLXRemoteInstallerClient](update_test) Actualizacion terminada...... %s"%date_update)
				if proc.returncode == 1:
					self._debug("[LLXRemoteInstallerClient](update_test) Fallo actulalizacion")
					updated="False"
			
			
			update_url=appDict[self.UPDATE]['url']
			new_version=subprocess.Popen(["lliurex-version -n"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
			new_version=new_version.split()[0].decode('utf-8')
			date=datetime.datetime.now()
			date_update=date.strftime("%d-%m-%Y %H:%M")
			updateDict={'version':new_version,'datetime':date_update,'url':update_url}
		
			if updated == 'True':
				self._debug("[LLXRemoteInstallerClient](update_test) Update Test: New dict %s"%updateDict)
			else:
				self._debug("[LLXRemoteInstallerClient](update_test) Updated operation has errors.....")
		else:
			self._debug("[LLXRemoteInstallerClient](update_test) Updated is not necessary, your system has the required version")
		
		return_n4d=[updateDict, updated]
		return n4d.responses.build_successful_call_response(return_n4d)
		
	#def deb_test



	def _refine_apt_repoList(self,appDict,dictOrig):
		self._debug("[LLXRemoteInstallerClient] (_refine_apt_repoList)")
		self._debug("[LLXRemoteInstallerClient] (_refine_apt_repoList)   --- Starting Function ----")
		repoList=[]
		list_apt=[]
		lliurex_net=["deb http://lliurex.net/jammy jammy main restricted universe multiverse","deb http://lliurex.net/jammy jammy-security main restricted universe multiverse","deb http://lliurex.net/jammy jammy-updates main restricted universe multiverse"]
		lliurex_mirror=["deb http://mirror/llx23 jammy main restricted universe multiverse","deb http://mirror/llx23 jammy-security main restricted universe multiverse","deb http://mirror/llx23 jammy-updates main restricted universe multiverse"]
		for source in appDict:
			self._debug("[LLXRemoteInstallerClient](_refine_apt_repoList) Adding applist from: "+str(source))
			aux_list_apt=appDict[source][self.LIST]
			self._debug("[LLXRemoteInstallerClient](_refine_apt_repoList) Adding PPA: "+str(source))
			url=appDict[source][self.URL]
			apt_aux=[]
			self._debug("(_refine_apt_repoList) Checking if apt list is installed "+str(aux_list_apt))
			for apt in aux_list_apt:
				if apt not in dictOrig:
					self._debug("(_refine_apt_repoList) Must install APT: "+apt)
					apt_aux.append(apt)
				else:
					self._debug("(_refine_apt_repoList) "+apt+" is installed")
			#Add non installed debs to list
			list_apt.extend(apt_aux)
			#configure pinning for new repos
			if source in ["LliureX"]:
				pass
				repoList.extend(lliurex_net)
			elif source in ["Mirror"]:
				repoList.extend(lliurex_mirror)
			else:
				repoList.append(url)
		appsRepoDict={'apt':list_apt,'repos':repoList}
		self._debug("[LLXRemoteInstallerClient](_refine_apt_repoList) RESUME to install APT: %s "%appsRepoDict['apt'])
		self._debug("")
		return_n4d=appsRepoDict
		return n4d.responses.build_successful_call_response(return_n4d)
	#def _refine_apt_repoList

	def apt_test(self,appDict,dict_orig):
		self._debug("apt_test")
		#Get dict values
		list_apt_resume=[]
		ubuntu=["deb http://archive.ubuntu.com/ubuntu jammy main restricted universe multiverse","deb http://archive.ubuntu.com/ubuntu jammy-security main restricted universe multiverse","deb http://archive.ubuntu.com/ubuntu jammy-updates main restricted universe multiverse"]
		list_apt=[]
		result_apt=["","","","",""]
		#List with repos for pinning customize
		repoList=ubuntu
		#Get debs and repos
		appsRepoDict=self._refine_apt_repoList(appDict[self.APT],dict_orig[self.APT])['return']
		repoList.extend(appsRepoDict['repos'])
		list_apt=appsRepoDict['apt']
		self.repo_customize_apt(repoList)	
		if list_apt:
			#Create token to indicator
			self._manage_indicator_token("apt","create")
			for url in repoList:
				if self.repo_add(url)['return']:
					self._debug("(apt_test) New REPO has been added to your system")
			if self.repo_update()['return']:
				self._debug("[LLXRemoteInstallerClient](apt_test) Your CACHE has been updated")
			else:
#				return [False,"failed repo_update"]
				#Delete token to indicator
				self._manage_indicator_token("apt","delete")
				return_n4d=result_apt
				return n4d.responses.build_successful_call_response(return_n4d)
		else:
#			return [False,"failed repo_add"]
			#Delete token to indicator
			self._manage_indicator_token("apt","delete")
			return_n4d=result_apt
			return n4d.responses.build_successful_call_response(return_n4d)
			#Proceed with the list, repos are updated
		self._debug("[LLXRemoteInstallerClient](apt_test) Calling apt_install with "+str(list_apt))
		result_apt_solved=self.apt_install(list_apt)['return']
		result_apt=result_apt_solved[2]
		result_apt_system=result_apt_solved[4]
		#Delete token to indicator
		self._manage_indicator_token("apt","delete")
		#Adding apps to install wich are installed in the system previously.
		if result_apt_system:
			for app in result_apt_system:
				COMMENT="Adding to installed APP: %s"%app
				self._debug(COMMENT)
				list_apt_resume.append(app)
				#Delete repo if was created by us
			
			
		#Adding apps installed in the system by remote installer.
		if result_apt:
			for app in result_apt:
				list_apt_resume.append(app)
				#Delete repo if was created by us
			self._debug("Call repo_restore")
			#self.repo_restore(self.file_sources)
		else:
			self._debug( "[LLXRemoteInstallerClient](apt_test) No apps installed")
			result_apt=["","","","",""]

		#Restore default config
		self._debug("Call repo_restore_config")
		self.repo_restore_config()	
		result_apt=list_apt_resume
		return_n4d=(result_apt)
		return n4d.responses.build_successful_call_response(return_n4d)
	#def apt_test

	def _update_results(self,dict_orig,result_deb,result_epi,result_sh,result_apt,result_update,updated):
		if not dict_orig:
			#Create dict if doesn't exists
			self._debug("[LLXRemoteInstallerClient](_update_results) Creando el diccionario.......")
			dict_new=self.create_dict ([self.APT,self.DEB,self.EPI,self.SH,self.UPDATE])['return'][2]
			dict_new[self.APT]=list(result_apt)
			dict_new[self.DEB]=list(result_deb[2])
			dict_net[self.EPI]=list(result_epi)
			dict_new[self.SH]=list(result_sh[2])
			dict_new[self.UPDATE]=result_update
			self.update_var_dict (self.N4D_INSTALLED,dict_new,"localhost")
		else:
			#Update dict
			try:
				updateDict=dict_orig[self.UPDATE]
			except:
				self._debug("Update Result: Creating new dictionarie")
				version_installed=subprocess.Popen(["lliurex-version -n"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
				version_installed=version_installed.split()[0]
				updateDict={'version':version_installed,'datetime':"None",'url':"Mirror"}
				dict_orig[self.UPDATE]=[]
				dict_orig[self.UPDATE]=updateDict
				
			
			dict_new=dict_orig
			log="[LLXRemoteInstallerClient](_update_results) Will add APT: %s ** DEBS: %s ** SH: %s ** UPDATE: %s "%(result_apt,result_deb[2],result_sh[2],result_update)
			self._debug(log)
			#Check the dict against a tuple
			dict_help=self.create_dict ([self.APT,self.DEB,self.EPI,self.SH,self.UPDATE])['return'][2]
			dict_help[self.APT]=list(result_apt)
			dict_help[self.DEB]=list(result_deb[2])
			dict_help[self.EPI]=list(result_epi)
			dict_help[self.SH]=list(result_sh[2])
			#dict_help[self.UPDATE]=result_update
			#self._debug("[LLXRemoteInstallerClient](test_system) dict to compare is "+str(dict_help))
			#Check values
			if updated == 'True':
				log="[LLXRemoteInstallerClient](_update_results) System has been updated to version: %s"%result_update['version']
				self._debug(log)
				dict_new[self.UPDATE]=result_update
			for valor_dict in dict_help:
				self._debug("[LLXRemoteInstallerClient](_update_results) Test APP from: "+valor_dict)
				try:
					for app_installed in dict_help[valor_dict]:
						ok=False
						self._debug("[LLXRemoteInstallerClient](_update_results) Check if app is installed: "+str(app_installed))
						for app_history in dict_orig[valor_dict]:
							log="[LLXRemoteInstallerClient](_update_results)  APP Installed: %s -- TESTING -- APP System: %s"%(app_installed,app_history)
							self._debug(log)
							if app_history == app_installed:
								self._debug("[LLXRemoteInstallerClient](_update_results) App exists, don't add to dict")
								ok=True
						if not ok:
							log="[LLXRemoteInstallerClient](_update_results) Adding app to list: %s"%app_installed
							self._debug(log)
							dict_new[valor_dict].append(app_installed)
						else:
							log="[LLXRemoteInstallerClient](_update_results) App hasn't been added to dict: %s"%app_installed
							self._debug(log)
				except Exception as e:
					self._debug("ERROR: "+str(e))
		return_n4d=(dict_new)
		return n4d.responses.build_successful_call_response(return_n4d)
	#def _update_results

	def test_system(self):
		try:
			#logFile="/tmp/remoteInstall.log"
			if os.path.exists(self.logFile):
				f=open (self.logFile,"a")
				f.write("\n")
				f.write("\n")
				f.write("\n")
				f.close()
			self._debug("")
			self._debug("-----------------------------------")
			self._debug("")
			self._debug("        Start Llx Remote           ")
			self._debug("      "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			self._debug("")
			self._debug("-----------------------------------")
			self._debug("")
			COMMENT="[LLXRemoteInstallerClient] (test_system) First test if exists this file %s"%(self.file_sources)
			self._debug(COMMENT)
			if os.path.exists(self.file_sources):
				COMMENT="[LLXRemoteInstallerClient] (test_system) Exists %s DELETE IT!!!"%(self.file_sources)
				os.remove(self.file_sources)
			else:
				COMMENT="[LLXRemoteInstallerClient] (test_system) NOT exists %s"%(self.file_sources)
			self._debug(COMMENT)	
			self._debug('++++++ FIN ++++++++')
			#Get installed apps dict
			self.test_var(self.N4D_INSTALLED,"localhost")
			dict_orig=self.read_var(self.N4D_INSTALLED,"localhost")['return'][2]
			#print dict_orig
			#Get server dict
			appDict=self.read_var(self.N4D_VAR)['return'][2]
			#Check the server's dict for install
			#if appDict in ["",None,"None"]:
			#print appDict
			if not appDict:
				COMMENT="[LLXRemoteInstallerClient](test_system) Variable %s do not exist in your server, do nothing"%self.N4D_VAR	
				self._debug(COMMENT)
				return [True,str(COMMENT)]
			self._debug("[LLXRemoteInstallerClient] (test_system) The DICTIONARY to use is: "+str(appDict))
			self._debug("[LLXRemoteInstallerClient] (test_system) The DICTIONARY installed in your system is: "+str(dict_orig))

			dict_orig_aux=dict_orig
			
			#Create tmp folder
			if not os.path.exists(self.dir_tmp):
				os.makedirs(self.dir_tmp)
			
			#TEST Debs
			self._debug("")
			self._debug("------------------------------------------------------------------")
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> call DEB_test")
			result_deb=self.deb_test(appDict[self.DEB],dict_orig[self.DEB])['return']
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> end DEB_test <-----")
			#TEST EPIs
			self._debug("")
			self._debug("------------------------------------------------------------------")
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> call EPI_test")
			try:
				if dict_orig[self.EPI]:
					pass
				else:
					dict_orig[self.EPI]=[]
			except Exception as e:
					dict_orig[self.EPI]=[]
					self._debug("Create intial dictionary for EPI")
			self.repo_update()
			result_epi=self.epi_test(appDict[self.EPI],dict_orig[self.EPI])['return']
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> end EPI_test <-----")
			#TEST SH
			self._debug("")
			self._debug("------------------------------------------------------------------")
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> call SH_test")
			result_sh=self.sh_test(appDict[self.SH],dict_orig[self.SH])['return']
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> end SH_test <-----")
			#TEST Apt
			self._debug("")
			self._debug("------------------------------------------------------------------")
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> call APT_test")
			result_apt=self.apt_test(appDict,dict_orig)['return']
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> end APT_test <-----")
			#TEST UPDATE
			self._debug("")
			self._debug("------------------------------------------------------------------")
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> call UPDATE_test")
			#self._debug(appDict[self.UPDATE]['activate'])
			if appDict[self.UPDATE]["activate"]=="True":
				try:
					self._debug('[LLXRemoteInstallerClient] (test_system) Calling to self.update_test ')
					result_update_vector_solved=self.update_test(appDict,dict_orig)
					self._debug('[LLXRemoteInstallerClient] (test_system) self.update_test: %s'%result_update_vector_solved)
					result_update_vector=result_update_vector_solved['return']
					#print result_update_vector
					result_update=result_update_vector[0]
					#print result_update
					updated=result_update_vector[1]
					#print updated
				except Exception as e:
					self._debug('[LLXRemoteInstallerClient] (test_system) Error in update_test: %s'%str(e))
			else:
				self._debug("AQUI ESTAMOS")
				if len(dict_orig[self.UPDATE])>0:
					#self._debug("DENTRO")
					result_update={'version':dict_orig[self.UPDATE]['version'],'url':dict_orig[self.UPDATE]['url'],'datetime':dict_orig[self.UPDATE]['datetime']}
				else:
					#self._debug("ELSE")
					result_update={}
				updated="False"
			self._debug("[LLXRemoteInstallerClient] (test_system) Updated is necessary??? : %s"%updated)
			self._debug("Updated is %s"%updated)
			self._debug("[LLXRemoteInstallerClient] (test_system) -----> end UPDATE_test <---")
			#Check that it's a list
			sh_installed=list(result_sh[2])
			#Add results to N4D dict
			dict_new=self._update_results(dict_orig,result_deb,result_epi,result_sh,result_apt,result_update,updated)['return']
#			if dict_orig in ["",None,{}]:
			log="[LLXRemoteInstallerClient] (test_system) Dict now is %s"%dict_new
			#print log
			self._debug(log)
			self._debug("[LLXRemoteInstallerClient] (test_system) Updating N4D Variable.......")
			
			#Delete system if it's necessary
			COMMENT="[LLXRemoteInstallerClient] (test_system) First test if exists this file %s"%(self.file_sources)
			self._debug(COMMENT)
			if os.path.exists(self.file_sources):
				COMMENT="[LLXRemoteInstallerClient] (test_system) Exists %s DELETE IT!!!"%(self.file_sources)
				os.remove(self.file_sources)
			else:
				COMMENT="[LLXRemoteInstallerClient] (test_system) NOT exists %s"%(self.file_sources)
			self._debug(COMMENT)
			
			#Add installed apps to N4D
			self._debug('++++INICIO UPDATE VAR++++')
			self.update_var_dict (self.N4D_INSTALLED,dict_new,"localhost")
			self._debug('++++Fin UPDATE VAR++++')
			if updated == 'False':
				COMMENT="The system has been configured with the APPS: %s * has executed the scripts: %s * Installed new DEBS: %s * Installed new EPIS: %s"%(result_apt,sh_installed,result_deb[2],result_epi)
			else:
				COMMENT="The system has been configured with the APPS: %s * has executed the scripts: %s * Installed new DEBS: %s  * Installed new EPIS: %s * Updated to: %s"%(result_apt,sh_installed,result_deb[2],result_epi,result_update['version'])
			self._debug(COMMENT)
			#print COMMENT
			return_n4d=[True,str(COMMENT),result_apt,result_sh[2],result_deb[2],updated,dict_new]
			return n4d.responses.build_successful_call_response(return_n4d)
		except Exception as e:
			self._debug("EXCEPTION "+str(e))
			#return[False,str(e)]
			COMMENT="[LLXRemoteInstallerClient] (test_system) Error: %e"%(e)
			return n4d.responses.build_successful_call_response([False,str(COMMENT)])
	
	#def test_system

	def _manage_indicator_token(self,action_type,action):
		
		if action_type=="deb":
			f=os.path.join(self.dir_tmp,"llxremote_deb_token")
		elif action_type=="epi":
			f=os.path.join(self.dir_tmp,"llxremote_epi_token")
		elif action_type=="sh":
			f=os.path.join(self.dir_tmp,"llxremote_sh_token")
		elif action_type=="apt":
			f=os.path.join(self.dir_tmp,"llxremote_apt_token")
			
		if action=="create":
			self._debug("Create token to indicator")
			try:
				if not os.path.exists(f):
					tmp=open(f,'w')
					tmp.close()
			except Exception as e:
				self._debug("ERROR: "+str(e))
				pass
		elif action=="delete":
			self._debug("Delete token to indicator")
			try:
				if  os.path.exists(f):
					os.remove(f)
			except Exception as e:
				self._debug("ERROR: "+str(e))
				pass
		return

	#def _manage_indicator_token	
