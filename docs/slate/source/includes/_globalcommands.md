## Global commands

This section includes commands as well as their usage and examples for general commands in the Redfish Utility. They include commands used to do things such as listing help for using commands, viewing, retrieving, modifying, and committing changes to server properties, and authenticating and logging in and out of the server.

### Help Command

> Help example commands:

```
redfish > help
Usage: redfish [GLOBAL OPTIONS] [COMMAND] [ARGUMENTS] [COMMAND OPTIONS]

Options:
  -h, --help            Show this help message and exit.
  -c FILE, --config=FILE
                        Use the provided configuration file instead of the
                        default one.
  --cache-dir=PATH      Use the provided directory as the location to cache
                        data (default location:
                        C:\Users\USERNAME\AppData\Roaming\.redfish

  GLOBAL OPTIONS:
    -v, --verbose       Display verbose information.
    -d, --debug         Display debug information.
    --nocache           During execution the application will temporarily
                        store data only in memory.
    --nologo            Include to block logo.

COMMANDS
  commit                       - Applies all the changes made during the
                                  current session.
  get                          - Displays the current value(s) of a
                                  property(ies) within a selected type.
  list                         - Displays the current value(s) of a
                                  property(ies) within a selected type
                                  including reserved properties.
  load                         - Loads the server configuration settings from
                                  a file.
  login                        - Connects to a server, establishes a secure
                                  session, and discovers data.
  logout                       - Ends the current session and disconnects from
                                  the server.
  save                         - Saves the selected type's settings to a file.
  select                       - Selects the object type to be used.
  set                          - Changes the value of a property within the
                                  currently selected type.
  status                       - Displays all pending changes within a
                                  selected type that need to be committed.
  types                        - Displays all selectable types within the
                                  currently logged in server.
  exit                         - Exits from the interactive shell.
  help                         - Displays command line syntax and help menus
                                  for individual commands. Example: help login

RAW COMMANDS
  rawdelete                    - This is the raw form of the DELETE command.
  rawget                       - This is the raw form of the GET command.
  rawhead                      - This is the raw form of the HEAD command.
  rawpatch                     - This is the raw form of the PATCH command.
  rawpost                      - This is the raw form of the POST command.
  rawput                       - This is the raw form of the PUT command.
redfish >

```

> **Above:** Entering the help to list the global redfish options and help options for all available commands.

```
redfish > help login
Usage: login [URL] [OPTIONS]

        To login remotely run using url and credentials
        example: login <url/hostname> -u <username> -p <password>

        To login on a local server run without arguments
        example: login

Options:
  -h, --help            show this help message and exit
  --url=URL             Use the provided URL to login.
  -u USER, --user=USER  If you are not logged in yet, including this flag
                        along with the password and URL flags can be used to
                        log into a server in the same command.
  -p PASSWORD, --password=PASSWORD
                        Use the provided password to log in.
  --includelogs         Optionally include logs in the data retrieval process.
  --selector=SELECTOR   Optionally include this flag to select a type to run
                        the current command on. Use this flag when you wish to
                        select a type without entering another command, or if
                        you wish to work with a type that is different from
                        the one you currently have selected.
  --filter=FILTER       Optionally set a filter value for a filter attribute.
                        This uses the provided filter for the currently
                        selected type. Note: Use this flag to narrow down your
                        results. For example, selecting a common type might
                        return multiple objects that are all of that type. If
                        you want to modify the properties of only one of those
                        objects, use the filter flag to narrow down results
                        based on properties.
                        Usage: --filter [ATTRIBUTE]=[VALUE]
  --path=PATH           Optionally set a starting point for data collection.
                        If you do not specify a starting point, the default
                        path will be /redfish/v1/. Note: The path flag can
                        only be specified at the time of login, so if you are
                        already logged into the server, the path flag will not
                        change the path. If you are entering a command that
                        isn't the login command, but include your login
                        information, you can still specify the path flag
                        there.
```

> **Above:** Providing a specific command will list help regarding that specific command.

