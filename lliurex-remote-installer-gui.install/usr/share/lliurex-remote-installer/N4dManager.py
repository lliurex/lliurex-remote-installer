import xmlrpclib

class N4dManager:
	
	
	
	def __init__(self):
		
		
		self.N4D_VAR="LLX_REMOTE_INSTALLER"
		
	#def init
	
	
	def lliurex_version(self):
		
		try:
		
			print self.client.lliurex_version("","LliurexVersion")
			return True
			
		except Exception as e:
			print e
			return False
			
			
		
	#def
	
	def lliurex_mirror(self):
		try:
			variable=self.client.lliurex_version("","LliurexVersion","-m")[1]
			#print variable
			return[True,variable]
			
		except Exception as e:
			print e
			return False
		
	#def lliurex_mirror
	
	def mirror_version(self):
		try:
			mirror_checked=self.client.mirror_version(self.user,"LliureXRemoteInstaller")
			version='False'
			if mirror_checked[0]:
				version=mirror_checked[1]

			return[True,version]
			
		except Exception as e:
			print e
			return False
		
	#def lliurex_mirror
	
	def net_mirror_version(self):
		try:
			mirror_checked=self.client.net_mirror_version(self.user,"LliureXRemoteInstaller")
			version='False'
			if mirror_checked[0]:
				version=mirror_checked[1]

			return[True,version]
			
		except Exception as e:
			print e
			return False
		
	#def net_lliurex_mirror
	
	def test_var (self):
		
		try:
			self.variable=self.client.test_var(self.user,"LliureXRemoteInstaller",self.N4D_VAR,self.user[0],self.user[1])
			return[True,self.variable]
		
		except Exception as e:
			print e
			return False
		
	#def ge
	

	def get_variable (self):
		
		try:
			
			self.variable=self.client.get_variable(self.user,"VariablesManager",self.N4D_VAR)
			return[True,self.variable]
		
		except Exception as e:
			print e
			return False
		
	#def get_value
	
	
	
	def set_variable (self,dict):
		
		try:
			#self.variable.update(dict)
			dict_orig=self.get_variable()
			#print dict_orig
			write_log=self.client.write_log(self.user,"LliureXRemoteInstaller",self.user[0],dict,dict_orig[1])
			if self.client.set_variable(self.user,"VariablesManager",self.N4D_VAR,dict)[0]:
				return True
			else:
				return False
		
		except Exception as e:
			print e
			return False
		
	#def set_variable
	
	
	
	def test_apt_list (self,dict):
		
		try:
			list_apt_ok=self.client.test_apt_list(self.user,"LliureXRemoteInstaller",dict)
			#list_apt_ok.wait()
			#print list_apt_ok
			if list_apt_ok[0]:
				return list_apt_ok
			else:
				return list_apt_ok
		
		except Exception as e:
			print e
			return False
		
	#def set_variable
	
	def test_deb_list (self,dict):
		
		try:
			list_deb_ok=self.client.test_deb_list(self.user,"LliureXRemoteInstaller",dict)
			#list_apt_ok.wait()
			if list_deb_ok[0]:
				return list_deb_ok
			else:
				return list_deb_ok
		
		except Exception as e:
			print e
			return False
		
	#def set_variable
	
	def test_list (self,dict,type):
		
		try:
			list_deb_ok=self.client.test_list(self.user,"LliureXRemoteInstaller",dict,type)
			print list_deb_ok
			return list_deb_ok
		
		except Exception as e:
			print e
			return False
		
	#def test_list
	
	def app_deb_exist (self,app=None,url=None):
		try:
			app_deb_tested=self.client.app_deb_exist(self.user,"LliureXRemoteInstaller",app,url)
			return app_deb_tested
			
		except Exception as e:
			print e
			return False
			
		
	def send_file(self,ip,url_source,url_dest):
		
		try:
			
			local_n4d=xmlrpclib.ServerProxy("https://localhost:9779")
			file_sent=local_n4d.send_file(self.user,"ScpManager",self.user[0],self.user[1],ip,url_source,url_dest)
			
			#list_apt_ok.wait()
			if file_sent["status"]:
				return True
			else:
				return False
		
		except Exception as e:
			print e
			return False
		
	#def set_variable
	
	def remove_file(self,file):
		
		try:
			file_sended=self.client.remove_file(self.user,"LliureXRemoteInstaller",file)
			#list_apt_ok.wait()
			return file_sended
		
		except Exception as e:
			print e
			return False
		
	#def set_variable
	
	
	def validate_user(self,username,password,server_ip):
		
		try:
			if server_ip in {'',None}:
				server_ip="server"
			if server_ip in {'localhost'}:
				proxy="https://localhost:9779"
				#print proxy
				self.client=xmlrpclib.ServerProxy(proxy)
			else:
				proxy="https://%s:9779"%server_ip
				#print proxy
				self.client=xmlrpclib.ServerProxy(proxy)
			
			self.server=server_ip
				
			ret=self.client.validate_user(username,password)
			if ret[0]:
				if "admins" in ret[1]:
					self.user=(username,password)
					return [True,""]
				else:
					return [False,"User is not allowed to use this application, only netadmins users"]
					
			return [False,"Wrong user and/or password"]
			
		except Exception as e:
			print e
			return [False,str(e)]
		
		
	#def validate_user
	
	
#class n4dmanager