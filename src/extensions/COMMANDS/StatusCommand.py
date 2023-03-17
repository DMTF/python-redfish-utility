###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/main/LICENSE.md
###

""" Status Command for RDMC """

import sys

from optparse import OptionParser
from rdmc_helper import ReturnCodes, \
                    InvalidCommandLineErrorOPTS

from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import NoCurrentSessionEstablished

class StatusCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='status',\
            usage='status\n\n\tRun to display all pending changes within'\
                    ' the currently\n\tselected type and that need to be' \
                    ' committed\n\texample: status',\
            summary='Displays all pending changes within a selected type'\
                    ' that need to be committed.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj
        self.selobj = rdmcObj.commandsDict["SelectCommand"](rdmcObj)

    def run(self, line):
        """ Main status worker function

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

        self.statusvalidation()
        contents = self._rdmc.app.status()
        selector = self._rdmc.app.get_selector()

        if contents:
            self.outputpatches(contents, selector)
        else:
            sys.stdout.write("No changes found\n")

        #Return code
        return ReturnCodes.SUCCESS

    def outputpatches(self, contents, selector):
        """ Helper function for status for use in patches
        
        :param contents: contents for the selection
        :type contents: string.
        :param selector: type selected
        :type selector: string.
        """
        sys.stdout.write("Current changes found:\n")
        for item in contents:
            for key, value in item.items():
                if selector and key.lower().startswith(selector.lower()):
                    sys.stdout.write("%s (Currently selected)\n" % key)
                else:
                    sys.stdout.write("%s\n" % key)
                for content in value:
                    try:
                        if isinstance(content[0]["value"], int):
                            sys.stdout.write('\t%s=%s' % \
                                 (content[0]["path"][1:], content[0]["value"]))
                        elif not isinstance(content[0]["value"], bool) and \
                                            not len(content[0]["value"]) == 0:
                            if content[0]["value"][0] == '"' and \
                                                content[0]["value"][-1] == '"':
                                sys.stdout.write('\t%s=%s' % \
                                                    (content[0]["path"][1:], \
                                                    content[0]["value"][1:-1]))
                            else:
                                sys.stdout.write('\t%s=%s' % \
                                                    (content[0]["path"][1:], \
                                                     content[0]["value"]))
                        else:
                            output = content[0]["value"]

                            if not isinstance(output, bool):
                                if len(output) == 0:
                                    output = '""'

                            sys.stdout.write('\t%s=%s' % \
                                             (content[0]["path"][1:], output))
                    except:
                        if isinstance(content["value"], int):
                            sys.stdout.write('\t%s=%s' % \
                                 (content["path"][1:], content["value"]))
                        elif not isinstance(content["value"], bool) and \
                                                not len(content["value"]) == 0:
                            if content["value"][0] == '"' and \
                                                    content["value"][-1] == '"':
                                sys.stdout.write('\t%s=%s' % \
                                                        (content["path"][1:], \
                                                        content["value"]))
                            else:
                                sys.stdout.write('\t%s=%s' % \
                                                        (content["path"][1:], \
                                                        content["value"]))
                        else:
                            output = content["value"]

                            if not isinstance(output, bool):
                                if len(output) == 0:
                                    output = '""'

                            sys.stdout.write('\t%s=%s' % \
                                                (content["path"][1:], output))
                    sys.stdout.write('\n')


    def statusvalidation(self):
        """ Status method validation function """
        try:
            self._rdmc.app.get_current_client()
        except:
            raise NoCurrentSessionEstablished("Please login and make setting" \
                                      " changes before using status command.")

    def definearguments(self, customparser):
        """ Wrapper function for new command main function

        :param customparser: command line input
        :type customparser: parser.
        """
        if not customparser:
            return

