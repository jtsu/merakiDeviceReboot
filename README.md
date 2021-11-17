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
* Edit tokens.py with your details.
* Add serial numbers of devices in apSerials.csv.  
  * Values should be comma separate.

## Running the script
* run: 'python3 rebootDevices.py'
