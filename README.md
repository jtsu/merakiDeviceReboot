# merakiDeviceReboot
Python script to reboot Meraki devices.  Devices are list by serial number in a CSV file, and the results of the reboots are posted to a WebEx Room.


## Requirements
* Python3
* Meraki SDK for Python
  * Meraki API/SDK Info: https://developer.cisco.com/meraki/api-v1/
  * Meraki SDK on GitHub: https://github.com/meraki/dashboard-api-python/
* WebEx Teams SDK for Python
  * WebExTeams SDK on GitHub: https://github.com/CiscoDevNet/webexteamssdk


## Configuration
* Edit tokens.py with required info:
  * API_KEY = "Your_Meraki_API_Key"
  * ORG_ID = "Your_Meraki_ORG_ID"
  * WEBEX_TOKEN = "Your_WebEx_Token"
  * WEBEX_ROOMID = "Your_WebEx_Room_ID"

* Add serial numbers of devices in apSerials.csv.  
  * Values should be comma separate.


## Running the Script
* run: 'python3 rebootDevices.py'


## Python Docker Container
* If you need a python environment with the required libraries and applications, files to build a docker container have been posted to the python_container folder.
* Copy the 3 script related files to the 'scripts' sub-directory before building your container.
  * rebootDevices.py
  * tokens.py
  * apSerials.csv 
* The dockerfile changes the working directory to the 'scripts' directory.
* A cron job will run the reboot script located in the 'scripts' directory.
  * Known issue: Cron not running when configured via dockerfile.
  * Workaround: entrypoint.sh script starting cron.


## Additional Information
* Get your Meraki API Key:
  * https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API
* API to get Meraki ORG ID:
  * https://developer.cisco.com/meraki/api-v1/#!get-organizations
* WebEx Access Tokens and Integrations/Bots:
  * https://developer.webex.com/docs/getting-started#accounts-and-authentication
  * https://developer.webex.com/docs/integrations
* WebEx Messaging Rooms API:
  * https://developer.webex.com/docs/api/v1/rooms
