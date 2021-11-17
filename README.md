# merakiDeviceReboot
Script to reboot Meraki devices.  Devices are list by serial numbers in a CSV file, and the results of the reboots are posted to a WebEx Room.

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
