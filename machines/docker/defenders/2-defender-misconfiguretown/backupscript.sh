#!/bin/bash
rm /var/www/public/backups/*
BACKUPTIME=`date +%b-%d-%y` 
DESTINATION=/var/www/public/backups/important-$BACKUPTIME.tar.gz #create a backup file using the current date in it's name
SOURCEFOLDERONE=/etc/shadow
SOURCEFOLDERTWO=/var/www/public

tar -czf $DESTINATION $SOURCEFOLDERONE $SOURCEFOLDERTWO --exclude=$SOURCEFOLDERTWO/backups  #create the backup