import xmlrpc.client 
import ssl
import os

import n4d.client
import n4d.server.core as n4dcore

class N4dManager:
	
	
	def __init__(self):
		
		self.N4D_VAR="LLX_REMOTE_INSTALLER"
		self.debug=False
		if self.debug:
			print("[LliureXRemoteInstaller] Debug mode activated")

		
	#def init



	def mprint(self,msg):
		
		if self.debug:
			print("[LliureXRemoteInstaller_N4DManager] %s"%str(msg))
			
	#def mprint
	
	
	def lliurex_version(self):
		
		try:
		
			#self.mprint(self.client.lliurex_version("","LliurexVersion"))
			self.mprint(self.client.LliurexVersion.lliurex_version())
			return True
			
		except Exception as e:
			self.mprint(e)
			return False		
	#def


	
	def lliurex_mirror(self):
		try:
			#variable=self.client.lliurex_version("","LliurexVersion","-m")
			variable=self.client.LliurexVersion.lliurex_version("-m")
			#self.mprint(variable)
			return[True,variable]
			
		except Exception as e:
			self.mprint(e)
			return False
		
	#def lliurex_mirror
	
	def mirror_version(self):
		try:
			#mirror_checked=self.client.mirror_version(self.user,"LliureXRemoteInstaller")
			mirror_checked=self.client.LliureXRemoteInstaller.mirror_version()
			self.mprint('mirror_version %s'%mirror_checked)
			version='False'
			if mirror_checked[0]:
				version=mirror_checked[1]

			return[True,version]
			
		except Exception as e:
			self.mprint(e)
			return False
		
	#def lliurex_mirror
	
	def net_mirror_version(self):
		try:
			mirror_checked=self.client.LliureXRemoteInstaller.net_mirror_version()
			self.mprint(mirror_checked)
			version='False'
			if mirror_checked[0]:
				version=mirror_checked[1]

			return[True,version]
			
		except Exception as e:
			self.mprint(e)
			return False
		
	#def net_lliurex_mirror
	
	def test_var (self):
		
		try:
			#self.variable=self.client.test_var(self.user,"LliureXRemoteInstaller",self.N4D_VAR,self.user[0],self.user[1])
			self.mprint('(test_var) Call N4D function..')
			self.variable=self.client.LliureXRemoteInstaller.test_var(self.N4D_VAR)
			self.mprint('(test_var) self.variable is: %s'%self.variable)
			return[True,self.variable]
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def ge
	

	def get_variable (self):
		
		try:
			
			#self.variable=self.client.get_variable(self.user,"VariablesManager",self.N4D_VAR)
			self.mprint('(get_variable) Call N4D function..')
			self.variable=self.client.get_variable(self.N4D_VAR)
			self.mprint('(get_variable) VAR is: %s'%self.variable)
			return[True,self.variable]
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def get_value
	
	
	
	def set_variable (self,dict_var):
		
		try:
			#self.variable.update(dict)
			dict_orig=self.get_variable()
			#self.mprint dict_orig
			#write_log=self.client.write_log(self.user,"LliureXRemoteInstaller",self.user[0],dict,dict_orig[1])
			write_log=self.client.LliureXRemoteInstaller.write_log(dict_var,dict_orig[1])
			solved=self.client.set_variable(self.N4D_VAR,dict_var)
			self.mprint('(set_variable) %s'%solved)
			if solved:
				return True
			else:
				return False
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def set_variable
	
	
	
	def test_apt_list (self,dict_var):
		
		try:
			#list_apt_ok=self.client.test_apt_list(self.user,"LliureXRemoteInstaller",dict_var)
			list_apt_ok=self.client.LliureXRemoteInstaller.test_apt_list(dict_var)
			#list_apt_ok.wait()
			#self.mprint list_apt_ok
			if list_apt_ok[0]:
				return list_apt_ok
			else:
				return list_apt_ok
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def set_variable
	
	def test_deb_list (self,dict_var):
		
		try:
			#list_deb_ok=self.client.test_deb_list(self.user,"LliureXRemoteInstaller",dict)
			list_deb_ok=self.client.LliureXRemoteInstaller.test_deb_list(dict_var)
			#list_apt_ok.wait()
			self.mprint('(N4dManager)(test_deb_list) %s'%list_deb_ok)
			if list_deb_ok[0]:
				return list_deb_ok
			else:
				return list_deb_ok
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def set_variable
	
	def test_list (self,dict_var,type):
		
		try:
			#list_deb_ok=self.client.test_list(self.user,"LliureXRemoteInstaller",dict,type)
			list_deb_ok=self.client.LliureXRemoteInstaller.test_list(dict_var,type)
			self.mprint(list_deb_ok)
			return list_deb_ok
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def test_list
	
	def app_deb_exist (self,app=None,url=None):
		try:
			#app_deb_tested=self.client.app_deb_exist(self.user,"LliureXRemoteInstaller",app,url)
			app_deb_tested=self.client.LliureXRemoteInstaller.app_deb_exist(app,url)
			return app_deb_tested
			
		except Exception as e:
			self.mprint(e)
			return False
			
		
	def send_file(self,ip,url_source,url_dest):
		
		try:
			#context=ssl._create_unverified_context()
			#local_n4d=xmlrpc.client.ServerProxy("https://localhost:9779",allow_none=True,context=context)
			#file_sent=local_n4d.send_file(self.user,"ScpManager",self.user[0],self.user[1],ip,url_source,url_dest)
			self.mprint('(send_file) Calling to scpmanager User: %s - Passwd: %s - IP: %s - Url_Source: %s - Url_dest: %s'%(self.user[0],self.user[1],ip,url_source,url_dest))
			file_sent=self.local_client.ScpManager.send_file(self.user[0],self.user[1],ip,url_source,url_dest)
			self.mprint('(send_file) %s'%file_sent)
			#list_apt_ok.wait()
			if file_sent:
				return True
			else:
				return False
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def set_variable
	
	def remove_file(self,file):
		
		try:
			#file_sended=self.client.remove_file(self.user,"LliureXRemoteInstaller",file)
			file_sended=self.client.LliureXRemoteInstaller.remove_file(file)
			#list_apt_ok.wait()
			return file_sended
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def set_variable
	
	def set_server(self,server_ip):
		
		#context=ssl._create_unverified_context()	
		#self.client=xmlrpc.client.ServerProxy("https://%s:9779"%server,allow_none=True,context=context)
		try:
			if server_ip in {'',None}:
				server_ip="server"
			self.server_ip=server_ip
			self.server="https://%s:9779"%server_ip
			self.mprint("(set_server) Proxy: %s"%self.server)
			return self.server
		except Exception as e:
			msg_log="(set_server) Error: %s"%(str(e))
			self.mprint(msg_log)		
	
	#def set_server

	
	def validate_user(self,username,password,server_ip):
		try:
			self.mprint('(validate_user)Validating user: %s'%username)
			self.server=self.set_server(server_ip)
			self.client=n4d.client.Client(self.server,username,password)
			self.mprint('(validate_user) sel.client: %s'%self.client)

			ret=self.client.validate_user()
			self.mprint('(validate_user) ret: %s'%ret)
			self.user_validated=ret[0]
			self.user_groups=ret[1]
			self.credentials=[username,password]
		
			if self.user_validated:
				self.user=[username,password]
				session_user=os.environ["USER"]
				self.ticket=self.client.get_ticket()
				if self.ticket.valid():
					self.client=n4d.client.Client(ticket=self.ticket)
					msg_log="Session User: %s"%session_user+" LlXRemoreInstaller User: %s"%username
					self.mprint(msg_log)
					
					self.local_client=n4d.client.Client("https://localhost:9779",username,password)
					local_t=self.local_client.get_ticket()
					if local_t.valid():
						self.local_client=n4d.client.Client(ticket=local_t)
					else:
						self.user_validated=False	
				else:
					self.user_validated=False
			self.mprint(self.user_groups)

		except Exception as e:
			msg_log="(validate_user)Session User Error: %s"%(str(e))
			self.mprint(msg_log)
			self.user_validated=False

	#def validate_user




	def list_available_epis(self):
		
		try:
			#file_sended=self.client.list_available_epis(self.user,"LliureXRemoteInstaller")
			file_sended=self.client.LliureXRemoteInstaller.list_available_epis()
			#list_apt_ok.wait()
			return file_sended
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def list_available_epis

	def epi_deb(self,epi_pkg):
		
		try:
			#file_sended=self.client.epi_deb(self.user,"LliureXRemoteInstaller",epi_pkg)
			file_sended=self.client.LliureXRemoteInstaller.epi_deb(epi_pkg)
			#list_apt_ok.wait()
			return file_sended
		
		except Exception as e:
			self.mprint(e)
			return False
		
	#def epi_deb
	
	
#class n4dmanager
