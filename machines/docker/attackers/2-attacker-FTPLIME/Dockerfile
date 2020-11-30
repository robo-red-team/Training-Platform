#From mathias kali image
FROM kalilinux/kali-rolling:latest
RUN apt update
RUN apt-get -y install nmap python3 
WORKDIR /working
COPY exploit.c exploit.c
COPY lime_pwn.py lime_pwn.py
COPY exploit.sh exploit.sh
CMD ["./exploit.sh $IP $TIMEOUT"]