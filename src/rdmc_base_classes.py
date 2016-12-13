###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

# -*- coding: utf-8 -*-
"""This is the helper module for RDMC"""

#---------Imports---------

import os
import glob
import shlex

import versioning
from optparse import OptionParser, OptionGroup

import cliutils

#---------End of imports---------

#Using hard coded list until better solution is found
HARDCODEDLIST = ["name", "description", "status", "links", "members", "id",
                 "relateditem", "actions", "oem"]

class CommandBase(object):
    """Abstract base class for all Command objects.

    This class is used to build complex command line programs
    """
    def __init__(self, name, usage, summary, aliases=None, optparser=None):
        self.name = name
        self.summary = summary
        self.aliases = aliases
        self.config_required = True # does the command access config data

        if optparser is None:
            self.parser = cliutils.CustomOptionParser()
        else:
            self.parser = optparser

        self.parser.usage = usage
        self._cli = cliutils.CLI()

    def run(self, line, rmdcopts):
        """Called to actually perform the work.

        Override this method in your derived class.  This is where your program
        actually does work.
        """
        pass

    def ismatch(self, cmdname):
        """Compare cmdname against possible aliases.

        Commands can have aliases for syntactic sugar.  This method searches
        aliases for a match.

        :param cmdname: name or alias to search for
        :type cmdname: str.
        :returns: boolean -- True if it matches, otherwise False
        """
        if cmdname is None or len(cmdname) == 0:
            return False

        cmdname_lower = cmdname.lower()
        if self.name.lower() == cmdname_lower:
            return True

        if self.aliases:
            for alias in self.aliases:
                if alias.lower() == cmdname_lower:
                    return True

        return False

    def print_help(self):
        """Automated help printer.
        """
        self.parser.print_help()

    def print_summary(self):
        """Automated summary printer.
        """
        maxsum = 45
        smry = self.summary

        if not smry:
            smry = ''

        sumwords = smry.split(' ')
        lines = []
        line = []
        linelength = 0

        for sword in sumwords:
            if linelength + len(sword) > maxsum:
                lines.append(' '.join(line))
                line = []
                linelength = 0

            line.append(sword)
            linelength += len(sword) + 1

        lines.append(' '.join(line))

        sep = '\n' + (' ' * 34)
        print "  %-28s - %s" % (self.name, sep.join(lines))

    def _parse_arglist(self, line=None):
        """parses line into an options and args taking
        special consideration of quote characters into account

        :param line: string of arguments passed in
        :type line: str.
        :returns: args list
        """
        if line is None:
            return self.parser.parse_args(line)

        arglist = []
        if isinstance(line, basestring):
            arglist = shlex.split(line, posix=False)
            for ind, val in enumerate(arglist):
                arglist[ind] = val.strip('"\'')
        elif isinstance(line, list):
            arglist = line

        exarglist = []
        if os.name == 'nt':
            # need to glob for windows
            for arg in arglist:
                gob = glob.glob(arg)

                if gob and len(gob) > 0:
                    exarglist.extend(gob)
                else:
                    exarglist.append(arg)

        else:
            for arg in arglist:
                exarglist.append(arg)

        return self.parser.parse_args(exarglist)

class RdmcCommandBase(CommandBase):
    """Base class for rdmc commands which includes some common helper
       methods.
    """

    def __init__(self, name, usage, summary, aliases, optparser=None):
        """ Constructor """
        CommandBase.__init__(self,\
            name=name,\
            usage=usage,\
            summary=summary,\
            aliases=aliases,\
            optparser=optparser)
        self.json = False
        self.cache = False
        self.nologo = False

    def is_enabled(self):
        """ If reachable return true for command """
        return True

    def enablement_hint(self):
        """
        Override to define a error message displayed to the user
        when command is not enabled.
        """
        return ""

class RdmcOptionParser(OptionParser):
    """ Constructor """
    def __init__(self):
        OptionParser.__init__(self,\
            usage="Usage: %s [GLOBAL OPTIONS] [COMMAND] [ARGUMENTS]"\
            " [COMMAND OPTIONS]" % versioning.__shortname__)

        globalgroup = OptionGroup(self, "GLOBAL OPTIONS")

        #to correct the capitalization on help text:
        self.option_list[0].help = 'Show this help message and exit.'

        self.add_option(
            '-c',
            '--config',
            dest='config',
            help="Use the provided configuration file instead of the default"\
            " one.",
            metavar='FILE'
        )

        config_dir_default = os.path.join(cliutils.get_user_config_dir(),\
                                            '.%s' % versioning.__shortname__)
        self.add_option(
            '--cache-dir',
            dest='config_dir',
            default=config_dir_default,
            help="Use the provided directory as the location to cache data"\
            " (default location: %s)" % config_dir_default,
            metavar='PATH'
        )

        globalgroup.add_option(
            '-v',
            '--verbose',
            dest='verbose',
            action="store_true",
            help="""Display verbose information.""",
            default=False
        )

        globalgroup.add_option(
            '-d',
            '--debug',
            dest='debug',
            action="store_true",
            help="""Display debug information.""",
            default=False
        )

        globalgroup.add_option(
            '--nocache',
            dest='nocache',
            action="store_true",
            help="During execution the application will temporarily store"\
            " data only in memory.",
            default=False
        )

        globalgroup.add_option(
            '--nologo',
            dest='nologo',
            action="store_true",
            help="""Include to block logo.""",
            default=False
        )

        self.add_option_group(globalgroup)
