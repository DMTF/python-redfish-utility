###
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/python-redfish-utility/blob/master/LICENSE.md
###

""" Load Command for RDMC """

import os
import sys
import json
import shlex
import subprocess

from queue import Queue
from datetime import datetime
from optparse import OptionParser
from rdmc_helper import ReturnCodes, InvalidCommandLineError, \
                    InvalidCommandLineErrorOPTS, InvalidFileFormattingError, \
                    NoChangesFoundOrMadeError, InvalidFileInputError, \
                    NoDifferencesFoundError, MultipleServerConfigError, \
                    InvalidMSCfileInputError

from rdmc_base_classes import RdmcCommandBase, HARDCODEDLIST

from redfish.ris.rmc_helper import LoadSkipSettingError

#default file name
__filename__ = 'redfish.json'

class LoadCommand(RdmcCommandBase):
    """ Constructor """
    def __init__(self, rdmcObj):
        RdmcCommandBase.__init__(self,\
            name='load',\
            usage='load [OPTIONS]\n\n\tRun to load the default configuration' \
            ' file\n\texample: load\n\n\tLoad configuration file from a ' \
            'different file\n\tif any property values have changed, the ' \
            'changes are committed and the user is logged out of the server'\
            '\n\n\texample: load -f output.json\n\n\tLoad configurations to ' \
            'multiple servers\n\texample: load -m mpfilename.txt -f output.' \
            'json\n\n\tNote: multiple server file format (1 server per new ' \
            'line)\n\t--url <url/hostname> -u admin -p password\n\t--url ' \
            '<url/hostname> -u admin -p password\n\t--url <url/hostname> -u ' \
            'admin -p password',\
            summary='Loads the server configuration settings from a file.',\
            aliases=[],\
            optparser=OptionParser())
        self.definearguments(self.parser)
        self.filenames = None
        self.mpfilename = None
        self.queue = Queue()
        self._rdmc = rdmcObj
        self.lobobj = rdmcObj.commandsDict["LoginCommand"](rdmcObj)
        self.selobj = rdmcObj.commandsDict["SelectCommand"](rdmcObj)
        self.setobj = rdmcObj.commandsDict["SetCommand"](rdmcObj)
        self.comobj = rdmcObj.commandsDict["CommitCommand"](rdmcObj)
        self.logoutobj = rdmcObj.commandsDict["LogoutCommand"](rdmcObj)

    def run(self, line):
        """ Main load worker function

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

        self.loadvalidation(options)
        returnValue = False

        loadcontent = dict()
        if options.mpfilename:
            sys.stdout.write("Loading configuration for multiple servers...\n")
        else:
            sys.stdout.write("Loading configuration...\n")

        for files in self.filenames:
            if not os.path.isfile(files):
                raise InvalidFileInputError("File '%s' doesn't exist. Please " \
                                "create file by running save command." % files)

            with open(files, "r") as myfile:
                data = myfile.read()

            try:
                loadcontents = json.loads(data)
            except:
                raise InvalidFileFormattingError("Invalid file formatting " \
                                                    "found in file %s" % files)

            if options.mpfilename:
                mfile = options.mpfilename
                outputdir=None

                if options.outdirectory:
                    outputdir=options.outdirectory

                if self.runmpfunc(mpfile=mfile, lfile=files, \
                                                        outputdir=outputdir):
                    return ReturnCodes.SUCCESS
                else:
                    raise MultipleServerConfigError("One or more servers "\
                                        "failed to load given configuration.")

            results = False

            for loadcontent in loadcontents:
                skip = False

                for content, loaddict in loadcontent.iteritems():
                    inputlist = list()

                    if content == "Comments":
                        skip = True
                        break

                    inputlist.append(content)

                    self.selobj.selectfunction(inputlist)
                    if self._rdmc.app.get_selector().lower() not in \
                                                                content.lower():
                        raise InvalidCommandLineError("Selector not found.\n")

                    try:
                        for _, items in loaddict.iteritems():
                            dicttolist = list(items.items())

                            if len(dicttolist) < 1:
                                continue

                            multilevel = [isinstance(x[1], dict) for x in \
                                                                    dicttolist]
                            indices = [i for i, j in enumerate(multilevel) if j]

                            if len(indices) > 0:
                                for index in indices:
                                    changes = []
                                    self.loadmultihelper(dicttolist[index][0], \
                                                 dicttolist[index][1], changes)

                                    for change in changes:
                                        if self._rdmc.app.loadset(dicttolist=\
                                                dicttolist, newargs=change[0], val=change[0]):
                                            results = True

                                indices.sort(cmp=None, key=None, reverse=True)

                                #Test validate thoroughly
                                for index in indices:
                                    del dicttolist[index]

                            if len(dicttolist) < 1:
                                continue

                            try:
                                if self._rdmc.app.loadset(\
                                      dicttolist=dicttolist):
                                    results = True
                            except LoadSkipSettingError:
                                returnValue = True
                                results = True
                                pass
                            except Exception:
                                raise
                    except Exception:
                        raise

                if skip:
                    continue

                try:
                    if results:
                        self.comobj.commitfunction()
                except NoChangesFoundOrMadeError:
                    if returnValue:
                        pass
                    else:
                        raise

            if not results:
                raise NoDifferencesFoundError("No differences found from " \
                                                    "current configuration.")

        #Return code
        if returnValue:
            return ReturnCodes.LOAD_SKIP_SETTING_ERROR
        else:
            return ReturnCodes.SUCCESS

    def loadmultihelper(self, sel, val, changes):
        """ Load multi helper function

        :param sel: current property
        :type sel: string.
        :param val: current value for property
        :type val: string.
        :param changes: current changes
        :type changes: string.
        """
        results = list()

        if isinstance(val, dict):
            for first, second in val.iteritems():
                (results, finalval) = self.loadmultihelper(first, second, \
                                                                        changes)
                results.insert(0, sel)
        else:
            results.append(sel + "=" + str(val))
            finalval = val
            changes.append((results, finalval))

        return (results, finalval)

    def loadvalidation(self, options):
        """ Load method validation function

        :param options: command line options
        :type options: list.
        """
        inputline = list()
        runlogin = False

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

        try:
            if runlogin:
                self.lobobj.loginfunction(inputline)
        except Exception:
            if options.mpfilename:
                pass
            else:
                raise

        #filename validations and checks
        if options.filename:
            self.filenames = options.filename
        elif self._rdmc.app.config:
            if self._rdmc.app.config._ac__loadfile:
                self.filenames = [self._rdmc.app.config._ac__loadfile]

        if not self.filenames:
            self.filenames = [__filename__]

    def verify_file(self, filedata, inputfile):
        """ Function used to handle oddly named files and convert to JSON

        :param filedata: input file data
        :type filedata: string.
        :param inputfile: current input file
        :type inputfile: string.
        """
        try:
            tempholder = json.loads(filedata)
            return tempholder
        except:
            raise InvalidFileFormattingError("Invalid file formatting found" \
                                                    " in file %s" % inputfile)

    def get_current_selector(self, path=None):
        """ Returns current selected content minus hard coded list

        :param path: current path
        :type path: string.
        """
        contents = self._rdmc.app.get_save(onlypath=path)
        if not contents:
            contents = list()
        for content in contents:
            for k in content.keys():
                if k.lower() in HARDCODEDLIST or '@odata' in k.lower():
                    del content[k]

        return contents

    def runmpfunc(self, mpfile=None, lfile=None, outputdir=None):
        """ Main worker function for multi file command

        :param mpfile: configuration file
        :type mpfile: string.
        :param lfile: custom file name
        :type lfile: string.
        :param outputdir: custom output directory
        :type outputdir: string.
        """
        self.logoutobj.run("")
        data = self.validatempfile(mpfile=mpfile, lfile=lfile)

        if data == False:
            return False

        processes = []
        finalreturncode = True
        outputform = '%Y-%m-%d-%H-%M-%S'

        if outputdir:
            if outputdir.endswith(('"',"'")) and \
                                                outputdir.startswith(('"',"'")):
                outputdir=outputdir[1:-1]

            if not os.path.isdir(outputdir):
                sys.stdout.write("The give output folder path does not " \
                                                                    "exist.\n")
                raise InvalidCommandLineErrorOPTS("")

            dirpath=outputdir
        else:
            dirpath = os.getcwd()

        dirname = '%s_%s' % (datetime.now().strftime(outputform), 'MSClogs')
        createdir = os.path.join(dirpath, dirname)
        os.mkdir(createdir)

        oofile = open(os.path.join(createdir, 'CompleteOutputfile.txt'), 'w+')
        sys.stdout.write('Create multiple processes to load configuration '\
                                            'concurrently to all servers...\n')

        while True:
            if not self.queue.empty():
                line = self.queue.get()
            else:
                break

            finput = '\n'+ 'Output for '+ line[line.index('--url')+1]+': \n\n'
            urlvar = line[line.index('--url')+1]
            listargforsubprocess = [sys.executable] + line

            if os.name is not 'nt':
                listargforsubprocess = " ".join(listargforsubprocess)

            logfile = open(os.path.join(createdir, urlvar+".txt"), "w+")
            pinput = subprocess.Popen(listargforsubprocess, shell=True,\
                                                stdout=logfile, stderr=logfile)

            processes.append((pinput, finput, urlvar, logfile))

        for pinput, finput, urlvar, logfile in processes:
            pinput.wait()
            returncode = pinput.returncode
            finalreturncode = finalreturncode and not returncode

            logfile.close()
            logfile = open(os.path.join(createdir, urlvar+".txt"), "r+")
            oofile.write(finput + str(logfile.read()))
            oofile.write('-x+x-'*16)
            logfile.close()

            if returncode == 0:
                sys.stdout.write('Loading Configuration for {} : SUCCESS\n'\
                                                                .format(urlvar))
            else:
                sys.stdout.write('Loading Configuration for {} : FAILED\n'\
                                                                .format(urlvar))
                sys.stderr.write('return code : {}.\nFor more '\
                         'details please check {}.txt under {} directory.\n'\
                                        .format(returncode, urlvar, createdir))

        oofile.close()

        if finalreturncode:
            sys.stdout.write('All servers have been successfully configured.\n')

        return finalreturncode

    def validatempfile(self, mpfile=None, lfile=None):
        """ Validate temporary file

        :param mpfile: configuration file
        :type mpfile: string.
        :param lfile: custom file name
        :type lfile: string.
        """
        sys.stdout.write('Checking given server information...\n')

        if not mpfile:
            return False

        if not os.path.isfile(mpfile):
            raise InvalidFileInputError("File '%s' doesn't exist, please " \
                            "create file by running save command." % mpfile)

        try:
            with open(mpfile, "r") as myfile:
                data = list()
                cmdtorun = ['load']
                cmdargs = ['-f', str(lfile)]
                globalargs = ['-v', '--nocache']

                while True:
                    line = myfile.readline()

                    if not line:
                        break

                    if line.endswith(os.linesep):
                        line.rstrip(os.linesep)

                    args = shlex.split(line, posix=False)

                    if len(args) < 5:
                        sys.stderr.write('Incomplete data in input file: {}\n'\
                                                                .format(line))
                        raise InvalidMSCfileInputError('Please verify the '\
                                            'contents of the %s file' %mpfile)
                    else:
                        linelist = globalargs + cmdtorun + args + cmdargs
                        line = str(line).replace("\n", "")
                        self.queue.put(linelist)
                        data.append(linelist)
        except Exception:
            raise

        if data:
            return data
        else:
            return False

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
            '-m',
            '--multiprocessing',
            dest='mpfilename',
            help="""use the provided filename to obtain data""",
            default=None,
        )
        customparser.add_option(
            '-o',
            '--outputdirectory',
            dest='outdirectory',
            help="""use the provided directory to output data for multiple server configuration""",
            default=None,
        )

