# Training-Platform
Training platform for the Robo-Red-Team project.

## How to run:
To run this, you need to be on a Linux-based system. First run:
```
bash install.sh [pacman/apt]
```
This will install the needed packages and Python dependencies. There is suport for 'pacman' and 'apt', if no param is given, then it will tell which packages to install.

Once you have installed the needed packages, then you can start the service with:
```
bash start.sh [API key]
```
*Note: You might have to run as root (sudo), in case Docker needs these priviliges.*
