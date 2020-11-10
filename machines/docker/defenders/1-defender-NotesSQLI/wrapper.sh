#!/bin/sh

$(python3 /var/www/MySecretNotes/app.py 80) & $(/usr/sbin/sshd -D)