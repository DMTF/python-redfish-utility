# Script Examples

The command catalog provided by the Redfish Utility enables a wide variety of options to manipulate and work with the server. Multiple commands chained together have the potential to provide higher-level functionality and meet any needs that arise depending on the task at hand.


## Selecting and getting properties from a type.

```
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

This is a batch file that logs into a remote server, selects the `ComputerSystem` type, and gets the `AssetTag` value.

## Saving and loading a file using file-based editing mode

```
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

This is a file-based edit mode helper for the Redfish Utility

1. Run to download selected type to a file called `redfish.json`

2. Edit the `redfish.json` file to make changes.

3. Press any key running batch program to continue with program, uploading the newly edited program to the server.
