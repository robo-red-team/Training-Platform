#!/bin/bash
echo -e "\n-==INSTALL FOR ROBO RED TEAM TRAINING PLATFORM==-\n"

# Dependencies
packages="python python-pip docker vagrant"
pythonDependencies="flask flask_restful flask_cors docker python-vagrant"
systemctlStart="docker" 

# Common things for pacman- and apt based systems
CommonSetup() {
    pip install $pythonDependencies
    systemctl enable $systemctlStart
    systemctl start $systemctlStart
}

# Installation of needed packages
if [ "$1" == "pacman" ]; then
    pacman -S $packages
    CommonSetup
elif [ "$1" == "apt" ]; then
    apt update
    apt install $packages
    CommonSetup
else
    echo -e "Please manually install: $packages\nand these Python libaries: $pythonDependencies\nOr run the script with 'pacman' or 'apt' as param."
fi

# Docker build
echo -e "\nPlase manually build the desired docker images\nYou can find them in ./machines/docker/*\nAnd in ./backend/microServices/*\n"