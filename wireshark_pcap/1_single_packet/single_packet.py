from scapy.all import Ether, IP, TCP, Raw, wrpcap

# 1. Define the layers
# Layer 2: Ethernet
eth_layer = Ether(
    src="00:11:22:33:44:55", 
    dst="66:77:88:99:aa:bb"
)

# Layer 3: IPv4
ip_layer = IP(
    src="192.168.1.10", 
    dst="192.168.1.20"
)

# Layer 4: TCP
# We use the 'PA' flag (Push-Acknowledgment) which is common for data-carrying packets
tcp_layer = TCP(
    sport=54321, 
    dport=80, 
    flags="PA", 
    seq=1000, 
    ack=5000
)

# Layer 7: HTTP (Synthetic Header)
http_payload = (
    "GET /index.html HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "User-Agent: Scapy-Generator\r\n"
    "Accept: */*\r\n"
    "\r\n"
)

# 2. Stack the layers using the '/' operator
single_packet = eth_layer / ip_layer / tcp_layer / Raw(load=http_payload)

# 3. Save to a pcap file
wrpcap("single_http_packet.pcap", [single_packet])

print("PCAP 'single_http_packet.pcap' generated successfully.")
