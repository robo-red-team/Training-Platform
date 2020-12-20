#!/bin/sh
rm machines.zip
zip machines.zip 1-defender-notessqli/ 2-defender-misconfiguretown/ -r 
docker build -t dockerattacker .
