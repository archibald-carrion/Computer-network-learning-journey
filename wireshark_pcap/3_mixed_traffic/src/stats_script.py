from scapy.all import rdpcap, IP, TCP

def analyze_pcap(filename):
    pkts = rdpcap(filename)
    # Dictionary to store stats per flow: (IP_src, IP_dst, port_src, port_dst)
    flows = {}

    for p in pkts:
        if IP in p and TCP in p:
            # Create a unique key for the bidirectional flow
            flow_id = tuple(sorted([(p[IP].src, p[TCP].sport), (p[IP].dst, p[TCP].dport)]))
            
            if flow_id not in flows:
                flows[flow_id] = []
            
            # Store the length of the IP packet
            flows[flow_id].append(len(p[IP]))

    print(f"{'Flow (Endpoints)':<45} | {'Pkts':<6} | {'Mean Size':<10} | {'Max Size':<8}")
    print("-" * 80)

    for fid, lengths in flows.items():
        mean_size = sum(lengths) / len(lengths)
        max_size = max(lengths)
        flow_label = f"{fid[0][0]}:{fid[0][1]} <-> {fid[1][0]}:{fid[1][1]}"
        print(f"{flow_label:<45} | {len(lengths):<6} | {mean_size:<10.2f} | {max_size:<8}")

if __name__ == "__main__":
    try:
        analyze_pcap("mixed_traffic.pcap")
    except FileNotFoundError:
        print("Error: mixed_traffic.pcap not found. Run the generator script first!")
