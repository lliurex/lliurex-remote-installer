import LliurexRemoteInstaller
import AptBox
import DebBox
import ExecBox
import ZeroBox
import UpdateBox
import N4dManager
import os
import sys


class Core:
	
	singleton=None
	DEBUG=False
	os.chdir(sys.path[0])
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):
		
		self.dprint("Init...")
		self.var=None
		
	#def __init__
	
	def init(self):
		
		self.dprint("Creating N4D client...")
		self.n4d=N4dManager.N4dManager()
		
		
		self.dprint("Creating AptBox...")
		self.apt_box=AptBox.AptBox()
		
		self.dprint("Creating DebBox...")
		self.deb_box=DebBox.DebBox()
		
		self.dprint("Creating ExecBox...")
		self.exec_box=ExecBox.ExecBox()

		self.dprint("Creating ZeroBox...")
		self.zero_box=ZeroBox.ZeroBox()
		
		self.dprint("Creating UpdateBox...")
		self.update_box=UpdateBox.UpdateBox()
		
		# ####
		
		# #########
		
		# Main window must be the last one
		self.dprint("Creating LliurexRemoteInstaller...")
		self.lri=LliurexRemoteInstaller.LliurexRemoteInstaller()
		
		self.lri.load_gui()
		self.lri.start_gui()
		
		
	#def init
	
	
	
	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
