###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

""" Commit Command for RDMC """

import sys

from optparse import OptionParser
from rdmc_helper import ReturnCodes, InvalidCommandLineErrorOPTS, \
                        NoChangesFoundOrMadeError, NoCurrentSessionEstablished

from rdmc_base_classes import RdmcCommandBase

class CommitCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='commit',\
            usage='commit [OPTIONS]\n\n\tRun to apply all changes made during the' \
                    ' current session\n\texample: commit',\
            summary='Applies all the changes made during the current' \
                    ' session.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def commitfunction(self, options=None):
        """ Main commit worker function

        :param options: command line options
        :type options: list.
        """
        self.commitvalidation()

        sys.stdout.write(u"Committing changes...\n")

        try:
            if not self._rdmc.app.commit(verbose=self._rdmc.opts.verbose):
                raise NoChangesFoundOrMadeError("No changes found or made " \
                                                    "during commit operation.")
        except Exception:
            raise

        self.logoutobj.logoutfunction("")

    def run(self, line):
        """ Wrapper function for commit main function
        
        :param line: command line input
        :type line: string.
        """
        try:
            (options, _) = self._parse_arglist(line)
        except:
            if ("-h" in line) or ("--help" in line):
                return ReturnCodes.SUCCESS
            else:
                raise InvalidCommandLineErrorOPTS("")

        self.commitfunction(options)

        #Return code
        return ReturnCodes.SUCCESS

    def commitvalidation(self):
        """ Commit method validation function """
        try:
            self._rdmc.app.get_current_client()
        except:
            raise NoCurrentSessionEstablished("Please login and make setting" \
                                      " changes before using commit command.")

    def definearguments(self, customparser):
        """ Wrapper function for new command main function

        :param customparser: command line input
        :type customparser: parser.
        """
        if not customparser:
            return

