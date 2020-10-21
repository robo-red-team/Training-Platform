#!/bin/bash
echo -e "\n-==INSTALL FOR ROBO RED TEAM TRAINING PLATFORM==-\n"
# Python dependencies
pip install flask flask_restful docker
# Docker dependencies
echo -e "\nPlase manually build the desired docker images\nYou can find them in ./machines/docker/*\n"
# OS dependencies 
echo -e "\nPlease make sure your system has: python, python-pip, docker\n"