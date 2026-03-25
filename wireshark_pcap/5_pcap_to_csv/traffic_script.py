from scapy.all import Ether, IP, TCP, UDP, Raw, wrpcap
import random

def generate_labeled_pcap():
    packets = []
    
    # Flow 1: Chat (TCP) - 10.0.0.1 <-> 10.0.0.2
    c_ip, s_ip = "10.0.0.1", "10.0.0.2"
    c_port, s_port = 4444, 80
    # 3-Way Handshake
    packets.append(Ether()/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="S", seq=100))
    packets.append(Ether()/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="SA", seq=500, ack=101))
    packets.append(Ether()/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="A", seq=101, ack=501))
    
    for i in range(30):
        # Small random lengths for chat (e.g., 5 to 50 bytes)
        payload = "C" * random.randint(5, 50)
        packets.append(Ether()/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="PA")/Raw(load=payload))

    # Flow 2: Video (UDP) - 192.168.1.50 <-> 192.168.1.100
    v_ip, vs_ip = "192.168.1.50", "192.168.1.100"
    v_port, vs_port = 5555, 443
    for i in range(30):
        # Large consistent lengths for video (e.g., 1400 to 1460 bytes)
        payload = "V" * random.randint(1400, 1460)
        packets.append(Ether()/IP(src=vs_ip, dst=v_ip)/UDP(sport=vs_port, dport=v_port)/Raw(load=payload))

    wrpcap("training_data.pcap", packets)
    print("Generated training_data.pcap with 60+ packets.")

generate_labeled_pcap()
