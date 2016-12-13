# -*- coding: utf-8 -*-
"""This is the main module for Redfish Utility handles all the CLI and UI interfaces"""

#---------Imports---------

import os
import sys
import errno
import shlex
import ctypes
import logging
import traceback
import importlib
import collections

import readline
import versioning
import redfish.ris
import redfish.rest.v1

import cliutils
import extensions

from rdmc_helper import ReturnCodes, ConfigurationFileError, \
                    CommandNotEnabledError, InvalidCommandLineError, \
                    InvalidCommandLineErrorOPTS, InvalidFileFormattingError, \
                    NoChangesFoundOrMadeError, InvalidFileInputError, UI, \
                    LOGGER, LERR, NoContentsFoundForOperationError, \
                    InfoMissingEntriesError, MultipleServerConfigError, \
                    InvalidOrNothingChangedSettingsError, \
                    NoDifferencesFoundError, InvalidMSCfileInputError, \
                    NoCurrentSessionEstablished, FailureDuringCommitError

from rdmc_base_classes import RdmcCommandBase, RdmcOptionParser, HARDCODEDLIST

if os.name != 'nt':
    import setproctitle

#import all extensions dynamically
for name in extensions.classNames:
    pkgName, cName = name.rsplit('.', 1)
    pkgName = 'extensions' + pkgName

    try:
        extensions._Commands[cName] = getattr(\
                                        importlib.import_module(pkgName), cName)
    except Exception, excp:
        sys.stderr.write("Error locating extension %s at location %s\n" % \
                                                (cName, 'extensions' + name))
        raise excp

#---------End of imports---------

# always flush stdout and stderr
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)

CLI = cliutils.CLI()

class RdmcCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, Args=None):
        RdmcCommandBase.__init__(self, \
            name=versioning.__shortname__, \
            usage=versioning.__shortname__ +' [command]', \
            summary='Redfish Utility', \
            aliases=[versioning.__shortname__], \
            optparser=RdmcOptionParser())
        Args.append('--showwarnings')
        self._commands = collections.OrderedDict()
        self.commandsDict = extensions._Commands
        self.interactive = False
        self._progname = '%s : %s' % (versioning.__shortname__, \
                                      versioning.__longname__)
        self.opts = None
        self.config_file = None
        self.app = redfish.ris.RmcApp(Args=Args)
        self.retcode = 0
        self.candidates = dict()
        self.commlist = list()
        self._redobj = None
        Args.remove('--showwarnings')

    def add_command(self, newcmd, section=None):
        """ Handles to addition of new commands

        :param newcmd: command to be added
        :type newcmd: str.
        :param section: section for the new command
        :type section: str.
        """
        if section not in self._commands:
            self._commands[section] = list()

        self._commands[section].append(newcmd)

    def get_commands(self):
        """ Retrieves list of commands added """
        return self._commands

    def search_commands(self, cmdname):
        """ Function to see if command exist in added commands

        :param cmdname: command to be searched
        :type cmdname: str.
        """
        for vals in self._commands.values():
            for cmd in vals:
                if cmd.ismatch(cmdname):
                    if not cmd.is_enabled():
                        raise CommandNotEnabledError(cmd.enablement_hint())

                    return cmd

        raise cliutils.CommandNotFoundException(cmdname)

    def _run_command(self, opts, args):
        """ Calls the commands run function

        :param opts: command options
        :type opts: options.
        :param args: list of the entered arguments
        :type args: list.
        """
        cmd = self.search_commands(args[0])

        if opts.debug:
            LOGGER.setLevel(logging.DEBUG)
            LERR.setLevel(logging.DEBUG)

        if not (opts.nologo or cmd.nologo) and not self.interactive:
            CLI.version(self._progname, versioning.__version__,\
                                versioning.__extracontent__, fileh=sys.stdout)

        if len(args) > 1:
            return cmd.run(args[1:])
        else:
            return cmd.run([])

    def run(self, line):
        """ Main rdmc command worker function

        :param line: entered command line
        :type line: list.
        """
        if os.name == 'nt':
            if not ctypes.windll.shell32.IsUserAnAdmin() != 0:
                UI().user_not_admin()
                raw_input("Press enter to exit")
                sys.exit(ReturnCodes.USER_NOT_ADMIN)
        elif not os.getuid() == 0:
            UI().user_not_admin()
            raw_input("Press enter to exit")
            sys.exit(ReturnCodes.USER_NOT_ADMIN)

        nargv = []
        curr = []
        argfound = False

        if "--version" in line:
            sys.stdout.write("""%(progname)s %(version)s\n""" % \
                     {'progname': versioning.__longname__, 'version': \
                                                        versioning.__version__})

            sys.stdout.flush()
            sys.exit(self.retcode)
        else:
            for argument in enumerate(line):
                if not argfound and not argument[1].startswith('-'):
                    nargv = line[argument[0]:]
                    break
                else:
                    argfound = False

                if argument[1] == "-c":
                    argfound = True

                curr.append(argument[1])

        (self.opts, _) = self.parser.parse_args(curr)

        if self.opts.config is not None and len(self.opts.config) > 0:
            if not os.path.isfile(self.opts.config):
                self.retcode = ReturnCodes.CONFIGURATION_FILE_ERROR
                sys.exit(self.retcode)

            self.app.config_file = self.opts.config

        self.app.config_from_file(self.app.config_file)
        logdir = self.app.config.get_logdir()

        if logdir:
            try:
                os.makedirs(logdir)
            except OSError, ex:
                if ex.errno == errno.EEXIST:
                    pass
                else:
                    raise

        logfile = os.path.join(logdir, versioning.__shortname__+'.log')

        # Create a file logger since we got a logdir
        lfile = logging.FileHandler(filename=logfile)
        formatter = logging.Formatter("%(asctime)s %(levelname)s\t: " \
                                                                "%(message)s")

        lfile.setFormatter(formatter)
        lfile.setLevel(logging.DEBUG)
        LOGGER.addHandler(lfile)
        self.app.LOGGER = LOGGER

        if self.opts.nocache:
            self.app.config.set_cache(False)

        self.app.config.set_cachedir(os.path.join(self.opts.config_dir, \
                                                                    'cache'))
        cachedir = self.app.config.get_cachedir()

        if cachedir:
            try:
                os.makedirs(cachedir)
            except OSError, ex:
                if ex.errno == errno.EEXIST:
                    pass
                else:
                    raise

        if ("login" in line and not "help" in line) or not line:
            self.app.logout()
        else:
            self.app.restore()

        if len(nargv) > 0:
            try:
                self.retcode = self._run_command(self.opts, nargv)
                if self.app.config.get_cache():
                    if ("logout" not in line) and ("--logout" not in line):
                        self.app.save()
            except Exception, excp:
                self.handle_exceptions(excp)

            return self.retcode
        else:
            self.cmdloop(self.opts)

            if self.app.config.get_cache():
                self.app.save()

    def cmdloop(self, opts):
        """ Interactive mode worker function

        :param opts: command options
        :type opts: options.
        """
        self.interactive = True

        if not opts.nologo:
            CLI.version(self._progname, versioning.__version__,\
                                versioning.__extracontent__, fileh=sys.stdout)

        if opts.debug:
            LOGGER.setLevel(logging.DEBUG)
            LERR.setLevel(logging.DEBUG)

        #**********Handler for GUI tab tab ***************
        for section in self._commands:
            if section.startswith('_'):
                continue

            for command in self._commands[section]:
                self.commlist.append(command.name)

        for item in self.commlist:
            if item == "help":
                self.candidates[item] = self.commlist
            else:
                self.candidates[item] = []

        self._redobj = TabAndHistoryCompletionClass(dict(self.candidates))
        readline.set_completer(self._redobj.main_completer_handler)
        readline.parse_and_bind("tab: complete")
        #***************************************************

        while True:
            line = raw_input(versioning.__shortname__+' > ')
            readline.add_history(line)

            if not len(line):
                continue
            elif line.endswith(os.linesep):
                line.rstrip(os.linesep)

            nargv = shlex.split(line, posix=False)

            try:
                if "login " in line or line == 'login':
                    self.app.logout()

                self.retcode = self._run_command(opts, nargv)
                self.check_for_tab_lists(nargv)
            except Exception, excp:
                self.handle_exceptions(excp)

            if self.opts.verbose:
                sys.stdout.write(u"REDFISH return code: %s\n" % self.retcode)

        return self.retcode

    def handle_exceptions(self, excp):
        """ Main exception handler for both shell and interactive modes

        :param excp: captured exception to be handled
        :type excp: exception.
        """
        try:
            raise
        # ****** RDMC ERRORS ******
        except ConfigurationFileError, excp:
            self.retcode = ReturnCodes.CONFIGURATION_FILE_ERROR
            UI().error(excp)
            sys.exit(excp.errcode)
        except CommandNotEnabledError, excp:
            self.retcode = ReturnCodes.COMMAND_NOT_ENABLED_ERROR
            UI().command_not_enabled(excp)
            extensions._Commands['HelpCommand'](rdmc=self).run("")
        except InvalidCommandLineError, excp:
            self.retcode = ReturnCodes.INVALID_COMMAND_LINE_ERROR
            UI().invalid_commmand_line(excp)
        except NoCurrentSessionEstablished, excp:
            self.retcode = ReturnCodes.NO_CURRENT_SESSION_ESTABLISHED
            UI().error(excp)
        except NoChangesFoundOrMadeError, excp:
            self.retcode = ReturnCodes.NO_CHANGES_MADE_OR_FOUND
            UI().invalid_commmand_line(excp)
        except InvalidFileInputError, excp:
            self.retcode = ReturnCodes.INVALID_FILE_INPUT_ERROR
            UI().invalid_commmand_line(excp)
        except InvalidCommandLineErrorOPTS, excp:
            self.retcode = ReturnCodes.INVALID_COMMAND_LINE_ERROR
        except InvalidFileFormattingError, excp:
            self.retcode = ReturnCodes.INVALID_FILE_FORMATTING_ERROR
            UI().invalid_file_formatting(excp)
        except NoContentsFoundForOperationError, excp:
            self.retcode = ReturnCodes.NO_CONTENTS_FOUND_FOR_OPERATION
            UI().no_contents_found_for_operation(excp)
        except InfoMissingEntriesError, excp:
            self.retcode = ReturnCodes.NO_VALID_INFO_ERROR
            UI().error(excp)
        except InvalidOrNothingChangedSettingsError, excp:
            self.retcode = ReturnCodes.SAME_SETTINGS_ERROR
            UI().error(excp)
        except NoDifferencesFoundError, excp:
            self.retcode = ReturnCodes.NO_CHANGES_MADE_OR_FOUND
            UI().no_differences_found(excp)
        except MultipleServerConfigError, excp:
            self.retcode = ReturnCodes.MULTIPLE_SERVER_CONFIG_FAIL
            UI().multiple_server_config_fail(excp)
        except InvalidMSCfileInputError, excp:
            self.retcode = ReturnCodes.MULTIPLE_SERVER_INPUT_FILE_ERROR
            UI().multiple_server_config_input_file(excp)
        except FailureDuringCommitError, excp:
            self.retcode = ReturnCodes.FAILURE_DURING_COMMIT_OPERATION
            UI().error(excp)
        # ****** CLI ERRORS ******
        except cliutils.CommandNotFoundException, excp:
            self.retcode = ReturnCodes.UI_CLI_COMMAND_NOT_FOUND_EXCEPTION
            UI().command_not_found(excp)
            extensions._Commands['HelpCommand'](rdmc=self).run("")
        # ****** RMC/RIS ERRORS ******
        except redfish.ris.UndefinedClientError:
            self.retcode = ReturnCodes.RIS_UNDEFINED_CLIENT_ERROR
            UI().error(u"Please login before making a selection")
        except redfish.ris.InstanceNotFoundError, excp:
            self.retcode = ReturnCodes.RIS_INSTANCE_NOT_FOUND_ERROR
            UI().printmsg(excp)
        except redfish.ris.CurrentlyLoggedInError, excp:
            self.retcode = ReturnCodes.RIS_CURRENTLY_LOGGED_IN_ERROR
            UI().error(excp)
        except redfish.ris.NothingSelectedError, excp:
            self.retcode = ReturnCodes.RIS_NOTHING_SELECTED_ERROR
            UI().nothing_selected()
        except redfish.ris.NothingSelectedSetError, excp:
            self.retcode = ReturnCodes.RIS_NOTHING_SELECTED_SET_ERROR
            UI().nothing_selected_set()
        except redfish.ris.InvalidSelectionError, excp:
            self.retcode = ReturnCodes.RIS_INVALID_SELECTION_ERROR
            UI().error(excp)
        except redfish.ris.rmc_helper.SessionExpired, excp:
            self.retcode = ReturnCodes.RIS_SESSION_EXPIRED
            self.app.logout()
            UI().printmsg(u"Current session has expired or is invalid, "\
                    "please login again with proper credentials to continue.\n")
        # ****** RMC/RIS ERRORS ******
        except redfish.rest.v1.RetriesExhaustedError, excp:
            self.retcode = ReturnCodes.V1_RETRIES_EXHAUSTED_ERROR
            UI().retries_exhausted_attemps()
        except redfish.rest.v1.InvalidCredentialsError, excp:
            self.retcode = ReturnCodes.V1_INVALID_CREDENTIALS_ERROR
            UI().invalid_credentials(excp)
        except redfish.rest.v1.ServerDownOrUnreachableError, excp:
            self.retcode = \
                    ReturnCodes.V1_SERVER_DOWN_OR_UNREACHABLE_ERROR
            UI().error(excp)
        except redfish.ris.rmc_helper.InvalidPathError, excp:
            self.retcode = ReturnCodes.RIS_REF_PATH_NOT_FOUND_ERROR
            UI().printmsg(u"Reference path not found.")
        # ****** GENERAL ERRORS ******
        except SystemExit:
            self.retcode = ReturnCodes.GENERAL_ERROR
            raise
        except Exception, excp:
            self.retcode = ReturnCodes.GENERAL_ERROR
            sys.stderr.write(u'ERROR: %s\n' % excp)

            if self.opts.debug:
                traceback.print_exc(file=sys.stderr)

    def check_for_tab_lists(self, command=None):
        """ Function to generate available options for tab tab

        :param command: command for auto tab completion
        :type command: string.
        """
        changes = dict()

        # select options
        typeslist = list()

        try:
            typeslist = list(set(self.app.types()))
            typeslist.sort()
            changes["select"] = typeslist
        except:
            pass

        # get/set options
        getlist = list()
        try:
            templist = self.app.get_save()

            for content in templist:        
                for k in content.keys():        
                    if k.lower() in HARDCODEDLIST or '@odata' in k.lower():
                        del content[k]

            for key, _ in templist[0].iteritems():
                getlist.append(key)

            getlist.sort()

            changes["get"] = getlist
            changes["set"] = getlist

        except:
            pass

        if len(changes):
            self._redobj.updates_tab_completion_lists(changes)

