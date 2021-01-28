from epi import epimanager as EpiManager
import json
import sys

#N4D es python2 y LlX Remote Installer es Python3, no puedo trabajar con librerias de EPI. Utilizo este script a modo de puente.
try:
	epi_operation=sys.argv[1]

	epi=EpiManager.EpiManager()
	epi_to_exec="epi."+epi_operation

	epi_solved={}
	exec("epi_solved['val']=%s"%epi_to_exec)

	data=json.dumps(epi_solved['val'])
	print (data)

except Exception as e:
	print('False')
