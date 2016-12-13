# Using the Redfish Utility

## Redfish Utility Modes of operation

The Redfish Utility has three modes of operation. By default, the interactive mode is utilized when you start the Redfish Utility. With Scriptable Mode, you can use a script that gives commands to the Redfish Utility. File-Based mode allows you to use a script that gives commands to the Redfish Utility and use a file to load and save settings.

### Interactive mode

Interactive mode is started when you run the Redfish Utility without any command line parameters. The `redfish>` prompt is displayed and you can enter commands one at a time. You can exit the interactive mode by entering the `exit` command at the prompt. On Windows systems, double-click `redfish.exe` to start an interactive session. You must be an administrator to run `redfish.exe`.

![Interactive Mode](images/InteractiveMode_1.png "Interactive Mode")

### Scriptable mode

> The following script can be called to retrieve information regarding the **ComputerSystem** type:

```
:: This is a batch file that logs into a remote server,
:: selects the ComputerSystem type, and gets the AssetTag value

:: Usage :: 
:: selectget.bat [URI] [USERNAME] [PASSWORD] 
@echo off

set argC=0
for %%x in (%*) do Set /A argC+=1
if %argC% LSS 3 goto :failCondition
goto :main

:failCondition
@echo Usage:
@echo selectget.bat [URI] [USERNAME] [PASSWORD]
goto :EOF

:main
@echo *****************************************
@echo ************* Logging in... *************
@echo *****************************************
redfish.exe login %1 -u %2 -p %3
@echo *****************************************
@echo *** selecting ComputerSystem type... ****
@echo *****************************************
redfish.exe select ComputerSystem.
@echo *****************************************
@echo ********** getting AssetTag... **********
@echo *****************************************
redfish.exe get AssetTag
pause
```

Scriptable mode is used if you want to script all the commands with the use of an external input file. The script contains a list of the Redfish Utility command lines that let users get and set properties of server objects.

In our example, first the `ComputerSystem` type is selected, and then the **get** command is used to retrieve information about the `AssetTag` property of `ComputerSystem`

### File-based mode

> The following script allows you to save, edit, and load a file to the server.

```
:: This a file-based edit mode helper for the Redfish Utility
:: 1. Run to download selected type to a file called redfish.json
:: 2. Edit the redfish.json file to make changes.
:: 3. Press any key running batch program to continue with program,
::    uploading the newly edited program to the server.

:: Usage ::
:: saveload.bat [SELECTOR] [FILENAME]
:: Specify a type with the SELECTOR tag, and
:: save to a file called FILENAME
@echo off
set argC=0
for %%x in (%*) do Set /A argC+=1
if %argC% LSS 2 goto :failCondition
goto :main

:failCondition
@echo Usage:
@echo saveload.bat [SELECTOR] [FILENAME]
@echo specify a type with the SELECTOR tag, and
@echo save to a file called FILENAME
goto :EOF

:main
redfish.exe login
redfish.exe save --selector=%1 --json -f %2
@echo Edit the file, then:
pause
redfish.exe load -f %2

```

File-based mode allows you to save and load settings from a file. File-based mode supports the JSON format.

When the example script is run, the following result is produced:

![File Mode example](images/FileBasedMode_1.png "File Based Mode example")

Here, the `ComputerSystem` type is saved to a file called `redfish1.json`. Then, after you modify any properties, the **load** command is used to make these changes on the server. 

The properties of `ComputerSystem` can be edited here, and then loaded on the server. When the file is loaded on the server, the Redfish Utility will attempt to patch all values in the file.
<aside class="warning">When you try to load a file make sure to remove all read only properties. If any properties fail to patch the Redfish Utility will return an error.</aside>
> After saving this configuration, the **redfish1.json** file looks like this:

```
{
	"#ComputerSystem.v1_2_0.ComputerSystem": {
		"/redfish/v1/Systems/1/": {
			"AssetTag": "newassettag"
		}
	}
}
```

## Configuration file (redfish.conf)

> default configuration file

```
[redfish]
#The Redfish Utility reads the following environment variables, and applies them at runtime.  
#Note that they can be overridden by command line switches.

#####         Cache Settings         #####
##########################################
# option to disable caching of all data
#cache = False

#####       Credential Settings      #####
##########################################
# option to use the provided url to login
#url = https://127.0.0.1

# option to use the provided username to login
#username = admin

# option to use the provided password to login
#password = password

#####         Commit Settings        #####
##########################################
# flag to commit in all places where applicable
#commit = True

#####    Output Default Settings     #####
##########################################
# flag to change output format in all places where applicable
#format = json

#####  Default Save/Load Settings    #####
##########################################
# option to set default save output file
#savefile = redfish.json

# option to set default load input file
#loadfile = redfish.json

```

The configuration file contains the default settings for the utility. You can use a text editor to change the behavior of the utility such as adding a server IP address, username, and password so you do not need to type this each time when you use the utility.

Configuration file locations:

- Windows OS: The same location as the executable file that starts the utility.
- Linux OS: `/etc/redfish/redfish.conf`
