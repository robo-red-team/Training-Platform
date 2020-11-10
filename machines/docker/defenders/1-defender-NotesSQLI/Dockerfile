FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install flask 
RUN apt-get install -y git
RUN mkdir /var/www

###

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd

RUN echo 'root:root' |chpasswd

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh
###


RUN git clone https://github.com/0xlimE/MySecretNotes.git /var/www/MySecretNotes
EXPOSE 80
EXPOSE 22

COPY wrapper.sh wrapper.sh
ENTRYPOINT ["sh","wrapper.sh"]
#CMD ./wrapper.sh