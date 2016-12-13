# -*- coding: utf-8 -*-
""" New Command for RDMC """

import sys

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import ReturnCodes, InvalidCommandLineErrorOPTS

class NewCommand(RdmcCommandBase):
    """ Main new command template class """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='newcommand',\
            usage='newcommand [OPTIONS]\n\n\tRun to show the new command is ' \
                'working\n\texample: newcommand',\
            summary='New command tutorial.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj

    def newcommandfunction(self, options=None):
        """ Main new command worker function

        :param options: command options
        :type options: options.
        """
        self.newcommandvalidation()

        # TODO: This is where you would add your main worker code
        #       Refer to other commands for an example of this function
        sys.stdout.write(u"Hello World. It's me %s.\n" % options.name)

    def run(self, line):
        """ Wrapper function for new command main function

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

        self.newcommandfunction(options)

        #Return code
        return ReturnCodes.SUCCESS

    def newcommandvalidation(self):
        """ new command method validation function """
        try:
			# TODO: Any validation required need to be placed here.
			#       Refer to other commands for an example of this function
            pass
        except:
            raise

    def definearguments(self, customparser):
        """ Wrapper function for new command main function

        :param customparser: command line input
        :type customparser: parser.
        """
        if not customparser:
            return

        # TODO: This is where you add all your command line arguments.
        #       For more information on this section research optparse for python

        customparser.add_option(
            '--name',
            dest='name',
            help="""Use the provided the output name.""",
            default="REDFISH",
        )

