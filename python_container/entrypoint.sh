#!/bin/bash

# Copyright (c) 2020 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#
#                https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.
#

echo
/bin/date
echo
echo "Starting cron..."
/usr/sbin/cron start >> /app/start.log 2>&1
echo "Check processes..."
/bin/ps -aux
echo
echo "check cron jobs..."
/usr/bin/crontab -l
echo
echo "Tailing start.log"
tail -f /app/start.log
