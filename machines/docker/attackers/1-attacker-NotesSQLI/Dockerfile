#From mathias kali image
FROM kalilinux/kali-rolling:latest
RUN apt update && apt upgrade -y
RUN apt-get -y install nmap python3 
WORKDIR /working
COPY notes_pwn.py notes_pwn.py
COPY exploit.sh exploit.sh
CMD ["./exploit.sh $IP $TIMEOUT"]