# Training-Platform
Training platform for the Robo-Red-Team project.

## How to run:
To run this, you need to be on a Linux-based system. First run:
```
bash install.sh
```
This will install the Python dependencies, and tell you which things you need to do manually *(Due to differences in Linux distribution package manegers)*

Once you have installed the needed packages, then you can start the service with:
```
python3 controller.py
```
*Note: You might have to run as root (sudo), in case Docker needs these priviliges.*
