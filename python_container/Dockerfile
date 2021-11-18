# Copyright (c) 2021 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#               https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.


FROM python:latest
WORKDIR /app
RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get install -y curl nano git cron
COPY ./scripts /scripts
COPY ./requirements.txt /app
COPY ./entrypoint.sh /app
COPY ./crontab.txt /app
RUN chmod 0644 /app/crontab.txt
RUN pip install -r requirements.txt
RUN crontab /app/crontab.txt
RUN chmod 777 /app/entrypoint.sh
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
WORKDIR /scripts
CMD ["/app/entrypoint.sh"]
