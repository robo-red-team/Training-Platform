#From mathias kali image
FROM kalilinux/kali-rolling:latest
RUN apt-get -y install nmap python3 python3-pip zip unzip
WORKDIR /working
RUN pip3 install flask flask_restful
COPY machines.zip /
RUN unzip machines.zip
EXPOSE 8855
ENTRYPOINT ["python3"]
CMD ["attackerAPI.py"]