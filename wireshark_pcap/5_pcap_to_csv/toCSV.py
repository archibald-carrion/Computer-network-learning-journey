import csv
from scapy.all import rdpcap, IP, TCP, UDP

def pcap_to_labeled_csv(pcap_file, output_csv):
    pkts = rdpcap(pcap_file)
    flows = {}

    # Step 1: Group by Flow
    for p in pkts:
        if IP in p:
            proto = "TCP" if TCP in p else "UDP" if UDP in p else "Other"
            if proto == "Other": continue
            
            sport = p[TCP].sport if TCP in p else p[UDP].sport
            dport = p[TCP].dport if TCP in p else p[UDP].dport
            
            # Key is (IP_A, IP_B, Port_A, Port_B)
            flow_id = tuple(sorted([(p[IP].src, sport), (p[IP].dst, dport)]))
            
            if flow_id not in flows:
                flows[flow_id] = {'lengths': [], 'ips': set([p[IP].src, p[IP].dst])}
            
            flows[flow_id]['lengths'].append(len(p))

    # Step 2: Extract Features and Label
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mean_len', 'max_len', 'min_len', 'pkt_count', 'label'])
        
        for fid, data in flows.items():
            lengths = data['lengths']
            
            # Simple Labeling Logic based on the synthetic IPs we used
            label = "Unknown"
            if "10.0.0.1" in data['ips'] or "10.0.0.2" in data['ips']:
                label = "Chat"
            elif "192.168.1.50" in data['ips'] or "192.168.1.100" in data['ips']:
                label = "Video"
            
            writer.writerow([
                sum(lengths)/len(lengths), # mean_len
                max(lengths),              # max_len
                min(lengths),              # min_len
                len(lengths),              # pkt_count
                label                      # Target Label
            ])

    print(f"Dataset saved to {output_csv}")

pcap_to_labeled_csv("training_data.pcap", "network_dataset.csv")
