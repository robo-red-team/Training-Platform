#!/bin/bash
# Print name
echo -e "███████████████████████████████████████████████████████████████████████\n█▄─▄▄▀█─▄▄─█▄─▄─▀█─▄▄─███▄─▄▄▀█▄─▄▄─█▄─▄▄▀███─▄─▄─█▄─▄▄─██▀▄─██▄─▀█▀─▄█\n██─▄─▄█─██─██─▄─▀█─██─████─▄─▄██─▄█▀██─██─█████─████─▄█▀██─▀─███─█▄█─██\n▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▀▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀\n"

#Start front- and backend server, as subprocesses
$(python3 ./frontend/tempFlaskServer.py 80) & $(python3 ./backend/backendServer.py 8855) 