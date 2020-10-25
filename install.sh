#!/bin/bash
echo -e "\n-==INSTALL FOR ROBO RED TEAM TRAINING PLATFORM==-\n"

packages="python python-pip docker"
pythonDependencies="flask flask_restful docker" 

# Installation of needed packages
if [ "$1" == "pacman" ]; then
    pacman -S $packages
    pip install $pythonDependencies
elif [ "$1" == "apt" ]; then
    apt install $packages
    pip install $pythonDependencies
else
    echo -e "Please manually install: $packages\nand these Python libaries: $pythonDependencies\nOr run the script with 'pacman' or 'apt' as param."
fi

# Docker build
echo -e "\nPlase manually build the desired docker images\nYou can find them in ./machines/docker/*\n"