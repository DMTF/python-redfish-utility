###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/main/LICENSE.md
###

""" Get Command for RDMC """

import redfish.ris

from optparse import OptionParser
from collections import (OrderedDict)
from rdmc_helper import ReturnCodes, \
                    InvalidCommandLineErrorOPTS, UI, \
                    NoContentsFoundForOperationError

from rdmc_base_classes import RdmcCommandBase, HARDCODEDLIST

class GetCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='get',\
            usage='get [PROPERTY] [OPTIONS]\n\n\tTo retrieve all' \
                    ' the properties run without arguments\n\texample: get' \
                    '\n\n\tTo retrieve multiple properties use the following' \
                    ' example\n\texample: get <property> <property> ' \
                    '<property>\n\n\tTo change output style format provide'\
                    ' the json flag\n\texample: get --json',\
            summary='Displays the current value(s) of a' \
                    ' property(ies) within a selected type.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self._rdmc = rdmcObj
        self.lobobj = rdmcObj.commandsDict["LoginCommand"](rdmcObj)
        self.selobj = rdmcObj.commandsDict["SelectCommand"](rdmcObj)
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def run(self, line):
        """ Main get worker function

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

        self.getvalidation(options)
        multiargs = False
        content = []

        if args:
            for arg in args:
                newargs = list()
                if "/" in arg:
                    newargs = arg.split("/")
                    arg = newargs[0]
                if len(args) > 1 and options.json:
                    multiargs = True
                    item = self.getworkerfunction(arg, options, line,\
                                newargs=newargs, results=True, multivals=True)
                    if item:
                        content.append(item)
                    else:
                        if not newargs:
                            raise NoContentsFoundForOperationError('No ' \
                                           'contents found for entry: %s' % arg)
                        else:
                            raise NoContentsFoundForOperationError('No ' \
                                       'contents found for entry: %s' % line[0])
                else:
                    if not self.getworkerfunction(arg, options, line,\
                                                                newargs=newargs):
                        if not newargs:
                            raise NoContentsFoundForOperationError('No ' \
                                           'contents found for entry: %s' % arg)
                        else:
                            raise NoContentsFoundForOperationError('No ' \
                                       'contents found for entry: %s' % line[0])
        else:
            if not self.getworkerfunction(args, options, line):
                raise NoContentsFoundForOperationError('No contents found')

        if multiargs and options.json:
            self.jsonprinthelper(content)

        if options.logout:
            self.logoutobj.logoutfunction("")

        #Return code
        return ReturnCodes.SUCCESS

    def getworkerfunction(self, args, options, line, newargs=None, \
                                results=None, uselist=False, multivals=False):
        """ main get worker function
        
        :param args: command line arguments
        :type args: list.
        :param options: command line options
        :type options: list.
        :param line: command line input
        :type line: string.
        :param newargs: new style arguments
        :type newargs: list.
        :param results: current results collected
        :type results: string.
        :param uselist: use reserved properties list to filter results
        :type uselist: bool
        :param multivals: multiple values 
        :type multivals: boolean.
        """
        listitem = False
        somethingfound = False
        contents = self._rdmc.app.get_save(args)
        values = {}
        itemnum = 0
        if not contents:
            raise NoContentsFoundForOperationError('No contents '\
                                                'found for entries: %s' % line)

        for content in contents:
            content = OrderedDict(sorted(list(content.items()), key=lambda x: x[0]))

            if not uselist:
                for k in list(content.keys()):
                    if k.lower() in HARDCODEDLIST or '@odata' in k.lower():
                        del content[k]

            if len(content):
                itemnum +=1
                if not newargs:
                    somethingfound = True
                else:
                    innerresults = OrderedDict()
                    newlist = list()

                    for item in newargs:
                        if isinstance(content, list):
                            if len(content) > 1:
                                argleft = [x for x in newargs if x not in \
                                                                        newlist]

                                [self.getworkerhelper(results, content[x], \
                                    newlist[:], argleft, jsono=options.json) \
                                                for x in range(len(content))]
                                listitem = True
                                break
                            else:
                                content = content[0]
                        for key in list(content.keys()):
                            if item.lower() == key.lower():
                                newlist.append(key)
                                content = content.get(key)
                                somethingfound = True
                                break
                            else:
                                somethingfound = False

                        if not somethingfound:
                            return somethingfound

                    counter = 0
                    for item in reversed(newlist):
                        if counter == 0:
                            innerresults = {item:content}
                            counter += 1
                        else:
                            innerresults = {item:innerresults}
                    content = innerresults
            else:
                continue

            if somethingfound and results:
                if multivals:
                    values[itemnum] = content
                else:
                    return content
            elif somethingfound and not listitem:
                if options.json:
                    UI().print_out_json(content)
                else:
                    UI().print_out_human_readable(content)
        if multivals:
            return values
        else:
            return somethingfound

    def getworkerhelper(self, results, content, newlist, newargs, jsono=False):
        """ helper function for list items
        
        :param results: current results collected
        :type results: string.
        :param content: current content to work on
        :type content: string.
        :param newlist: new style list
        :type newlist: list.
        :param newargs: new style arguments
        :type newargs: list.
        :param jsono: boolean to determine output style
        :type jsono: boolean.
        """
        innerresults = OrderedDict()
        listitem = False
        for item in newargs:
            if isinstance(content, list):
                if not content:
                    return
                if len(content) > 1:
                    argleft = [x for x in newargs if x not in newlist]
                    [self.getworkerhelper(results, content[x], newlist[:],\
                                argleft, jsono) for x in range(len(content))]
                    listitem = True
                    break
                else:
                    content = content[0]
            for key in list(content.keys()):
                if item.lower() == key.lower():
                    newlist.append(key)
                    content = content.get(key)
                    somethingfound = True
                    break
                else:
                    somethingfound = False

            if not somethingfound:
                return somethingfound

        counter = 0
        for item in reversed(newlist):
            if counter == 0:
                innerresults = {item:content}
                counter += 1
            else:
                innerresults = {item:innerresults}
                content = innerresults

        if somethingfound and results:
            return content
        elif somethingfound and not listitem:
            if jsono:
                UI().print_out_json(content)
            else:
                UI().print_out_human_readable(content)

    def jsonprinthelper(self, content):
        """ Helper for JSON UI print out

        :param content: current content to work on
        :type content: string.
        """
        final = dict()

        for item in content:
            for num, _ in item.items():
                try:
                    final[num].update(item[num])
                except:
                    final[num] = item[num]
        for num in final:
            UI().print_out_json(final[num])

    def getvalidation(self, options):
        """ get method validation function
        
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
        customparser.add_option(
            '--logout',
            dest='logout',
            action="store_true",
            help="Optionally include the logout flag to log out of the"\
            " server after this command is completed. Using this flag when"\
            " not logged in will have no effect",
            default=None,
        )
