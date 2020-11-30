#!/bin/sh

echo root:$1 |chpasswd
$(python3 /var/www/MySecretNotes/app.py 80) & $(/usr/sbin/sshd -D)
