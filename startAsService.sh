#!/bin/bash
cp roboRedTeam.service /etc/systemd/system/
systemctl start roboRedTeam.service
systemctl enable roboRedTeam.service