class TabAndHistoryCompletionClass(object):
    """ Tab and History Class used by interactive mode """
    def __init__(self, options):
        self.options = options
        self.current_candidates = []
        self.possible_vals = []
        self.val_pos = 0
        return

    def main_completer_handler(self, text, state):
        """ Handler of all input entries, tabs, and history

        :param text: input text
        :type text: string.
        :param state: current state
        :type state: string.
        """
        response = None

        # Build match list on first iteration else continue
        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            if not words:
                # option for words list
                self.current_candidates = sorted(self.options.keys())
            else:
                # traverse all words entries and passing accordingly
                try:
                    if begin == 0:
                        # first word
                        candidates = self.options.keys()
                    else:
                        # later word
                        first = words[0]
                        candidates = self.options[first]
                    if being_completed:
                        # match options with portion of input being completed
                        self.current_candidates = [w for w in candidates\
                           if w.lower().startswith(being_completed.lower())]
                    else:
                        # matching empty string so use all candidates
                        self.current_candidates = candidates

                except (KeyError, IndexError):
                    self.current_candidates = []

        # Return the state from the match list if found otherwise return None.
        try:
            response = self.current_candidates[state]
        except IndexError:
            # No candidate found for state
            response = None

        # Response return
        return response

    def updates_tab_completion_lists(self, options):
        """ Function to update tab completion lists

        :param options: options list
        :type options: list.
        """
        # Loop through options passed and add them to them
        # to the current tab options list
        for key, value in options.iteritems():
            self.options[key] = value


