#Setup apt on our servet
echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list

printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable
apt-get update
apt-get install linux-headers-$(uname -r|sed 's/[^-]*-[^-]*-//')
# Setup Wireguard
apt-get install wireguard
wg genkey | tee /etc/wireguard/wg-private.key | wg pubkey > /etc/wireguard/wg-public.key
sudo nano /etc/wireguard/wg0.conf

privateKeyValue=$(cat /etc/wireguard/wg-private.key)

ethvalue=$(ip -o -4 route show to default | awk '{print $5}')

echo "[Interface]
PrivateKey = $privateKeyValue # The server_private.key value.
Address = 10.0.0.1/24 # Internal IP address of the VPN server.
ListenPort = 56 # Previously, we opened this port to listen for incoming connections in the firewall.
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o $ethvalue -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o $ethvalue -j MASQUERADE

# Configurations for the clients. You need to add a [Peer] section for each VPN client.
[Peer]
PublicKey = nreKUqhW3oQZtswhNd246s2gG8HRFoIsM7isGZinC0o= # client_public.key value.
AllowedIPs = 10.0.0.2/32, 10.0.0.2/24 # Internal IP address of the VPN client.
" > /etc/wireguard/wg0.conf