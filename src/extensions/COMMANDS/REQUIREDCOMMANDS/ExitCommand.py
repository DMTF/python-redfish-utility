###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

""" Exit Command for rdmc """

import sys

from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import ReturnCodes, InvalidCommandLineErrorOPTS

class ExitCommand(RdmcCommandBase):
    """ Exit class to handle exiting from interactive mode """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='exit',\
            usage='exit\n\n\tRun to exit from the interactive shell\n\t' \
            'example: exit',\
            summary='Exits from the interactive shell.',\
            aliases=['quit'])

        self._rdmc = rdmcObj
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def run(self, line):
        """If an argument is present, print help else exit

        :param line: command line input
        :type line: string.
        """
        try:
            (_, args) = self._parse_arglist(line)
        except:
            if ("-h" in line) or ("--help" in line):
                return ReturnCodes.SUCCESS
            else:
                raise InvalidCommandLineErrorOPTS("")

        if args is None or len(args) == 0 or not line:
            self.logoutobj.run("")
            sys.stdout.write('Bye for now\n')

            #System exit
            sys.exit(ReturnCodes.SUCCESS)
        else:
            sys.stderr.write("Exit command does not take any parameters.\n")
            raise InvalidCommandLineErrorOPTS("Invalid command line arguments.")