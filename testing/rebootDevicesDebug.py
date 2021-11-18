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
import tokensJason as tokens
import csv

dashboard = meraki.DashboardAPI(tokens.API_KEY, suppress_logging=True)
delay = 2

# Read values from the CSV file.
def readCsvFile():
    startTime = time.perf_counter()

    with open('apSerials.csv', 'r') as file:
        read = csv.reader(file)
        csvRows = []
        for row in read:
            csvRows.append(row)

    stopTime = time.perf_counter()
    print(f"readCsvFile completed in {stopTime-startTime}")

    return (csvRows)


# Function to reboot each device by its serial number, and returning a list of
# device serial numbers and its reboot status.
def rebootDevice(deviceSerialNumbers):
    startTime = time.perf_counter()
    rebootStatus = []

    if len(deviceSerialNumbers) != 0:
        for item in deviceSerialNumbers:
            loopStart = time.perf_counter()
            try:
                reboot = dashboard.devices.rebootDevice(serial=item)
                rebootStatus.append({"serial": item, "status": reboot})
                time.sleep(delay)
            except:
                print(f"Exception error: {item} -Check SDK Logs. Continuing.")
                continue
            loopStop = time.perf_counter()
            print(f"Iteration for an AP reboot completed in {loopStop-loopStart} secs.")


    stopTime = time.perf_counter()
    print(f"rebootDevice function completed in {stopTime-startTime} secs.")

    # Return list of serial and status of the reboot trigger
    return(rebootStatus)


# get all devices in ORG and reboot them all
def getAllDevices():
    startTime = time.perf_counter()
    rebootStatus = []
    apCount = 0
    model = "MR42"
    productType = "wireless"

    response = dashboard.organizations.getOrganizationDevices(tokens.ORG_ID, total_pages='all')
    getOrgDeviceTime = time.perf_counter()
    print(f"Get all devices for reboot completed in {getOrgDeviceTime-startTime} secs.")

    for device in response:
        loopStart = time.perf_counter()
        if model in device['model']:
            try:
                print(f"{device['serial']}, {device['name']}, {device['model']}")
                apCount += 1
                #reboot = dashboard.devices.rebootDevice(serial=device['serial'])
                #rebootStatus.append({"serial": device['serial'], "status": reboot})
                #time.sleep(delay)
            except:
                print(f"Exception error: {device['serial']} -Check SDK Logs. Continuing.")
                continue
            loopStop = time.perf_counter()
            print(f"Iteration for an AP reboot completed in {loopStop-loopStart} secs.")
    print(apCount)
    stopTime = time.perf_counter()
    print(f"rebootDevice function completed in {stopTime-startTime} secs.")

    # Return list of serial and status of the reboot trigger
    return(rebootStatus)


# Function to create a summary status of the reboot results.
# We're counting the number of device reboot success and fails, and returning
# the final count and a list of devices that failed to trigger a reboot.
def rebootStatus(rebootResults):

    startTime = time.perf_counter()

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

    stopTime = time.perf_counter()
    print(f"rebootStatus completed in {stopTime-startTime} sec.")

    return (results)


# Function to post the final status results to a WebEx Room.
def postWebex(rebootStatus):

    startTime = time.perf_counter()

    webex = WebexTeamsAPI(access_token=tokens.WEBEX_TOKEN)

    # Post the rebootStatus to the webex room
    webex.messages.create(tokens.WEBEX_ROOMID, markdown=json.dumps(rebootStatus))
    print("Reboot status results posted to Webex room.")

    stopTime = time.perf_counter()
    print(f"postWebex completed in {stopTime-startTime} secs.")


if __name__ == '__main__':

    # Get list of device serial numbers to reboot from CSV file.
    startTime = time.perf_counter()

    rows = readCsvFile()
    deviceSerialNumbers = []
    for row in range(len(rows)):
        # nested loops in case of multiple rows in CSV file
        for serial in rows[row]:
            deviceSerialNumbers.append(serial)

    stopTime = time.perf_counter()
    print(f"Device list from CSV completed in {stopTime-startTime}")


    print("Starting reboot script.  It may take several minutes to complete.")
#    rebootAP = rebootDevice(deviceSerialNumbers)
#    status = rebootStatus(rebootAP)
#    postWebex(status)

getAllDevices()
