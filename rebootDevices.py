#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
import meraki
from webexteamssdk import WebexTeamsAPI
import time
import tokens
import csv

dashboard = meraki.DashboardAPI(tokens.API_KEY, suppress_logging=True)
delay = 2

# Read values from the CSV file.
def readCsvFile():
    with open('apSerials.csv', 'r') as file:
        read = csv.reader(file)
        csvRows = []
        for row in read:
            csvRows.append(row)
    return (csvRows)


# Function to reboot each device by its serial number, and returning a list of
# device serial numbers and its reboot status.
def rebootDevice(deviceSerialNumbers):
    rebootStatus = []

    if len(deviceSerialNumbers) != 0:
        for item in deviceSerialNumbers:
            try:
                reboot = dashboard.devices.rebootDevice(serial=item)
                rebootStatus.append({"serial": item, "status": reboot})
                time.sleep(delay)
            except:
                print(f"Exception error: {item} -Check SDK Logs. Continuing.")
                continue
    # Return list of serial and status of the reboot trigger
    return(rebootStatus)


# Function to create a summary status of the reboot results.
# We're counting the number of device reboot success and fails, and returning
# the final count and a list of devices that failed to trigger a reboot.
def rebootStatus(rebootResults):
    passCount = 0
    failCount = 0
    results = []
    apFailList = []

    for item in rebootResults:
        if item["status"]["success"] is True:
            passCount += 1
        else:
            failCount += 1
            apFailList.append(item["serial"])

    results.append({"apRebooted": passCount, "apNotRebooted": failCount, "apFailList": apFailList})
    print(results)
    return (results)


# Function to post the final status results to a WebEx Room.
def postWebex(rebootStatus):
    webex = WebexTeamsAPI(access_token=tokens.WEBEX_TOKEN)

    # Post the rebootStatus to the webex room
    webex.messages.create(tokens.WEBEX_ROOMID, markdown=json.dumps(rebootStatus))
    print("Reboot status results posted to Webex room.")


if __name__ == '__main__':

    # Get list of device serial numbers to reboot from CSV file.
    rows = readCsvFile()
    deviceSerialNumbers = []
    for row in range(len(rows)):
        # nested loops in case of multiple rows in CSV file
        for serial in rows[row]:
            deviceSerialNumbers.append(serial)

    print("Starting reboot script.  It may take several minutes to complete.")
    rebootAP = rebootDevice(deviceSerialNumbers)
    status = rebootStatus(rebootAP)
    postWebex(status)
