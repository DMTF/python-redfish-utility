###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

""" Save Command for RDMC """

import sys
import json
import redfish.ris

from optparse import OptionParser
from collections import (OrderedDict)
from rdmc_helper import ReturnCodes, \
                    InvalidCommandLineErrorOPTS

from rdmc_base_classes import RdmcCommandBase, HARDCODEDLIST
from rdmc_helper import InvalidCommandLineError, InvalidFileFormattingError

#default file name
__filename__ = 'redfish.json'

class SaveCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='save',\
            usage='save [OPTIONS]\n\n\tRun to save a selected type to a file' \
            '\n\texample: save --selector ComputerSystem.\n\n\tChange the ' \
            'default output filename\n\texample: save --selector ' \
            'ComputerSystem. -f output.json',\
            summary=u"Saves the selected type's settings to a file.",\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self.filename = None
        self._rdmc = rdmcObj
        self.lobobj = rdmcObj.commandsDict["LoginCommand"](rdmcObj)
        self.selobj = rdmcObj.commandsDict["SelectCommand"](rdmcObj)
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def run(self, line):
        """ Main save worker function

        :param line: command line input
        :type line: string.
        """
        try:
            (options, args) = self._parse_arglist(line)
        except:
            if ("-h" in line) or ("--help" in line):
                return ReturnCodes.SUCCESS
            else:
                raise InvalidCommandLineErrorOPTS("")

        self.savevalidation(options)

        if not len(args) == 0:
            raise InvalidCommandLineError('Save command takes no arguments.')

        contents = self._rdmc.app.get_save(args, pluspath=True)
        type_string = self._rdmc.app.current_client.monolith._typestring

        if not contents:
            raise redfish.ris.NothingSelectedError
        else:
            sys.stdout.write("Saving configuration...\n")
            templist = list()

            for content in contents:
                typeselector = None
                pathselector = None

                for path, values in content.iteritems():
                    values = OrderedDict(sorted(values.items(),\
                                                         key=lambda x: x[0]))

                    for dictentry in values.keys():
                        if dictentry == type_string:
                            typeselector = values[dictentry]
                            pathselector = path
                            del values[dictentry]
                        elif dictentry.lower() in HARDCODEDLIST or '@odata' in \
                                                              dictentry.lower():
                            del values[dictentry]

                    if len(values):
                        tempcontents = dict()
                        if typeselector and pathselector:
                            tempcontents[typeselector] = {pathselector: values}
                        else:
                            raise InvalidFileFormattingError("Missing path or" \
                                                     " selector in input file.")

                    templist.append(tempcontents)
            contents = templist

        if not contents:
            raise redfish.ris.NothingSelectedError
        else:
            contents = self.add_save_file_header(contents)

        outfile = open(self.filename, 'w')
        outfile.write(json.dumps(contents, indent=2, \
                                                cls=redfish.ris.JSONEncoder))
        outfile.close()
        sys.stdout.write("Configuration saved to: %s\n" % self.filename)

        if options.logout:
            self.logoutobj.logoutfunction("")

        #Return code
        return ReturnCodes.SUCCESS

    def savevalidation(self, options):
        """ Save method validation function

        :param options: command line options
        :type options: list.
        """
        inputline = list()

        if self._rdmc.app.config._ac__format.lower() == 'json':
            options.json = True

        try:
            self._rdmc.app.get_current_client()
        except:
            if options.user or options.password or options.url:
                if options.url:
                    inputline.extend([options.url])
                if options.user:
                    inputline.extend(["-u", options.user])
                if options.password:
                    inputline.extend(["-p", options.password])
            else:
                if self._rdmc.app.config.get_url():
                    inputline.extend([self._rdmc.app.config.get_url()])
                if self._rdmc.app.config.get_username():
                    inputline.extend(["-u", \
                                  self._rdmc.app.config.get_username()])
                if self._rdmc.app.config.get_password():
                    inputline.extend(["-p", \
                                  self._rdmc.app.config.get_password()])

        if len(inputline) and options.selector:
            if options.filter:
                inputline.extend(["--filter", options.filter])
            if options.includelogs:
                inputline.extend(["--includelogs"])
            if options.path:
                inputline.extend(["--path", options.path])

            inputline.extend(["--selector", options.selector])
            self.lobobj.loginfunction(inputline)
        elif options.selector:
            if options.filter:
                inputline.extend(["--filter", options.filter])
            if options.includelogs:
                inputline.extend(["--includelogs"])
            if options.path:
                inputline.extend(["--path", options.path])

            inputline.extend([options.selector])
            self.selobj.selectfunction(inputline)
        else:
            try:
                inputline = list()
                selector = self._rdmc.app.get_selector()
                if options.filter:
                    inputline.extend(["--filter", options.filter])
                if options.includelogs:
                    inputline.extend(["--includelogs"])
                if options.path:
                    inputline.extend(["--path", options.path])

                inputline.extend([selector])
                self.selobj.selectfunction(inputline)
            except:
                raise redfish.ris.NothingSelectedError

        #filename validations and checks
        self.filename = None

        if options.filename and len(options.filename) > 1:
            raise InvalidCommandLineError(u"Save command doesn't support " \
                    "multiple filenames.")
        elif options.filename:
            self.filename = options.filename[0]
        elif self._rdmc.app.config:
            if self._rdmc.app.config._ac__savefile:
                self.filename = self._rdmc.app.config._ac__savefile

        if not self.filename:
            self.filename = __filename__

    def add_save_file_header(self, contents):
        """ Helper function to retrieve the comments for save file

        :param contents: current save contents
        :type contents: list.
        """
        templist = list()

        headers = self._rdmc.app.get_save_header()
        templist.append(headers)

        for content in contents:
            templist.append(content)

        return templist

    def definearguments(self, customparser):
        """ Wrapper function for new command main function

        :param customparser: command line input
        :type customparser: parser.
        """
        if not customparser:
            return

        customparser.add_option(
            '--url',
            dest='url',
            help="Use the provided URL to login.",
            default=None,
        )
        customparser.add_option(
            '-u',
            '--user',
            dest='user',
            help="If you are not logged in yet, including this flag along"\
            " with the password and URL flags can be used to log into a"\
            " server in the same command.""",
            default=None,
        )
        customparser.add_option(
            '-p',
            '--password',
            dest='password',
            help="""Use the provided password to log in.""",
            default=None,
        )
        customparser.add_option(
            '--logout',
            dest='logout',
            action="store_true",
            help="Optionally include the logout flag to log out of the"\
            " server after this command is completed. Using this flag when"\
            " not logged in will have no effect",
            default=None,
        )
        customparser.add_option(
            '--includelogs',
            dest='includelogs',
            action="store_true",
            help="Optionally include logs in the data retrieval process.",
            default=False,
        )
        customparser.add_option(
            '-f',
            '--filename',
            dest='filename',
            help="Use this flag if you wish to use a different"\
            " filename than the default one. The default filename is" \
            " %s." % __filename__,
            action="append",
            default=None,
        )
        customparser.add_option(
            '--selector',
            dest='selector',
            help="Optionally include this flag to select a type to run"\
             " the current command on. Use this flag when you wish to"\
             " select a type without entering another command, or if you"\
              " wish to work with a type that is different from the one"\
              " you currently have selected.",
            default=None,
        )
        customparser.add_option(
            '--filter',
            dest='filter',
            help="Optionally set a filter value for a filter attribute."\
            " This uses the provided filter for the currently selected"\
            " type. Note: Use this flag to narrow down your results. For"\
            " example, selecting a common type might return multiple"\
            " objects that are all of that type. If you want to modify"\
            " the properties of only one of those objects, use the filter"\
            " flag to narrow down results based on properties."\
            "\t\t\t\t\t Usage: --filter [ATTRIBUTE]=[VALUE]",
            default=None,
        )
        customparser.add_option(
            '--path',
            dest='path',
            help="Optionally set a starting point for data collection."\
            " If you do not specify a starting point, the default path"\
            " will be /redfish/v1/. Note: The path flag can only be specified"\
            " at the time of login, so if you are already logged into the"\
            " server, the path flag will not change the path. If you are"\
            " entering a command that isn't the login command, but include"\
            " your login information, you can still specify the path flag"\
            " there.  ",
            default=None,
        )
        customparser.add_option(
            '-j',
            '--json',
            dest='json',
            action="store_true",
            help="Optionally include this flag if you wish to change the"\
            " displayed output to JSON format. Preserving the JSON data"\
            " structure makes the information easier to parse.",
            default=False
        )
