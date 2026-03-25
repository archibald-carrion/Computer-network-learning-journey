from scapy.all import Ether, IP, TCP, Raw, wrpcap

# Configuration
c_mac = "00:11:22:33:44:55"
s_mac = "66:77:88:99:aa:bb"
c_ip = "192.168.1.10"
s_ip = "192.168.1.20"
c_port = 55340
s_port = 80

packets = []

# --- 1. TCP Three-Way Handshake ---
# SYN
syn = Ether(src=c_mac, dst=s_mac)/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="S", seq=1000)
packets.append(syn)

# SYN-ACK
syn_ack = Ether(src=s_mac, dst=c_mac)/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="SA", seq=5000, ack=1001)
packets.append(syn_ack)

# ACK
ack1 = Ether(src=c_mac, dst=s_mac)/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="A", seq=1001, ack=5001)
packets.append(ack1)

# --- 2. HTTP Request ---
http_req = "GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"
request = Ether(src=c_mac, dst=s_mac)/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="PA", seq=1001, ack=5001)/Raw(load=http_req)
packets.append(request)

# --- 3. HTTP Response ---
http_resp = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!"
response = Ether(src=s_mac, dst=c_mac)/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="PA", seq=5001, ack=1001 + len(http_req))/Raw(load=http_resp)
packets.append(response)

# --- 4. TCP Teardown ---
# Server FIN
s_fin = Ether(src=s_mac, dst=c_mac)/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="FA", seq=5001 + len(http_resp), ack=1001 + len(http_req))
packets.append(s_fin)

# Client ACK
c_ack = Ether(src=c_mac, dst=s_mac)/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="A", seq=1001 + len(http_req), ack=5001 + len(http_resp) + 1)
packets.append(c_ack)

# Client FIN
c_fin = Ether(src=c_mac, dst=s_mac)/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="FA", seq=1001 + len(http_req), ack=5001 + len(http_resp) + 1)
packets.append(c_fin)

# Server ACK
s_ack = Ether(src=s_mac, dst=c_mac)/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="A", seq=5001 + len(http_resp) + 1, ack=1001 + len(http_req) + 1)
packets.append(s_ack)

# Write to file
wrpcap("synthetic_http.pcap", packets)
print("PCAP file 'synthetic_http.pcap' generated successfully.")
