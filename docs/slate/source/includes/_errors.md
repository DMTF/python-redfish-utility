# Error Codes

<aside class="notice">The error codes listed below are returned by the Redfish Utility, not the managed server.</aside>

The Redfish Utility uses the following error codes:

Error Code | Description
---------- | -------
1	| Error occurred while reading the configuration file. See the error message for details.
2	| Error occurred when user tried to invoke a command that isn't enabled.
3	| Invalid command line syntax. Use the **-h** parameter for complete command line parameters.
4	| The input JSON file is in an invalid format.
5	| Windows User not admin.
6	| No contents found for operation.
7	| Invalid File input error.
8	| No changes made or found.
9	| No Valid info error.
10	| Error occurred while parsing user command line inputs. See the error message for details.
11	| Warning occurred during command line inputs parsing. See the error message for details.
12	| Invalid individual command usage. Use the **-h** parameter for individual command line parameters.
13	| Error occurred when user tries to invoke a command that doesn’t exist.
21	| Occurs when there are no clients active (usually when user hasn't logged in).
22	| Error occurred when attempting to operate on another instance while logged in.
23	| Error occurred when attempting to select an instance that does not exist.
24	| Error occurred when attempting to access an object type without first selecting it.
25	| Error occurred when attempting to access an object type without first selecting it while using filters.
26	| Error occurred when attempting to set an object type without first selecting it.
27	| Error occurred when selection argument fails to match anything.
28	| Error occurred when validating user input against schema files.
30	| RIS session expired.
31	| Error occurred when retry attempts to reach the selected server have been exhausted.
32	| Occurs when invalid credentials have been provided.
33	| Error occurred when correct credentials have been provided and server is unresponsive.
36	| Error occurred due to an unexpected response.
40	| Same settings error.
44	| No current session established.
45	| Failure during commit operation
51	| Multiple server configuration failure
52	| Multiple server input file error.
53	| Load skip setting error.
61	| Error occurred when trying to change a value.
62  | The requested path was not found.
255	| A general error occurred while manipulating server settings. See the error message for details
