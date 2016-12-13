###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-library/blob/master/LICENSE.md
###

# -*- coding: utf-8 -*-
""" Logout Command for RDMC """

import sys

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase

from rdmc_helper import ReturnCodes, InvalidCommandLineErrorOPTS

class LogoutCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='logout',\
            usage='logout\n\n\tRun to end the current session and disconnect' \
                    ' from the server\n\texample: logout',\
            summary='Ends the current session and disconnects from the' \
                    ' server.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj

    def logoutfunction(self, line):
        """ Main logout worker function

        :param line: command line input
        :type line: string.
        """
        try:
            (_, _) = self._parse_arglist(line)
        except:
            if ("-h" in line) or ("--help" in line):
                return ReturnCodes.SUCCESS
            else:
                raise InvalidCommandLineErrorOPTS("")

        self._rdmc.app.logout("")

    def run(self, line):
        """ Wrapper function for main logout function

        :param line: command line input
        :type line: string.
        """
        try:
            sys.stdout.write(u"Logging session out.\n")
            self.logoutfunction(line)
        except Exception, excp:
            raise excp

        #Return code
        return ReturnCodes.SUCCESS

    def definearguments(self, customparser):
        """ Wrapper function for new command main function

        :param customparser: command line input
        :type customparser: parser.
        """
        if not customparser:
            return

