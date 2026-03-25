from scapy.all import Ether, IP, TCP, Raw, wrpcap

packets = []

def create_tcp_session(c_ip, s_ip, c_port, s_port, seq_c, seq_s, data_list, is_video=False):
    sess = []
    # Handshake
    sess.append(Ether()/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="S", seq=seq_c))
    sess.append(Ether()/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="SA", seq=seq_s, ack=seq_c+1))
    sess.append(Ether()/IP(src=c_ip, dst=s_ip)/TCP(sport=c_port, dport=s_port, flags="A", seq=seq_c+1, ack=seq_s+1))
    
    curr_c = seq_c + 1
    curr_s = seq_s + 1
    
    # Data Exchange
    for data in data_list:
        p = Ether()/IP(src=s_ip, dst=c_ip)/TCP(sport=s_port, dport=c_port, flags="PA", seq=curr_s, ack=curr_c)/Raw(load=data)
        sess.append(p)
        curr_s += len(data)
    
    return sess

# 1. Chat Flow: Small packets
chat_data = ["Hello!", "How are you?", "Fine, thanks."]
packets += create_tcp_session("10.0.0.1", "10.0.0.2", 4444, 80, 1000, 5000, chat_data)

# 2. Video Flow: Large "MTU-sized" packets (simulating 1460 bytes of payload)
video_chunk = "V" * 1460 
video_data = [video_chunk] * 20  # 20 large packets
packets += create_tcp_session("10.0.0.1", "10.0.0.2", 5555, 8080, 2000, 9000, video_data, True)

wrpcap("mixed_traffic.pcap", packets)
print("PCAP 'mixed_traffic.pcap' generated.")
