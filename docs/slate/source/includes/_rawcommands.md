## Raw commands

These are the raw HTTP RESTful operations that can be used through the Redfish Utility. The commands and their examples that can be found in this section include the equivalents of HTTP RESTful **PATCH, GET, POST, PUT, DELETE**, and **HEAD**.

### RawPatch command

> RawPatch example commands:

```
redfish > get Attributes/AdminName –u username –p password --url=xx.xx.xx.xx –-selector=Bios.
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
Attributes=
            AdminName=""
redfish > rawpatch patch.json
One or more properties were changed and will not take effect until system is reset.
redfish > logout
Logging session out.
redfish > get Attributes/AdminName --selector=Bios. -u username -p password --url=xx.xx.xx.xx
Discovering data...Done
WARNING: Cache is activated session keys are stored in plaintext
AdminName=John Doe
```

> The following **patch.json** file was used in the above example:

```json
{
    "path": "/redfish/v1/systems/1/bios/Settings",
    "body": {
        "AdminName": "John Doe"
    }
}
```

> **Above:** Here, the **AdminName** of type **Bios** was "" before. The rawpatch command sent the patch.json to change that property to become **John Doe**. Commit is left out deliberately here since, raw commands (such as rawpost, rawput, etc.) do not require the commit command to be run since changes are made directly.



#### Syntax

rawpatch *[Filename] [Optional Parameters]*

#### Description

Use this command to perform an HTTP RESTful Patch command. Run to send a patch from the data in the input file.

#### Parameters

> Filename parameter example:

```json
{
	"path": "/redfish/v1/systems/1/bios/Settings",
	"body": {
		"AdminName": "John Doe"
	}
}
```

- **Filename**

Include the filename to use the data in the input file to send the patch. See the example JSON file that can be used to rawpatch on the side.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

- **--response**

Use this flag to return the response body.

- **--getheaders**

Use this flag to return the response headers.

- **--headers=HEADERS**

Use this flag to add extra headers to the request. Usage: --headers=HEADER:VALUE,HEADER:VALUE

#### Inputs

File

Input the file containing the JSON information you wish to use for the HTTP RESTful PATCH command.

#### Outputs

None

### RawGet command

> RawGet example commands:

```
redfish > rawget "/redfish/v1/systems/1/bios/settings" -u username -p password --url=16.83.62.220
The operation completed successfully.
{
  "@odata.type": "#Bios.v1_0_0.Bios",
  "Attributes": {
    "MemFastTraining": "Enabled",
	...
    "TpmState": "NotPresent",
    "CollabPowerControl": "Enabled"
  },
  "Description": "Platform/BIOS Configuration (RBSU) Pending Settings",
  "@odata.context": "/redfish/v1/$metadata#Bios.Bios",
  "Name": "BIOS Configuration Pending Settings"
}
```

> **Above:** The rawget command here executed the GET command on the path **/redfish/v1/systems/1/bios/settings**. This displays the information in the given path. Note that the full list of information has been truncated here for space.

```
redfish > rawget "/redfish/v1/systems/1/bios/settings" –u username –p password --url=xx.xx.xx.xx --filename=output.json
The operation completed successfully.
Results written out to 'output.json'.
```

#### Syntax

rawget *[Path] [Optional Parameters]*

#### Description

Use this command to perform an HTTP RESTful GET command. Run to retrieve data from the passed in path.

#### Parameters

- **Path**

Pass the path to the `rawget` command to point it at a location.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

- **--response**

Use this flag to return the response body.

- **--getheaders**

Use this flag to return the response headers.

- **--headers=HEADERS**

Use this flag to add extra headers to the request. Usage: --headers=HEADER:VALUE,HEADER:VALUE

- **-f FILENAME, --filename=FILENAME**

Write results to the specified file.

- **-b FILENAME, --writebin=FILENAME**

Write the results to the specified file in binary.

#### Inputs

None

#### Outputs

File

If you include the `filename` flag, this command will return an output file of the information retrieved when the `rawget` command was executed.

### RawPost command

> RawPost example commands:

```
resfish > rawpost forcerestart.json -u username -p password --url=xx.xx.xx.xx
The operation completed successfully.
```

> The following **forcerestart.json** file is used in conjuncture:

```json
        {
            "path": "/redfish/v1/systems/1/Actions/ComputerSystem.Reset",
            "body": {
                "ResetType": "ForceRestart"
            }
        }
```

> **Above:** The rawpost command performs an HTTP REST POST operation using the information provided in the provided file. Here the ForceRestart ResetType was set, so after the rawpost posted the changes the server executed a ForceRestart. Note that if a full path is not given, the utility will search for the file in the location the Redfish Utility is started in.

#### Syntax

rawpost *[Filename] [Optional Parameters]*

