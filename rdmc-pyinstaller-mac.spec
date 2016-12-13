###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

# -*- mode: python -*-
import os

block_cipher = None

def hiddenImportGet():
	tl = []
	classNames = []
	_Commands = {}

	extensionDir = os.path.dirname(os.getcwd()+ '/src')

	replacement = '/'

	for (cwd, dirs, filenames) in os.walk(extensionDir):
		dirs[:] = [d for d in dirs if not d[0] == '.']
		tl.append((cwd,[files for files in filenames if not files[0] == '.']))

	for cwd, names in tl:
		cn = cwd.split('extensions')[-1]
		cn = cn.replace(replacement, '.')
		for name in names:
			if '.pyc' not in name and '__init__' not in name:
				name = name.replace('.py', '')
				classNames.append('extensions'+cn+'.'+name)
	return classNames

a = Analysis(['.//src//rdmc.py'],
             pathex=[],
             binaries=None,
             datas=[('.//src//extensions', 'extensions')],
             hiddenimports=hiddenImportGet(),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             cipher=block_cipher)


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='redfish',
          debug=False,
          strip=None,
          upx=True,
	  icon='',
          console=True )
