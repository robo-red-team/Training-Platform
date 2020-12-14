FROM ubuntu:16.04

RUN apt-get update

# Install apache, PHP, and supplimentary programs. curl and lynx-cur are for debugging the container.
RUN apt-get -y install apache2 \
php7.0 \
libapache2-mod-php7.0 \
cron \
nano

#
RUN a2enmod php7.0
RUN a2enmod rewrite

#make needed dirs
RUN mkdir /var/www/public
RUN mkdir /var/www/public/backups
RUN mkdir /var/www/public/uploads

#Copy stuff over
COPY upload.php /var/www/public
COPY index.html /var/www/public
COPY wrapper.sh /root


## Cron backup script
COPY backupscript.sh /root
RUN echo "*/1 * * * * /bin/sh /root/backupscript.sh" >> /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
RUN touch /var/log/cron.log



# Manually set up the apache environment variables
ENV APACHE_RUN_USER root
ENV APACHE_RUN_GROUP root
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

VOLUME ["/var/www", "/etc/apache2/sites-enabled"]
ADD apache-config.conf /etc/apache2/sites-enabled/000-default.conf
###

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd

RUN echo 'root:root' |chpasswd

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh
###

#make www-data own the folder

EXPOSE 22
EXPOSE 80


ENTRYPOINT ["sh","/root/wrapper.sh"]