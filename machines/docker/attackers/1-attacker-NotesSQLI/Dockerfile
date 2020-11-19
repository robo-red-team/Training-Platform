#From mathias kali image
FROM kalilinux/kali-rolling:latest
RUN apt update
RUN apt-get -y install nmap python3 python3-pip
WORKDIR /working
RUN pip3 install flask flask_restful
COPY notes_pwn.py notes_pwn.py
COPY exploit.sh exploit.sh
EXPOSE 8855
ENTRYPOINT ["python3"]
CMD ["attackerAPI.py"]