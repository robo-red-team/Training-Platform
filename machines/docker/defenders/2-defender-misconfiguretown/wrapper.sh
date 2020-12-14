#!/bin/sh

echo root:$1 |chpasswd
chown -R www-data:www-data /var/www/public
cron
/usr/sbin/sshd
/usr/sbin/apache2ctl -D FOREGROUND
