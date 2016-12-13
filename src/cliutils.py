# -*- coding: utf-8 -*-
"""Base implementation for cli interaction with Redfish interface"""

#---------Imports---------

import os
import re
import sys
import getpass
import optparse
import subprocess

if os.name == 'nt':
    import ctypes
    from ctypes import wintypes, windll

#---------End of imports---------

class CommandNotFoundException(Exception):
    """Exception throw when Command is not found"""
    pass

def get_user_config_dir():
    """Platform specific directory for user configuration.

    :returns: returns the user configuration directory.
    :rtype: string
    """
    if os.name == 'nt':
        try:
            csidl_appdata = 26

            shgetfolderpath = windll.shell32.SHGetFolderPathW
            shgetfolderpath.argtypes = [wintypes.HWND, ctypes.c_int, \
                             wintypes.HANDLE, wintypes.DWORD, wintypes.LPCWSTR]


            path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
            result = shgetfolderpath(0, csidl_appdata, 0, 0, path_buf)

            if result == 0:
                return path_buf.value
        except ImportError:
            pass

        return os.environ['APPDATA']
    else:
        return os.path.expanduser('~')

def is_exe(filename):
    """Determine if filename is an executable.

    :param filename: the filename to examine.
    :type filename: string
    :returns: True if filename is executable False otherwise.
    :rtype: boolean
    """
    if sys.platform == 'win32':
        if os.path.exists(filename):
            return True

        # windows uses PATHEXT to list valid executable extensions
        pathext = os.environ['PATHEXT'].split(os.pathsep)
        (_, ext) = os.path.splitext(filename)

        if ext in pathext:
            return True
    else:
        if os.path.exists(filename) and os.access(filename, os.X_OK):
            return True

    return False

def find_exe(filename, path=None):
    """Search path for a executable (aka which)

    :param filename: the filename to search for.
    :type filename: string.
    :param path: the path(s) to search (default: os.environ['PATH'])
    :param path: string separated with os.pathsep
    :returns: string with full path to the file or None if not found.
    :rtype: string or None.
    """
    if path is None:
        path = os.environ['PATH']

    pathlist = path.split(os.pathsep)

    # handle fully qualified paths
    if os.path.isfile(filename) and is_exe(filename):
        return filename

    for innerpath in pathlist:
        foundpath = os.path.join(innerpath, filename)

        if is_exe(foundpath):
            return foundpath

    return None

def get_terminal_size():
    """Returns the rows and columns of the terminal as a tuple.

    :returns: the row and column count of the terminal
    :rtype: tuple (cols, rows)
    """
    _tuple = (80, 25) # default

    if os.name == 'nt':
        pass
    else:
        which_stty = find_exe('stty')

        if which_stty:
            args = [which_stty, 'size']
            procs = subprocess.Popen(args, shell=False, \
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout_s, _) = procs.communicate()

            #retcode = p.wait()
            if stdout_s and re.search(r'^\d+ \d+$', stdout_s):
                rows, cols = stdout_s.split()
                _tuple = (cols, rows)

    return _tuple

