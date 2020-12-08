#!/bin/sh
rm machines.zip
zip machines.zip 1-defender-notessqli/ 2-defender-ftplime/ -r 
docker build -t dockerattacker .
