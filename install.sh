#!/bin/bash
echo -e "\n-==INSTALL FOR ROBO RED TEAM TRAINING PLATFORM==-\n"

# Dependencies
packages="python vagrant"
pythonDependencies="flask flask_restful flask_cors docker python-vagrant"
systemctlStart="docker" 


# Build all docker instances
BuildDocker() {
    bash buildDockers.sh
}

# Common things for pacman- and apt based systems
CommonSetup() {
    systemctl enable $systemctlStart
    systemctl start $systemctlStart
    BuildDocker
}

# Installation of needed packages
if [ "$1" == "pacman" ]; then
    pacman -S $packages docker python-pip
    pip install $pythonDependencies
    CommonSetup
    echo -e "\nRemember to install WireGuard\n"
elif [ "$1" == "apt" ]; then
    apt update
    apt install $packages docker.io python3-pip
    pip3 install $pythonDependencies
    CommonSetup
    systemctl enable "wg-quick@wg0"
    bash wireGuard.sh
else
    BuildDocker
    echo -e "\n======================\n---Manually install---\n======================\nPlease manually install: $packages WireGuard [docker/docker.io] [pip for python3]\nand these Python libaries: $pythonDependencies\nOr run the script with 'pacman' or 'apt' as param.\n"
fi