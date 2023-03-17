###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/main/LICENSE.md
###

""" RawPut Command for rdmc """

import sys
import json

from optparse import OptionParser
from rdmc_base_classes import RdmcCommandBase, RdmcOptionParser
from rdmc_helper import ReturnCodes, InvalidCommandLineError, \
                    InvalidCommandLineErrorOPTS, UI, InvalidFileInputError, \
                    InvalidFileFormattingError

class RawPutCommand(RdmcCommandBase):
    """ Raw form of the put command """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='rawput',\
            usage='rawput [FILENAME] [OPTIONS]\n\n\tRun to send a post from ' \
                    'the data in the input file.\n\texample: rawput rawput.' \
                    'txt\n\n\tExample input file:\n\t{\n\t    "path": "/redfish/' \
                    'v1/(put path)",\n\t    "body":{\n\t      ' \
                    '  "PutProperty": "PutValue"\n\t    }\n\t}',
            summary='This is the raw form of the PUT command.',\
            aliases=['rawput'],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj
        self.lobobj = rdmcObj.commandsDict["LoginCommand"](rdmcObj)

    def run(self, line):
        """ Main raw put worker function

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
        results = None

        if options.sessionid:
            url = self.sessionvalidation(options)
        else:
            self.putvalidation(options)

        contentsholder = None

        if len(args) == 1:
            try:
                inputfile = open(args[0], 'r')
                contentsholder = json.loads(inputfile.read())
            except Exception as excp:
                raise InvalidFileInputError("%s" % excp)
        elif len(args) > 1:
            raise InvalidCommandLineError("Raw put only takes 1 argument.\n")
        else:
            raise InvalidCommandLineError("Missing raw put file input "\
                                                                "argument.\n")

        if options.headers:
            extraheaders = options.headers.split(',')

            for item in extraheaders:
                header = item.split(':')

                try:
                    headers[header[0]] = header[1]
                except:
                    raise InvalidCommandLineError("Invalid format for " \
                                                            "--headers option.")

        if "path" in contentsholder and "body" in contentsholder:
            returnresponse = False

            if options.response or options.getheaders:
                returnresponse = True

            results = self._rdmc.app.put_handler(contentsholder["path"], \
                      contentsholder["body"], verbose=self._rdmc.opts.verbose, \
                      sessionid=options.sessionid, url=url, headers=headers, \
                      response=returnresponse, silent=options.silent)
        else:
            raise InvalidFileFormattingError("Input file '%s' was not "\
                                             "formatted properly." % args[0])

        if results and returnresponse:
            if options.getheaders:
                sys.stdout.write(json.dumps(dict(\
                                 results._http_response.getheaders())) + "\n")
    
            if options.response:
                sys.stdout.write(results.text)

        #Return code
        return ReturnCodes.SUCCESS

    def putvalidation(self, options):
        """ Raw put validation function

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
        """ Raw put session validation function

        :param options: command line options
        :type options: list.
        """

        url = None
        if options.user or options.password or options.url:
            if options.url:
                url = options.url
        else:
            if self._rdmc.app.config.get_url():
                url = self._rdmc.app.config.get_url()
        if url and not "https://" in url:
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

