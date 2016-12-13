""" RawDelete Command for RDMC """

import sys
import json

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase, RdmcOptionParser
from rdmc_helper import ReturnCodes, InvalidCommandLineError, \
                    InvalidCommandLineErrorOPTS, UI

class RawDeleteCommand(RdmcCommandBase):
    """ Raw form of the delete command """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='rawdelete',\
            usage='rawdelete [PATH] [OPTIONS]\n\n\tRun to to delete data from' \
                    ' the passed in path.\n\texample: rawdelete "/redfish/v1/' \
                    'Sessions/(session ID)"',
            summary='This is the raw form of the DELETE command.',\
            aliases=['rawdelete'],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj
        self.lobobj = rdmcObj.commandsDict["LoginCommand"](rdmcObj)

    def run(self, line):
        """ Main raw delete worker function

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

        url = None
        headers = {}

        if options.sessionid:
            url = self.sessionvalidation(options)
        else:
            self.deletevalidation(options)

        if len(args) > 1:
            raise InvalidCommandLineError("Raw delete only takes 1 argument.\n")
        elif len(args) == 0:
            raise InvalidCommandLineError("Missing raw delete input path.\n")

        if args[0].startswith('"') and args[0].endswith('"'):
            args[0] = args[0][1:-1]

        if options.expand:
            args[0] = args[0] + '?$expand=.'

        try:
            currentsess = self._rdmc.app.current_client._rest_client.\
                                            _RestClientBase__session_location
        except:
            currentsess=None

        if options.headers:
            extraheaders = options.headers.split(',')

            for item in extraheaders:
                header = item.split(':')

                try:
                    headers[header[0]] = header[1]
                except:
                    InvalidCommandLineError("Invalid format for --headers " \
                                                                    "option.")

        if currentsess and (args[0] in currentsess):
            self._rdmc.app.logout()
            sys.stdout.write("Your session has been deleted.\nPlease log "\
                                        "back in if you wish to continue.\n")
        else:
            returnresponse = False

            if options.response or options.getheaders:
                returnresponse = True

            results = self._rdmc.app.delete_handler(args[0], \
                verbose=self._rdmc.opts.verbose, sessionid=options.sessionid, \
                url=url, headers=headers, silent=options.silent)

        if returnresponse and results:
            if options.getheaders:
                sys.stdout.write(json.dumps(dict(\
                                 results._http_response.getheaders())) + "\n")

            if options.response:
                sys.stdout.write(results.text)
        elif results.status == 404:
            return ReturnCodes.NO_CONTENTS_FOUND_FOR_OPERATION
        elif results.status != 200:
            return ReturnCodes.UI_CLI_USAGE_EXCEPTION

        #Return code
        return ReturnCodes.SUCCESS

    def deletevalidation(self, options):
        """ Raw delete validation function

        :param options: command line options
        :type options: list.
        """
        inputline = list()

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

            self.lobobj.loginfunction(inputline, skipbuild=True)

    def sessionvalidation(self, options):
        """ Raw delete session validation function
        
        :param options: command line options
        :type options: list.
        """

        if options.user or options.password or options.url:
            if options.url:
                url = options.url
        else:
            if self._rdmc.app.config.get_url():
                url = self._rdmc.app.config.get_url()
        if not "https://" in url:
            url = "https://" + url

        return url

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
            '--response',
            dest='response',
            action="store_true",
            help="Use this flag to return the response body.",
            default=False
        )
        customparser.add_option(
            '--getheaders',
            dest='getheaders',
            action="store_true",
            help="Use this flag to return the response headers.",
            default=False
        )
        customparser.add_option(
            '--headers',
            dest='headers',
            help="Use this flag to add extra headers to the request."\
            "\t\t\t\t\t Usage: --headers=HEADER:VALUE,HEADER:VALUE",
            default=None,
        )
        customparser.add_option(
            '--silent',
            dest='silent',
            action="store_true",
            help="""Use this flag to silence responses""",
            default=False,
        )
        customparser.add_option(
            '--sessionid',
            dest='sessionid',
            help="Optionally include this flag if you would prefer to "\
            "connect using a session id instead of a normal login.",
            default=None
        )
        customparser.add_option(
            '--expand',
            dest='expand',
            action="store_true",
            help="""Use this flag to expand the path specified using the """\
                                            """expand notation '?$expand=.'""",
            default=False,
        )

