#!/bin/bash
if [ "$1" == "" ]
then
    echo -e "\n-===!ERROR!===-\nPlease enter an API key as the first parameter!\n"
else
    # Print name
    echo -e "███████████████████████████████████████████████████████████████████████\n█▄─▄▄▀█─▄▄─█▄─▄─▀█─▄▄─███▄─▄▄▀█▄─▄▄─█▄─▄▄▀███─▄─▄─█▄─▄▄─██▀▄─██▄─▀█▀─▄█\n██─▄─▄█─██─██─▄─▀█─██─████─▄─▄██─▄█▀██─██─█████─████─▄█▀██─▀─███─█▄█─██\n▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▀▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀\n"
    echo -e "▀█▀ █▀█ ▄▀█ █ █▄░█ █ █▄░█ █▀▀   █▀█ █░░ ▄▀█ ▀█▀ █▀▀ █▀█ █▀█ █▀▄▀█\n░█░ █▀▄ █▀█ █ █░▀█ █ █░▀█ █▄█   █▀▀ █▄▄ █▀█ ░█░ █▀░ █▄█ █▀▄ █░▀░█\n"

    # Generate SHA256 hash of API key
    apiKey=$(echo -n "$1RoboRedTeamNotSoSecretSalt" | sha256sum | awk '{print $1}' | tr -d "\n")

    #Start front- and backend server, as subprocesses
    $(python3 ./frontend/tempWebServer.py 80) & $(python3 ./backend/backendServer.py 8855 $apiKey)
fi 