if __name__ == '__main__':
    # Initialization of main command class
    ARGUMENTS = sys.argv[1:]

    RDMC = RdmcCommand(Args=ARGUMENTS)

    # Addition of rdmc commands and sub commands
    for cName in extensions.classNames:
        sName = cName.split('.')[1]
        cName = cName.split('.')[-1]
        
        if not cName.endswith("Command"):
            continue
        
        if cName == 'HelpCommand':
            RDMC.add_command(extensions._Commands[cName](rdmc=RDMC), \
                                                                section=sName)
        else:
            try:
                RDMC.add_command(extensions._Commands[cName](RDMC), \
                                                                section=sName)
            except Exception, excp:
                sys.stderr.write("Error loading extension: %s\n" % cName)
                sys.stderr.write("\t" + excp.message + '\n')

    # Main execution function call wrapper
    if os.name != 'nt':
        FOUND = False
        VARIABLE = setproctitle.getproctitle()

        for items in VARIABLE.split(" "):
            if FOUND:
                VARIABLE = VARIABLE.replace(items, "xxxxxxxx")
                break

            if items == "--password" or items == "-p":
                FOUND = True

        setproctitle.setproctitle(VARIABLE)

    RDMC.retcode = RDMC.run(ARGUMENTS)

    if RDMC.opts.verbose:
        sys.stdout.write(u"return code: %s\n" % RDMC.retcode)

    # Return code
    sys.exit(RDMC.retcode)
