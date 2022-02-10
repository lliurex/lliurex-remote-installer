#!/usr/bin/env python3
#
# $Id: setup.py,v 1.32 2010/10/17 15:47:21 ghantoos Exp $
#
#    Copyright (C) 2008-2009  Ignace Mouzannar (ghantoos) <ghantoos@ghantoos.org>
#
#    This file is part of lshell
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
import sys


if __name__ == '__main__':
	
	setup(name='llxremote_cli',
		version='0.1',
		description='Lliurex Remote Installer.CLI tool',
		long_description="""""",
		author='Lliurex Team',
		author_email='daduve@gmail.com',
		maintainer='Daniel Durán Vecino',
		maintainer_email='daduve@gmail.com',
		keywords=['software','instalar'],
		url='http://www.lliurex.net',
		license='GPL',
		platforms='UNIX',
		packages = ['llxremotecli'],
		package_dir = {'llxremotecli':'llxremote-cli'},
		data_files = [('sbin',['llxremote-cli/llxremote'])],
		classifiers=[
			'Development Status :: 1 - Beta',
			'Environment :: Console'
			'Intended Audience :: End Users',
			'License :: OSI Approved :: GNU General Public License v3',
			'Operating System :: POSIX',
			'Programming Language :: Python',
			'Topic :: Software',
			'Topic :: Install apps',
			],
	)
