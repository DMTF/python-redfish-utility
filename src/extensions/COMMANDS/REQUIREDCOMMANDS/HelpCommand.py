""" Help Command for RDMC """

import sys

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase, RdmcOptionParser
from rdmc_helper import ReturnCodes, InvalidCommandLineError, \
                    InvalidCommandLineErrorOPTS

class HelpCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, **kwargs):
        RdmcCommandBase.__init__(self,\
            name='help',\
            usage='help [COMMAND]\n\n\tFor more detailed command descriptions' \
                    ' use the help command feature\n\texample: help login',\
            summary='Displays command line syntax and'\
                    ' help menus for individual commands.'\
                    ' Example: help login',\
            aliases=[],\
            optparser=OptionParser())
        self.config_required = False
        self._rdmc = None
        if 'rdmc' in kwargs:
            self._rdmc = kwargs['rdmc']

    def run(self, line):
        """ Wrapper function for help main function

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
            RdmcOptionParser().print_help()
            if self._rdmc:
                cmddict = self._rdmc.get_commands()
                sorted_keys = cmddict.keys()
                sorted_keys.sort()

                for key in sorted_keys:
                    if key[0] == '_':
                        continue
                    else:
                        sys.stdout.write(u'\n%s\n' % key)

                    for cmd in cmddict[key]:
                        cmd.print_summary()
        else:
            if self._rdmc:
                cmddict = self._rdmc.get_commands()
                sorted_keys = cmddict.keys()
                for key in sorted_keys:
                    for cmd in cmddict[key]:
                        if cmd.ismatch(args[0]):
                            cmd.print_help()
                            return

                raise InvalidCommandLineError("Command '%s' not found." % args[0])
        #Return code
        return ReturnCodes.SUCCESS

