Assignment: Traffic Characterization & Flow Analysis
Objective
Distinguish between application types by analyzing flow statistics and packet size distribution in a mixed-traffic environment.
1. The 'Conversations' Snapshot
    1. Open mixed_traffic.pcap and navigate to Statistics -> Conversations -> TCP.
    2. Compare the 'Bytes' and 'Packets' columns for both rows. Which Stream ID corresponds to the 'Chat' and which to the 'Video'? Justify your answer using the data.
    3. Calculate the average packet size for each stream. How does this relate to the application's likely purpose?
2. Packet Size Distribution
    4. Navigate to Statistics -> Packet Lengths.
    5. Identify the two distinct spikes in the distribution graph. Explain what each represents in the context of these two applications.
    6. Why does the 'Chat' application result in significantly more small (control) overhead compared to the 'Video' stream?
3. Throughput & I/O Graphs
    7. Open Statistics -> I/O Graphs. Create filters for 'tcp.port == 80' and 'tcp.port == 8080'.
    8. Set the Y-Axis to 'Bits/Sec'. What is the peak throughput of each stream?
    9. If you were to apply a Machine Learning model to classify these flows, which three statistical features would be most reliable for identification?




Solution Key: Traffic Characterization & Flow Analysis
1. The Conversations Snapshot
Identification: Stream 1 (Port 8080) is the Video flow due to high byte/packet counts. Stream 0 (Port 80) is the Chat flow due to minimal data transfer.
Average Packet Size: Chat packets average <100 bytes (signaling/text). Video packets average ~1500 bytes (MTU-sized data transfer).
2. Packet Size Distribution
Spikes: The 40-79 byte spike represents TCP ACKs/control packets. The 1280-2559 byte spike represents the 1460-byte video payloads.
Overhead: Chat has high overhead because the 40-byte header is large relative to the tiny payload. Video is more efficient as the header is small relative to 1460 bytes.
3. Throughput & ML Features
Peak Throughput: Video will show a significantly higher bits/sec curve in the I/O graph.
ML Features: 1. Mean Packet Length, 2. Inter-Arrival Time (IAT) Variance, 3. Flow Asymmetry (Ratio of bytes Sent vs. Received).