```
redfish > login -h
Usage: login [URL] [OPTIONS]

        To login remotely run using url and credentials
        example: login <url/hostname> -u <username> -p <password>

        To login on a local server run without arguments
        example: login

Options:
  -h, --help            show this help message and exit
  --url=URL             Use the provided URL to login.
  -u USER, --user=USER  If you are not logged in yet, including this flag
                        along with the password and URL flags can be used to
                        log into a server in the same command.
  -p PASSWORD, --password=PASSWORD
                        Use the provided password to log in.
  --includelogs         Optionally include logs in the data retrieval process.
  --selector=SELECTOR   Optionally include this flag to select a type to run
                        the current command on. Use this flag when you wish to
                        select a type without entering another command, or if
                        you wish to work with a type that is different from
                        the one you currently have selected.
  --filter=FILTER       Optionally set a filter value for a filter attribute.
                        This uses the provided filter for the currently
                        selected type. Note: Use this flag to narrow down your
                        results. For example, selecting a common type might
                        return multiple objects that are all of that type. If
                        you want to modify the properties of only one of those
                        objects, use the filter flag to narrow down results
                        based on properties.
                        Usage: --filter [ATTRIBUTE]=[VALUE]
  --path=PATH           Optionally set a starting point for data collection.
                        If you do not specify a starting point, the default
                        path will be /redfish/v1/. Note: The path flag can
                        only be specified at the time of login, so if you are
                        already logged into the server, the path flag will not
                        change the path. If you are entering a command that
                        isn't the login command, but include your login
                        information, you can still specify the path flag
                        there.
```

> **Above:** The alternate syntax to list details regarding a command.

#### Syntax

help *[command] [optional parameters]*

#### Description

Displays command line syntax and help menus for individual commands. Use this command if you want to know more about a command or need help using a command. Alternatively, you can use the `help` command without specifying a particular command if you wish to see all available commands and options.

#### Parameters

- Command 

Supplying a command to help will cause this command to display the help message corresponding to the given command, as well as the options relating to that particular command.

<aside class="notice">If no command is provided, the help command will provide help on all available commands and options.</aside>

- **-h, --help**

Running the help command with the **–h** or **–help** command will display information on how to use the help command.

- **-c FILE, --config=FILE**

Use the provided configuration file instead of the default one.

- **--cache-dir=PATH**

Use the provided directory as the location to cache data (default location: `C:\Users\USERNAME\AppData\Roaming\.redfish`).

#### Global Options

**-v, --verbose**

Display verbose information.

**-d, --debug**

Display debug information.

**-nocache**

During execution the application will temporarily store data only in memory.

**-nologo**

Include to block logo.

#### Inputs

None

#### Outputs

None

### Login command

> Login example commands:

```
redfish > login xx.xx.xx.xx -u username -p password --selector=ComputerSystem.
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select
Current selection: 'ComputerSystem.'
```

> **Above:** To login remotely, supply the URL, username, and password for the server. Here the selector tag has been included so that the **ComputerSystem** type is selected once the user is logged in. You can prove that the **ComputerSystem** type has indeed been selected when we enter the select command.

```
redfish > login xx.xx.xx.xx -u username -p password --path=/redfish/v1/Managers/1/VirtualMedia/
Discovering data...Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > types
Type options:
#VirtualMedia.v1_0_0.VirtualMedia
#VirtualMediaCollection.VirtualMediaCollection

redfish > login xx.xx.xx.xx -u username -p password --path=/redfish/v1/
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > types
Type options:
#AccountService.v1_0_2.AccountService
#Bios.v1_0_0.Bios
#Chassis.v1_2_0.Chassis
#ChassisCollection.ChassisCollection
#ComputerSystem.v1_2_0.ComputerSystem
#ComputerSystemCollection.ComputerSystemCollection
...
#VirtualMedia.v1_0_0.VirtualMedia
#VirtualMediaCollection.VirtualMediaCollection
```