class CLI(object):
    """Class for building command line interfaces."""
    def __init__(self, out=sys.stdout):
        self._out = out
        cols, rows = get_terminal_size()
        self._cols = int(cols)
        self._rows = int(rows)

    def get_hrstr(self, character='-'):
        """returns a string suitable for use as a horizontal rule.

        :param character: the character to use as the rule. (default -)
        :type character: str.
        """
        return '%s\n' % (character * self._cols)

    def hr(self, fileh=None, character='-'):
        """writes a horizontal rule to the file handle.

        :param fileh: file handle to write to. defaults to sys.stdout.
        :type fileh: file like object.
        :param character: the character to use as the rule. (default -)
        :type character: str.
        """
        outfh = fileh

        if not outfh:
            outfh = sys.stdout

        outfh.write(self.get_hrstr(character=character))
        outfh.flush()

    def version(self, progname, version, extracontent, fileh=sys.stdout):
        """Prints a version string to fileh.

        :param progname: the name of the program.
        :type progname: str.
        :param version: the version of the program.
        :type version str.
        :param fileh: the file handle to write to. Default is sys.stdout.
        :type fileh: file object
        :returns: None
        """
        fileh.write("%(progname)s version %(version)s\n%(extracontent)s" \
                                % {'progname': progname, 'version': version, \
                                                'extracontent': extracontent})

        fileh.flush()
        self.hr(fileh)

        return None

    def prompt_password(self, msg, default=None):
        """Convenient password prompting function

        :param msg: prompt text.
        :type msg: str.
        :param default: default value if user does not enter anything.
        :type default: str.
        :returns: string user entered, or default if nothing entered
        """
        message = "%s : " % msg

        if default is not None:
            message = "%s [%s] : "%(msg, default)

        i = getpass.getpass(message)

        if i is None or len(i) == 0:
            i = default

        i = str(i)

        return i.strip()

class ArgumentHolder(object):
    """Data holder required for positional parameters"""
    def __init__(self, args):
        self.option_groups = []
        self.option_list = args

class PositionalArgument(optparse.Option):
    """A work around for optparse's lack of support for positional arguments"""
    def __init__(self, *opts, **attrs):
        attrs['action'] = 'store_true'
        optparse.Option.__init__(self, *opts, **attrs)

    def prompt(self):
        """Helper for prompt_password"""
        if self.prompt_masked is None:
            return None

        return CLI.prompt_password(self.prompt_masked)

class CustomOptionParser(optparse.OptionParser):
    """An option parser with support for positional parameter help"""
    optparse.Option.ATTRS.append('prompt_masked')
    def __init__(self, usage=None, option_list=None, \
                 option_class=optparse.Option, version=None, \
                 conflict_handler="error", description=None, formatter=None, \
                 add_help_option=True, prog=None, epilog=None, \
                 argument_heading="Arguments"):

        optparse.OptionParser.__init__(self, usage, option_list, option_class, \
                                       version, conflict_handler, description, \
                                       formatter, add_help_option, prog)

        self._argument_heading = argument_heading
        self._args = []
        self._repattern = re.compile(r'^\s*\-+')

    def format_help(self, formatter=None):
        """Function to help format help.

        :param formatter: formatter
        :type formatter: formatter
        """
        argh = ArgumentHolder(self._args)

        if formatter is None:
            formatter = self.formatter

        result = []
        formatter.store_option_strings(argh)

        if self.usage:
            result.append(self.get_usage() + "\n")
        if self.description:
            result.append(self.format_description(formatter) + "\n")
        if self._argument_heading:
            result.append(formatter.format_heading(self._argument_heading))
        if self._args:
            result.append(self.format_argument_help(formatter))

        result.append(self.format_option_help(formatter))
        result.append(self.format_epilog(formatter))

        return "".join(result)

    def add_argument(self, argument):
        """Add a positional argument.

        :param argument: positional argument to add
        :type argument: PositionalArgument object
        """
        self._args.append(argument)

    def get_arguments(self):
        """List of PostitionalArgument objects"""
        return self._args

    def format_argument_help(self, formatter):
        """Function to help format argument help.

        :param formatter: formatter
        :type formatter: formatter
        """
        if not self._args:
            return ""

        result = []
        for option in self._args:
            if not option.help is optparse.SUPPRESS_HELP:
                output = formatter.format_option(option)
                output = self._repattern.sub('  ', output)
                result.append(output)

        return '%s\n' % "".join(result)

    def get_usage(self):
        """A usage generator with support for positional parameters"""
        if self.usage:
            usg = self.expand_prog_name(self.usage)

            if self._args:
                for arg in self._args:
                    attrval = getattr(arg, 'prompt_masked')

                    if attrval:
                        continue

                    usg += ' %s' % arg.metavar.replace('-', '')

            return self.formatter.format_usage(usg)
        else:
            return ""

