###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/main/LICENSE.md
###

import os
import sys
tl = []
classNames = []
_Commands = {}

extensionDir = os.path.dirname(__file__)

if os.name != 'nt':
    replacement = '/'
else:
    replacement = '\\'

for (cwd, dirs, filenames) in os.walk(extensionDir):
    dirs[:] = [d for d in dirs if not d[0] == '.']
    tl.append((cwd, [files for files in filenames if not files[0] == '.']))

for cwd, names in tl:
    cn = cwd.split('extensions')[-1]
    cn = cn.replace(replacement, '.')
    for name in names:
        if name.endswith('.py') and '__' not in name:
            name = name.replace('.py', '')
            classNames.append(cn+'.'+name+'.'+name)