> **Above:** Here the path was set to **/redfish/v1/managers/1/virtualmedia/** instead of the default **/redfish/v1/**. To check that the path has indeed been set to a different place, the types command was entered and returned the types in the specified path, instead of in the default **/redfish/v1/**. You can log in again with the default **/redfish/v1/** to show the change.

#### Syntax

login *[URL] [User] [Password] [Optional Parameters]*

#### Description

Connects to a server, establishes a secure session, and discovers data from that server. Use the `login` command to connect to a server. This command establishes a secure session and discovers data from that server.

#### Parameters

- **URL**

Connect to the server located at the provided URL.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User**

Connect to the server as the provided user.

- **-p Password**

Connect to the server with the password corresponding to the given user.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--selector=SELECTOR**

Optionally including the **selector** flag allows you to select a type to run the current command on. Use this flag when you wish to select a type without entering another command, or if you wish to work with a type that is different from the one you currently have selected.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice">Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the <b>filter</b> flag to narrow down results based on properties.</aside>

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be /redfish/v1/.

<aside class="notice">The path flag can only be specified at the time of login, so if you are already logged in to the server, the path flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the path flag there.</aside>

<aside class="warning">Cache is activated session keys and it is normal to see these keys stored in plaintext. This warning regarding an activated cache is normal to see. The full list has been truncated for space.</aside>

### Types command

> Types example commands:

```
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > types
Type options:
#AccountService.v1_0_2.AccountService
#Bios.v1_0_0.Bios
#Chassis.v1_2_0.Chassis
#ChassisCollection.ChassisCollection
#ComputerSystem.v1_2_0.ComputerSystem
#ComputerSystemCollection.ComputerSystemCollection
...
#VirtualMedia.v1_0_0.VirtualMedia
#VirtualMediaCollection.VirtualMediaCollection
```

> **Above:** This command will list all the available types that you can select. The full list has been truncated for space.

```
redfish > types -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
Type options:
#AccountService.v1_0_2.AccountService
#Bios.v1_0_0.Bios
#Chassis.v1_2_0.Chassis
#ChassisCollection.ChassisCollection
#ComputerSystem.v1_2_0.ComputerSystem
#ComputerSystemCollection.ComputerSystemCollection
...
#VirtualMedia.v1_0_0.VirtualMedia
#VirtualMediaCollection.VirtualMediaCollection
```

> **Above:** This command simultaneously logs in to the server at the provided URL with the provided username and password, and list all the available types that you can select. The full list has been truncated here for space.

```
redfish > types -u username -p password --url=xx.xx.xx.xx --path=/redfish/v1/Managers/1/VirtualMedia/
Discovering data.....Done
WARNING: Cache is activated session keys are stored in plaintext
Type options:
#VirtualMedia.v1_0_0.VirtualMedia
#VirtualMediaCollection.VirtualMediaCollection
```

> **Above:** Specifying a path for the type command will print the types found in the given path. Here only the types found in **/redfish/v1/Managers/1/VirtualMedia/** were returned.

#### Syntax

types *[Optional Parameters]*

#### Description

The `types` command displays all selectable types available within the currently logged in server. Types include a name as well as version information. Types represent the schema used for the resource and indicate the version of the schema. Version information is `major.minor.errata` (for example `#ComputerSystem.v1_2_0.ComputerSystem`). Major versions are not backwards compatible, but everything else is.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be` /redfish/v1/`.

<aside class="notice">The <b>path</b> flag can only be specified at the time of login, so if you are already logged into the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the <b>login</b> command, but include your login information, you can still specify the path flag there.</aside>

#### Inputs

None

#### Outputs

None

### Select command

> Select example commands:

```
redfish > select ComputerSystem. -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select
Current selection: 'ComputerSystem.'
```

> **Above:** Before the commands were entered here, the user was not logged in to the server. When you use the select tag with login credentials, you are logged in to the server and the inputted type is selected. The type was selected by entering the select command with no type specified is verified, which shows that the currently selected type is returned. Note the addition of a period after the type selected, **ComputerSystem**. Using a period here limits the selection, preventing accidentally also selecting **ComputerSystemCollection**. This also removes the need to include the version.

```
redfish > select Chassis. -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select
Current selection: 'Chassis.'
```

> **Above:** Here the **Chassis** type was selected instead of the **ComputerSystem** type like in the example above.

#### Syntax

select *[Type] [Optional Parameters]*

#### Description

Use `select` to choose a specific type to work with. Eligible types for selection are those listed by the types command. Because commands are entered individually in the Redfish Utility, working with specific types requires that you highlight or select the particular type you are working with. Use the `select` command to highlight a type so that you can work with it.

#### Parameters

- **Type**

Specify the type you want to select. Omitting a type to select will cause select to display the currently selected type.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice"> Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the filter flag to narrow down results based on properties.</aside>

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be` /redfish/v1/`.

<aside class="notice"> The <b>path</b> flag can only be specified at the time of login, so if you are already logged in to the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the <b>path</b> flag there.</aside>

#### Inputs

None

#### Outputs

None

### List command

> List command examples:

```
redfish > login xx.xx.xx.xx –u username –p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > select Bios.
redfish > list
@odata.context=/redfish/v1/$metadata#Bios.Bios
@odata.type=#Bios.v1_0_0.Bios
Attributes=
            MemFastTraining=Enabled
			...
            TpmState=NotPresent

            CollabPowerControl=Enabled
Description=Platform/BIOS Configuration (RBSU) Pending Settings
Name=BIOS Configuration Pending Settings
```

> **Above:** This command shows the current values of the properties of the selected type, including reserved properties. The full list has been truncated here for space.

```
redfish > login xx.xx.xx.xx –u username –p password 
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > select Bios.
redfish > list --json
{
  "@odata.context": "/redfish/v1/$metadata#Bios.Bios",
  "@odata.type": "#Bios.v1_0_0.Bios",
  "Attributes": {
    "MemFastTraining": "Enabled",
	...
    "TpmState": "NotPresent",
    "CollabPowerControl": "Enabled"
  },
  "Description": "Platform/BIOS Configuration (RBSU) Pending Settings",
  "Name": "BIOS Configuration Pending Settings"
}
```

> **Above:** Including the **--json** tag preserves the JSON structure of the type’s information. The full list has been truncated here for space.

```
redfish > list -u username -p password --url=xx.xx.xx.xx --selector=Bios.
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
@odata.context=/redfish/v1/$metadata#Bios.Bios
@odata.type=#Bios.v1_0_0.Bios
Attributes=
            MemFastTraining=Enabled
			...
            TpmState=NotPresent

            CollabPowerControl=Enabled
Description=Platform/BIOS Configuration (RBSU) Pending Settings
Name=BIOS Configuration Pending Settings
```

```
redfish > select EthernetInterface. –u username –p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > list --json
{
  "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces
/Members/$entity",
  "@odata.etag": "W/\"15C8AD78\"",
  "@odata.id": "/redfish/v1/Managers/1/EthernetInterfaces/1/",
  "@odata.type": "#EthernetInterface.v1_0_0.EthernetInterface",
  "AutoNeg": true,
  "Description": "Configuration of this Manager Network Interface",
...
}
{
  "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces
/Members/$entity",
  "@odata.etag": "W/\"9F621D6E\"",
  "@odata.id": "/redfish/v1/Managers/1/EthernetInterfaces/2/",
  "@odata.type": "#EthernetInterface.v1_0_0.EthernetInterface",
  "AutoNeg": null,
  "Description": "Configuration of this Manager Network Interface",
..
}
redfish > list --filter Id=2 --json
{
  "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces
/Members/$entity",
  "@odata.etag": "W/\"9F621D6E\"",
  "@odata.id": "/redfish/v1/Managers/1/EthernetInterfaces/2/",
  "@odata.type": "#EthernetInterface.v1_0_0.EthernetInterface",
  "AutoNeg": null,
  "Description": "Configuration of this Manager Network Interface",
...
}
```

> **Above:** After the server is logged in to and the <b>EthernetInterface</b> type is selected, the list command reveals that there are two objects with that type on the server. So, to only show the one at **/redfish/v1/Managers/1/EthernetInterfaces/2/**, the list command was run again with the **--filter** flag included. The full list has been truncated here for space.

#### Syntax

list *[Optional Parameters]*

#### Description

Displays the JSON model of the currently selected type, showing current value(s) of properties including reserved properties. After you have selected a type, you can use the list command to see the details of the currently selected type. This includes information such as current values of properties.

<aside class="notice">The list command does display reserved properties for types, while the get command does not.</aside>

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice"> Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the filter flag to narrow down results based on properties.</aside>

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be `/redfish/v1/`.

<aside class="notice"> The <b>path</b> flag can only be specified at the time of login, so if you are already logged in to the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the <b>path</b> flag there.</aside>

- **--logout**

Optionally include the logout flag to log out of the server after this command is completed. You need to be logged in to use this flag.

#### Inputs

None

#### Outputs

None

### Get command

> Get example commands:

```
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select Bios.
redfish > get
Attributes=
            MemFastTraining=Enabled

			...

            TpmState=NotPresent

            CollabPowerControl=Enabled
```

> **Above:** Using get without any property specified shows the properties of the selected type. Note that no reserved properties are shown with the get command. Also, the full list has been truncated for space.

```
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select Bios.
redfish > get Attributes/AdminName
Attributes=
            AdminName=NewAdminName
```

> **Above:** Using get with a specific property lists the current value of that property, given that a type has already been selected.

```
redfish > get Attributes/AdminEmail -u username -p password --url=xx.xx.xx.xx --selector=Bios. 
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
Attributes=
            AdminEmail=test@test.com
```

> **Above:** Here the server at xx.xx.xx.xx is logged into, the type Bios. is selected, and the get command is used to retrieve the AdminEmail property of Bios.

```
redfish > login xx.xx.xx.xx –u username –p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > select Bios.
redfish > get Attributes/AdminPhone --logout
Attributes=
            AdminPhone=""
Logging session out.
```

> **Above:** Because the logout flag was included here, the user is logged out of the server after the get command here is performed.

```
redfish > login xx.xx.xx.xx –u username –p password 
redfish > select VirtualMedia.
redfish > get ConnectedVia MediaTypes
ConnectedVia=NotConnected
ConnectedVia=NotConnected
MediaTypes=Floppy

            USBStick
MediaTypes=CD

            DVD
redfish > get ConnectedVia MediaTypes --filter @odata.id=/redfish/v1/Managers/1/
VirtualMedia/2/
ConnectedVia=NotConnected
MediaTypes=CD

            DVD
```

> **Above:** Here, the get command utilizes its ability to take multiple properties as arguments. The first time the get command was used on the **ConnectedVia** and **MediaTypes property**, two objects of type **VirtualMedia** and **MediaTypes** were returned. However, to get the **ConnectedVia** and **MediaTypes** value for only one of the types, the filter tag was included. When the get command was run with the filter, the only value printed this time was the **ConnectedVia** value and the **MediaTypes** value for the **VirtualMedia** located with the specified @odata.id.

#### Syntax

get *[Property] [Optional Parameters]*

#### Description

Displays the current value of a property of the currently selected type. Use the `get` command to retrieve the current value of a property. Use this command only after a type has already been selected. If the value you are looking up has no value, it will return with no contents found for that property entry.

<aside class="notice">The difference between the <b>get</b> command and the <b>list</b> command is that the <b>list</b> command also lists details about reserved properties, while the <b>get</b> command does not.</aside>

#### Parameters

- **Property**

Supplying a property will cause get to display the current value for that particular property. Otherwise, if you wish to retrieve all the properties, run without arguments. This is still assuming you have a type already selected.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice"> Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the <b>filter</b> flag to narrow down results based on properties.</aside>

- **-j, --json**

Optionally include this flag if you wish to change the displayed output to JSON format. Preserving the JSON data structure makes the information easier to read.

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be `/redfish/v1/`.

<aside class="notice"> The <b>path</b> flag can only be specified at the time of login, so if you are already logged in to the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the <b>path</b> flag there.</aside>

- **--logout**

Optionally include the logout flag to log out of the server after this command is completed. You need to be logged in to use this flag.

#### Inputs

None

#### Outputs

None

### Set command

> Set example commands:

```
redfish > login xx.xx.xx.xx –u username –p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > select Bios.
redfish > set "Attributes/AdminName=John Doe" Attributes/ServiceName=ExampleService
redfish > get Attributes/AdminName Attributes/ServiceName
Attributes=
            AdminName=John Doe
Attributes=
            ServiceName=ExampleService
```

> **Above:** Here the **ServiceName** property of the type **Bios** has been set to the value **ExampleService**. When the get command is performed next, the value of **ServiceName** has been set to **ExampleService**. Note that, despite the get command showing that **ServiceName** has been set to **ExampleService**, if the commit command is not performed next, then the changes will not be reflected next time the server is logged into.

```
set Attributes/ServiceName=ExampleService2 -u username -p password --url=xx.xx.xx.xx --selector=Bios.
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > get Attributes/ServiceName
Attributes=
            ServiceName=ExampleService2
```

> **Above:** Set the attribute of a type using the set command. Here the server is logged into using the username, password, and URL flags, and then **Bios** is selected with the selector flag. Then, the **ServiceName** property is set.

```
redfish > set Attributes/AdminName=JohnDoe -u username -p password --url xx.xx.xx.xx --selector=Bios. --commit
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
Committing changes...
The operation completed successfully.
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > get Attributes/AdminName --selector=Bios.
Attributes=
            AdminName=JohnDoe
```

> **Above:** Here the **AdminName** property of the type **Bios** was set to the value **JohnDoe**. Including the commit flag committed the changes, so that after logging back into the server, the **AdminName** becomes **JohnDoe**. Otherwise it would have returned to its previous value.

```
redfish > set Attributes/AdminName=JohnDoe -u username -p password --url=xx.xx.xx.xx --selector=Bios. --logout
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
Logging session out.
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > get Attributes/AdminName –u username –p password --url=xx.xx.xx.xx --selector=Bios.
Attributes=
            AdminName=""
```

> **Above:** Here the **AdminName** property of the type **Bios** was set to the value **JohnDoe**. However, since the commit flag was not set, after the server is logged into again the **AdminName** property has returned to its original value.

#### Syntax

set *[Property=Value] [Path] [Optional Parameters]*

<aside class="notice">The syntax formats used to set properties can be tricky if not done correctly. See the following examples to illustrate how the syntax works.</aside>

- `set Attributes/AdminName=John`

This is **correct** syntax. This sets the `AdminName` to John.

- `set “Attributes/AdminName=John Doe”`

This is **correct** syntax. If the property has a space in it, use quotes around the entire property/value pair. Here the `AdminName` has been set to John Doe.

- `set Attributes/AdminName=””`

This is **correct** syntax. Use this syntax if you wish to remove the `AdminName` property value, using quotes that have nothing between them.

- `set Attributes/AdminName=’’`

This is **correct** syntax. This is an alternate syntax that also removes the `AdminName` property and sets it to nothing. Use single quotes with nothing between them.

- `set Attributes/AdminName=’””’`

This is **correct** syntax. This deletes the `AdminName` value.

- `set Attributes/AdminName=”John Doe”`

This is **incorrect** syntax, and will not be correctly reflected on the server.

#### Description

Given that a type is currently selected, changes the value of a property in that type. Use the `set` command to assign a value to the property of a type, provided that a type has already been selected. Properties in a multilevel path can be set using this command, and multiple properties of a type can also be simultaneously set.

<aside class="warning">No changes you have set will be reflected on the server unless you commit your changes afterward.</aside>

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--selector=SELECTOR**

Optionally include the selector flag to select a type to run the current command on. Use this flag when you wish to select a type without entering another command, or if you wish to work with a type that is different from the one you currently have selected.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice"> Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the filter flag to narrow down results based on properties.</aside>

- **--commit**

Use this flag when you are ready to commit all the changes for the current selection. Including the --commit flag will log you out of the server after the command is run. Some changes made in this way will be updated instantly, while others will be reflected the next time the server is started.

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be` /redfish/v1/`.

<aside class="notice"> The <b>path</b> flag can only be specified at the time of login, so if you are already logged in to the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the <b>path</b> flag there.</aside>

- **--logout**

Optionally include the logout flag to log out of the server after this command is completed. You need to be logged in to use this flag.

#### Inputs

None

#### Outputs

None

### Save command

> Save example commands:

```
redfish > save --selector=Bios. -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated session keys are stored in plaintext
Saving configuration...
Configuration saved to: redfish.json
```

> **Above:** Here, the server is logged into, Bios is selected, and the corresponding JSON file is saved to a local directory as the file redfish.json. The redfish.json file holds all the information regarding the selected type. Here, the save function was performed on the Bios type, so the redfish.json file that was saved holds the information about Bios. The file holding that information looks like the following. 

> **Below:** Example json file

```json
{
    "#Bios.v1_0_0.Bios": {
      "/redfish/v1/systems/1/bios/Settings/": {
        "Attributes": {
          "MemFastTraining": "Enabled", 
		  ...
          "TpmState": "NotPresent", 
          "CollabPowerControl": "Enabled"
        }
      }
    }
  }
```

```
redfish > save –u username –p password --url=xx.xx.xx.xx --selector=Bios. --filename=BiosInfo.json --logout
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
Saving configuration...
Configuration saved to: BiosInfo.json
```

> **Above:** Here, **Bios** is selected, and the corresponding JSON file is saved to a file called **BiosInfo.json** in a local directory. The attached --logout flag logs the user out after this command is completed.

#### Syntax

save *[Optional Parameters]*

#### Description

Saves the JSON information of a selected type to a local file. Use this command along with the `load` command when you want to modify properties of a selected type through file editing. Using this command saves a local copy of your selected type’s JSON information.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-f FILENAME, --filename=FILENAME**

Use this flag if you wish to use a different filename than the default one. The default filename is `redfish.json`.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--includelogs**

Optionally choose to set the **includelogs** flag. Doing so will include logs in the data retrieval process.

- **--selector=SELECTOR**

Include the selector flag to select a type to run the current command on. Use this flag when you wish to select a type without entering another command, or if you wish to work with a type that is different from the one you currently have selected.

- **--filter [FILTER_ATTRIBUTE=FILTER_VALUE]**

Optionally set a filter value for a filter attribute. This uses the provided filter for the currently selected type.

<aside class="notice"> Use this flag to narrow down your results. For example, selecting a common type might return multiple objects that are all of that type. If you want to modify the properties of only one of those objects, use the filter flag to narrow down results based on properties.</aside>

- **-j, --json**

Optionally include this flag if you wish to change the displayed output to JSON format. Preserving the JSON data structure makes the information easier to read.

- **--path=PATH**

Optionally set a starting point for data collection. If you do not specify a starting point, the default path will be` /redfish/v1/`.

<aside class="notice"> The <b>path</b> flag can only be specified at the time of login, so if you are already logged in to the server, the <b>path</b> flag will not change the path. If you are entering a command that isn’t the login command, but include your login information, you can still specify the <b>path</b> flag there.</aside>

- **--logout**

Optionally include the logout flag to log out of the server after this command is completed. You need to be logged in to use this flag.

#### Inputs

None

#### Outputs

JSON file

### Load command

> Load example commands:

```
redfish > load -m mpfilename.txt -f output.json
Loading configuration for multiple servers...
Logging session out.
Checking given server information...
Create multiple processes to load configuration concurrently to all servers...
Loading Configuration for 10.0.0.100 : SUCCESS
```

> **Above:** This is the multi-server configuration setup. You must pass in a multi-server file in the following format:

```
--url https://10.0.0.100 -u admin -p password
--url https://10.0.0.101 -u admin -p password
--url https://10.0.0.102 -u admin -p password
--url https://10.0.0.103 -u admin -p password
```

> **Above:** All servers are configured concurrently. Because the filename tag is included, it searches for the file called **output.json** and loads that information to the servers by setting any property values that have changed. If no values have changed, the load process is complete. If any property values have changed, the changes are committed and the user is logged out of the server. Logs of the entire process are then stored in the same location as the redfish logs.

```
redfish > load -u username -p password --url=xx.xx.xx.xx
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
Loading configuration...
Committing changes...
One or more properties were changed and will not take effect until system is reset.
Logging session out.
```

> **Above:** The load command entered here first logs into the server using the given information. Then, since no file was specified for it to load, it searches for the file called **redfish.json** and loads that information to the server by setting any property values that have changed. If no values have changed, it is finished. Otherwise, it commits the changes and logs the user out of the server. Here there have been changes made, so the after changing property values the changes are committed and the server logged out of.

```
redfish > load -u username -p password --url=xx.xx.xx.xx --filename=biosconfig.json
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
Loading configuration...
Error: No differences found from current configuration.
```

> **Above:** The load command entered here first logs into the server using the given information. Since the filename tag has been included, it searches for the file called **biosconfig.json** and loads that information to the server by setting any property values that have changed. If no values have changed, it is finished. Otherwise, it commits the changes. Here all the properties specified in **biosconfig.json** are the same as the values on the server, so the command is finished executing.

#### Syntax

load *[Optional Parameters]*

#### Description

Loads the server configuration from a file. Run this command without parameters to use the configuration found in the file called `redfish.json`. Otherwise, you can point this command to use any file you specify. Use this function to change the properties of a type to new values. This command uploads the new values of the type’s properties to the server.

<aside class="warning">When you try to load a file make sure to remove all read only properties. If any properties fail to patch the Redfish Utility will return an error.</aside>

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-f FILENAME, --filename=FILENAME**

Use this flag if you wish to use a different filename than the default one. The default filename is `redfish.json`.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--logout**

Optionally include the logout flag to log out of the server after this command is completed. You need to be logged in to use this flag.

- **-m MPFILENAME, --multiprocessing=MPFILENAME**

Use the provided filename to obtain data.

- **-o OFILENAME, --outputfilename=OFILENAME**

Use the provided filename to output data.

#### Inputs

JSON Object

Input a JSON object to load from a custom configuration file, otherwise the configuration will default to looking for a file called `redfish.json`.

#### Outputs

None

### Status command

> Status example commands:

```
redfish > select ComputerSystem. -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > set AssetTag=NewAssetTag
redfish > select Bios.
redfish > set Attributes/AdminName=NewAdminName
redfish > status
Current changes found:
#ComputerSystem.v1_2_0.ComputerSystem
        AssetTag=NewAssetTag
#Bios.v1_0_0.Bios
        Attributes/AdminName=NewAdminName
```

> **Above:** The status command shows changes to be committed. Here we see that the **AssetTag** property of **ComputerSystem** has been set to **NewAssetTag**, and that the **AdminName** property of **Bios** has been set to **NewAdminName**. The status command shows all pending changes, including changes for different types.

#### Syntax

status *[Optional Parameters]*

#### Description

Displays all pending changes. All pending changes will be displayed, regardless of which type is currently selected. Unless you have already committed your changes using the `–commit` flag, changes you make to properties will be queued. Use the `status` command to see all the changes that have not been committed yet.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

#### Inputs

None

#### Outputs

None

### Commit command

> Commit example commands:

```
redfish > select Bios. -u username -p password --url=xx.xx.xx.xx
Discovering data................................................................
...................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > set Attributes/AdminName=GeneKranz
redfish > commit
Committing changes...
The operation completed successfully.
```

> **Above:** Once you have made changes and are ready for them to take effect, use the commit command to commit your changes. Here the commit command saves the **AdminName** property of **Bios.** to the new value of **GeneKranz**. The commit command always logs out of the server.

```
redfish > login xx.xx.xx.xx -u username -p password
Discovering data...............................................................
..................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select Bios.
redfish > set "Attributes/AdminName=ExampleName"
redfish > set "Attributes/AdminEmail=person@place.com"
redfish > set "Attributes/AdminPhone=888-888-8888"
redfish > status
Current changes found:
#Bios.v1_0_0.Bios
        Attributes/AdminName=ExampleName
        Attributes/AdminEmail=person@place.com
        Attributes/AdminPhone=888-888-8888
redfish > commit
Committing changes...
The operation completed successfully.
```

> **Above:** The commit command applies all changes found by the status command.



#### Syntax

commit *[Optional Parameters]*

#### Description

Applies all changes made during the current session and then executes the `logout` command. After you have changed one or more values for the property of a type, you need to commit those changes in order for those changes to be reflected on the server. Use the `commit` command to do this. Once you have run the `commit` command, you will automatically be logged out of the server.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

#### Inputs

None

#### Outputs

None

### Logout command

> Logout example commands:

```
redfish > login xx.xx.xx.xx -u username -p password 
Discovering data................................................................
..................................Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > logout
Logging session out.
```

> **Above:** Use the logout command to end the session and disconnect from the server.

```
redfish > login xx.xx.xx.xx -u username -p password
Discovering data................................................................
..................................Done
WARNING: Cache is activated. Session keys are stored in plaintext.
redfish > select Bios.
redfish > set Attributes/AdminName=NewAdminName --logout
```

> **Above:** Here the logout flag was used to demonstrate that the server can be logged out of after another command. Here, after the **AdminName** property of **Bios** was set to a new value, the server was logged out of because the logout flag was included. The changes were not committed.

#### Syntax

logout *[Optional Parameters]*

#### Description

Use the `logout` command to exit your session and to disconnect from the server.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

#### Inputs

None

#### Outputs

None

### Exit command

> Exit example commands

```
redfish > login xx.xx.xx.xx -u username -p password 
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
redfish > logout
Logging session out.
redfish > exit
Bye for now
```

> **Above:** This command exits the interactive shell.

#### Syntax

exit *[Optional Parameters]*

#### Description

Use the `exit` command if you wish to exit from the interactive shell. Using exit will also log you out and disconnect you from the server.

#### Parameters

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

#### Inputs

None

#### Outputs

None