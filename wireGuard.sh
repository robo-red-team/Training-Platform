#Setup apt on our server
#echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list


#printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable
apt-get update
#apt-get install linux-headers-$(uname -r|sed 's/[^-]*-[^-]*-//')
# Setup Wireguard
apt-get install -y wireguard docker.io zip unzip
mkdir /etc/wireguard
umask 0077 /etc/wireguard
rm -r /etc/wireguard/*
rm -r backend/vpnBundles/*
mkdir backend
mkdir backend/vpnBundles
wg genkey | tee /etc/wireguard/wg-server_private.key | wg pubkey > /etc/wireguard/wg-server_public.key

privateKeyValue=$(cat /etc/wireguard/wg-server_private.key)
publicKeyValue=$(cat /etc/wireguard/wg-public_private.key)
location=$(pwd)"/backend/vpnBundles"
#Removes comment tag to allow ip forwarding
#server='net.ipv4.ip_forward=1'; sed -i "/^#$server/ c$server" /etc/sysctl.conf

#Sets IP forwarding to 1, to allow it
#echo 1 > /proc/sys/net/ipv4/ip_forward

#ethValue=$(ip -o -4 route show to default | awk '{print $5}')

#Sets the wg0.conf file with server values
echo "[Interface]
PrivateKey = $privateKeyValue # The server_private.key value.
Address = 192.168.2.1/24 # Internal IP address of the VPN server.
ListenPort = 56 # Previously, we opened this port to listen for incoming connections in the firewall.

" > /etc/wireguard/wg0.conf

numberOfClients=100

#Get IP of server for client config file
server_IP=$(hostname -I | awk '{print $1}')

#Adds "numberOfClients" amount of clients to the server config file
for i in $(eval echo "{1..$numberOfClients}")
do
    mkdir /etc/wireguard/keys_for_$(($i))
    wg genkey | tee /etc/wireguard/keys_for_$(($i))/wg-client_private.key | wg pubkey > /etc/wireguard/keys_for_$(($i))/wg-client_public.key
    echo "[Peer]
PublicKey = $(cat /etc/wireguard/keys_for_$(($i))/wg-client_public.key) # client_public.key value.
AllowedIPs = 192.168.2.$(($i+1))/32 # Internal IP address of the VPN client.

" >> /etc/wireguard/wg0.conf

echo "[Interface]
PrivateKey = $(cat /etc/wireguard/keys_for_$(($i))/wg-client_private.key) 
Address = 192.168.2.$(($i+1))/32

[Peer]
PublicKey = $(cat /etc/wireguard/wg-server_public.key)
AllowedIPs = 192.168.2.0/24, 192.168.3.0/24
Endpoint = $server_IP:56
PersistentKeepalive = 30
" > /etc/wireguard/keys_for_$(($i))/wg0.conf

zip -r -j $location/bundle$(($i)).zip /etc/wireguard/keys_for_$(($i))
done

#create docker network
docker network rm docker-vpn
docker network create docker-vpn  --subnet 192.168.3.0/24

#Forward traffic to the docker image
iptables -A FORWARD  -p tcp -i wg0 --dst 192.168.3.0/24 -j ACCEPT

#restart then enable
systemctl restart wg-quick@wg0
systemctl enable wg-quick@wg0
