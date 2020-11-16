#Setup apt on our server
echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list

printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable
apt-get update
apt-get install linux-headers-$(uname -r|sed 's/[^-]*-[^-]*-//')
# Setup Wireguard
apt-get install wireguard
wg genkey | tee /etc/wireguard/wg-server_private.key | wg pubkey > /etc/wireguard/wg-pserver_public.key

privateKeyValue=$(cat /etc/wireguard/wg-server_private.key)

#Removes comment tag to allow ip forwarding
server='net.ipv4.ip_forward=1'; sed -i "/^#$server/ c$server" /etc/sysctl.conf

#Sets IP forwarding to 1, to allow it
echo 1 > /proc/sys/net/ipv4/ip_forward

ethValue=$(ip -o -4 route show to default | awk '{print $5}')

#Sets the wg0.conf file with server values
echo "[Interface]
PrivateKey = $privateKeyValue # The server_private.key value.
Address = 10.0.0.1/24 # Internal IP address of the VPN server.
ListenPort = 56 # Previously, we opened this port to listen for incoming connections in the firewall.
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o $ethValue -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o $ethValue -j MASQUERADE
" > /etc/wireguard/wg0.conf

numberOfClients=5

#Adds "numberOfClients" amount of clients to the server config file
for i in $(eval echo "{1..$numberOfClients}")
do
    wg genkey | tee /etc/wireguard/wg-client_private$(($i+1)).key | wg pubkey > /etc/wireguard/wg-client_public$(($i+1)).key
    echo "[Peer]
PublicKey = $(cat /etc/wireguard/wg-client_public$(($i+1)).key) # client_public.key value.
AllowedIPs = 10.0.0.$(($i+1))/32, 10.0.0.$(($i+1))/24 # Internal IP address of the VPN client.
" >> /etc/wireguard/wg0.conf
done

systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0