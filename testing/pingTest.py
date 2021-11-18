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
pingResultsDelay = 60


def readCsvFile():
    with open('apSerials.csv', 'r') as file:
        read = csv.reader(file)
        csvRows = []
        for row in read:
            csvRows.append(row)
    return (csvRows)


def pingTest(deviceSerialNumbers):
    pingResults = []
    for serial in deviceSerialNumbers:
        print(f"Pinging {serial}")
        createPing = dashboard.devices.createDeviceLiveToolsPingDevice(serial)
        pingId = createPing['pingId']
        time.sleep(delay)
        pingResults.append({'serial': serial, 'pingId': pingId})
    return(pingResults)


def getPingResults(pingTest):
    pingResults = []
    for test in pingTest:
        print(f"Getting Ping Results for {test['serial']}")
        try:
            getPingResults = dashboard.devices.getDeviceLiveToolsPingDevice(test['serial'], test['pingId'])
            loss = (getPingResults['results']['loss']['percentage'])
            pingResults.append({'serial': test['serial'], 'loss': loss})
            print(f"{loss}")
            time.sleep(delay)
        except TypeError:
            print("TypeError in getPingResults: results = null?")
            pingResults.append({'serial': test['serial'], 'loss': 200})
            time.sleep(delay)
            continue
    return(pingResults)


def pingStatus(pingResults):
    passCount = 0
    failCount = 0
    results = []
    apFailList = []

    for item in pingResults:
        if item["loss"] == 0:
            passCount += 1
        else:
            failCount += 1
            apFailList.append(item["serial"])

    results.append({"pingPassed": passCount, "pingFailed": failCount, "apFailList": apFailList})
    print(results)
    return (results)


def postWebex(rebootStatus):
    # Using the Webex SDK. More info can be found here: https://webexteamssdk.readthedocs.io/en/latest/index.html
    webex = WebexTeamsAPI(access_token=tokens.WEBEX_TOKEN)

    # Post the status to the webex room
    webex.messages.create(tokens.WEBEX_ROOMID, markdown=json.dumps(rebootStatus))
    print("Ping results posted to Webex room.")


if __name__ == '__main__':

    # Get list of device serial numbers to reboot from CSV file.
    rows = readCsvFile()
    deviceSerialNumbers = []
    for row in range(len(rows)):
        # nested loops in case of multiple rows in CSV file
        for serial in rows[row]:
            deviceSerialNumbers.append(serial)

    print("Starting Ping Test.  It may take several minutes to complete.")
    ping = pingTest(deviceSerialNumbers)
    time.sleep(pingResultsDelay)
    results = getPingResults(ping)
    status = pingStatus(results)
    postWebex(status)
