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
bash buildDockers.sh

#Setup apt on our servet
echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list

printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable
apt-get update
apt-get install linux-headers-$(uname -r|sed 's/[^-]*-[^-]*-//')
# Setup Wireguard
apt-get install wireguard
wg genkey | tee /etc/wireguard/wg-private.key | wg pubkey > /etc/wireguard/wg-public.key
sudo nano /etc/wireguard/wg0.conf

printf '[Interface]
PrivateKey = 0OCZoWrdeSsCCuNnYoLrhCcZ2nd9Fmcf9ABfOfMVnGo= # The server_private.key value.
Address = 10.0.0.1/24 # Internal IP address of the VPN server.
ListenPort = 56 # Previously, we opened this port to listen for incoming connections in the firewall.
# Change "enp0s5" to the name of your network interface in the following two settings. This commands configures iptables for WireGuard.
#iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp0s31f6 -j SNAT --to-source 1.2.3.4
#iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp0s31f6 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp0s31f6 -j MASQUERADE

# Configurations for the clients. You need to add a [Peer] section for each VPN client.
[Peer]
PublicKey = nreKUqhW3oQZtswhNd246s2gG8HRFoIsM7isGZinC0o= # client_public.key value.
AllowedIPs = 10.0.0.2/32, 10.0.0.2/24 # Internal IP address of the VPN client.
' > /etc/wireguard/wg0.conf