#### Description

Use this command to perform an HTTP RESTful POST command. Run to post the data from the passed in path.

#### Parameters

> Example Filename parameter JSON file below:

```json
        {
            "path": "/redfish/v1/systems/(system ID)/Actions/ComputerSystem.Reset",
            "body": {
                "ResetType": "ForceRestart"
            }
        }
```

- **Filename**

Include the filename to send a post from the data included in this input file. An example JSON file is shown on the side:

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

- **--response**

Use this flag to return the response body.

- **--getheaders**

Use this flag to return the response headers.

- **--headers=HEADERS**

Use this flag to add extra headers to the request. Usage: --headers=HEADER:VALUE,HEADER:VALUE

#### Inputs

File

Input the file containing the JSON information you wish to use for the HTTP RESTful PUT command.

#### Outputs

None

### RawPut command

> RawPut example commands:

```
redfish > rawput put.json –u username –p password –-url=xx.xx.xx.xx
One or more properties were changed and will not take effect until system is reset.
```

> This example uses the following **put.json** file:

```
{
    "path": "/redfish/v1/systems/1/bios/settings/",
    "body":{
        "BaseConfig": "default"
    }
}
```

> **Above:** Here the rawput command was used to put the above put.json file to the server.

#### Syntax

rawput *[Filename] [Optional Parameters]*

#### Description

Use this command to perform an HTTP RESTful PUT command. Run to retrieve data from the passed in path.

#### Parameters

> Example input file below:

```json
{	
    "path": "/redfish/v1/systems/1/bios/settings/",
    "body":{	
        "BaseConfig": "default"
    }
}
```

- **Filename**

Include the filename to send a PUT from the data included in this input file. Example Input file shown on the side:

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

- **--response**

Use this flag to return the response body.

- **--getheaders**

Use this flag to return the response headers.

- **--headers=HEADERS**

Use this flag to add extra headers to the request. Usage: --headers=HEADER:VALUE,HEADER:VALUE

#### Inputs

File

Input the file containing the JSON information you wish to use for the HTTP RESTful PUT command.

#### Outputs

None

### RawDelete command

> RawDelete example commands:

```
redfish > login xx.xx.xx.xx –u username –p password
redfish > rawdelete "/redfish/v1/Sessions/admin556dba8328b43959/"
The operation completed successfully.
```

> **Above:** Here the rawdelete command was used to delete a session. After the server was logged into, the provided session was deleted.

#### Syntax

rawdelete *[Path] [Optional Parameters]*

#### Description

Use this command to perform an HTTP RESTful DELETE command. Run to delete data from the passed in path.

#### Parameters

- **Path**

Pass in the path to point the HTTP RESTful DELETE command.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

- **--response**

Use this flag to return the response body.

- **--getheaders**

Use this flag to return the response headers.

- **--headers=HEADERS**

Use this flag to add extra headers to the request. Usage: --headers=HEADER:VALUE,HEADER:VALUE

#### Inputs

None

#### Outputs

None

### RawHead command

> RawHead example commands:

```
redfish > rawhead /redfish/v1/systems/1/bios/settings -u username -p password --url=xx.xx.xx.xx
The operation completed successfully.
{
  "Content-Length": "0",
  "Connection": "keep-alive",
  "ETag": "9E59E654",
  "Allow": "GET, HEAD, POST, PUT, PATCH",
  "Date": "Sat, 22 Oct 2016 09:32:49 GMT",
  "OData-Version": "4.0",
  "X-Frame-Options": "sameorigin"
}
```

> **Above:** The rawhead command is the HTTP RESTful HEAD operation. It is used to retrieve the data from the passed in path.

#### Syntax

rawhead [Path] [Optional Parameters]

#### Description

Use this command to perform an HTTP RESTful HEAD command. Run to retrieve header data from the passed in path.

#### Syntax

- **Path**

Pass in the path to point the HTTP RESTful HEAD command.

- **-h, --help**

Including the help flag on this command will display help on the usage of this command.

- **-f, --filename=Filename**

Include the filename to perform the current operation.

- **-u User, --user=USER**

If you are not logged in yet, including this flag along with the password and URL flags can be used to log into a server in the same command.

- **-p Password, --password=PASSWORD**

If you are not logged in yet, use this flag along with the user and URL flags to login. Use the provided password corresponding to the username you gave to login.

- **--url=URL**

If you are not logged in yet, use the provided URL along with the user and password flags to login to the server in the same command.

- **--sessionid=SESSIONID**

Optionally include this flag if you would prefer to connect using a session id instead of a normal login.

- **--silent**

Use this flag to silence responses.

#### Inputs

None

#### Outputs

File

If you specify the `filename` flag, the `rawhead` command will output a file containing the information retrieved when performing the `rawhead` command.


