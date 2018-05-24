###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

# -*- coding: utf-8 -*-
""" Login Command for RDMC """

import sys
import getpass
import redfish.ris

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import ReturnCodes, InvalidCommandLineError, \
                            InvalidCommandLineErrorOPTS, PathUnavailableError

class LoginCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='login',\
            usage='login [URL] [OPTIONS] \n\n\tTo login' \
                    ' remotely run using url and credentials' \
                    '\n\texample: login <url/hostname> -u <username> -p' \
                    ' <password>\n\n\tTo login on a local server run' \
                    ' without arguments\n\texample: login',\
            summary='Connects to a server, establishes a secure session,'\
                    ' and discovers data.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self.url = None
        self.username = None
        self.password = None
        self._rdmc = rdmcObj
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def loginfunction(self, line, skipbuild=None):
        """ Main worker function for login class
        
        :param line: entered command line
        :type line: list.
        :param skipbuild: flag to determine if monolith should be build
        :type skipbuild: boolean.
        """
        try:
            (options, args) = self._parse_arglist(line)
        except:
            if ("-h" in line) or ("--help" in line):
                return ReturnCodes.SUCCESS
            else:
                raise InvalidCommandLineErrorOPTS("")

        self.loginvalidation(options, args)

        self._rdmc.app.login(username=self.username, \
                      password=self.password, base_url=self.url, \
                      verbose=self._rdmc.opts.verbose, \
                      path=options.path, skipbuild=skipbuild, \
                      includelogs=options.includelogs)

        # Warning for cache enabled, since we save session in plain text
        if self._rdmc.app.config.get_cache() and not skipbuild:
            sys.stdout.write("WARNING: Cache is activated. Session keys are" \
                                                    " stored in plaintext.\n")

        if self._rdmc.opts.debug:
            sys.stdout.write("WARNING: Logger is activated. Logging is" \
                                                    " stored in plaintext.\n")

        if options.selector:
            try:
                sel = None
                val = None

                if options.filter:
                    try:
                        (sel, val) = options.filter.split('=')
                        sel = sel.strip()
                        val = val.strip()

                        if val.lower() == "true" or val.lower() == "false":
                            val = val.lower() in ("yes", "true", "t", "1")
                    except:
                        raise InvalidCommandLineError("Invalid filter" \
                        " parameter format. [filter_attribute]=[filter_value]")

                self._rdmc.app.select(query=options.selector, sel=sel, val=val)

                if self._rdmc.opts.verbose:
                    sys.stdout.write("Selected option: '%s'" % options.selector)
                    sys.stdout.write('\n')
            except Exception as excp:
                raise redfish.ris.InstanceNotFoundError(excp)

    def loginvalidation(self, options, args):
        """ Login helper function for login validations
        
        :param options: command line options
        :type options: list.
        :param args: command line arguments
        :type args: list.
        """
        # Fill user name/password from config file
        if not options.user:
            options.user = self._rdmc.app.config.get_username()
        if not options.password:
            options.password = self._rdmc.app.config.get_password()

        # Password and user name validation
        if options.user and not options.password:
            # Option for interactive entry of password
            tempinput = getpass.getpass()

            if tempinput:
                options.password = tempinput
            else:
                raise InvalidCommandLineError("Empty or invalid password" \
                                                                " was entered.")

        if options.user:
            self.username = options.user

        if options.password:
            self.password = options.password


        if len(args) > 0:
            # Any argument should be treated as an URL
            self.url = args[0]

            # Verify that URL is properly formatted for https://
            if not "https://" in self.url:
                self.url = "https://" + self.url
        else:
            # Check to see if there is a URL in config file
            if self._rdmc.app.config.get_url():
                self.url = self._rdmc.app.config.get_url()

        if not self.url:
            raise InvalidCommandLineError('No URL entered for login.')

    def run(self, line):
        """ wrapper function for main login function
        
        :param line: command line input
        :type line: string.
        """

        self.loginfunction(line)
        if ("-h" in line) or ("--help" in line):
            return ReturnCodes.SUCCESS
        if not self._rdmc.app.current_client.monolith._visited_urls:
            self.logoutobj.run("")
            raise PathUnavailableError("The path specified by the --path"\
                            " flag is unavailable.")

        #Return code
        return ReturnCodes.SUCCESS

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
            '--includelogs',
            dest='includelogs',
            action="store_true",
            help="Optionally include logs in the data retrieval process.",
            default=False,
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

