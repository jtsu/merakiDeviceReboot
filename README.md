# merakiDeviceReboot
Script to reboot Meraki devices in an Org and posts the results to a WebEx room.

## Requirements
* Python3
* Meraki SDK
* WebEx Teams SDK

## Configuration
* Add serial numbers of devices to apSerials.csv.  
  * Values should be comma separate.
* Edit tokens.py with your details.

## Running the script
* run: 'python rebootDevices.py'
