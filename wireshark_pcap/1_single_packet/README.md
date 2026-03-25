1. Layer 2 Identification: Look at the Ethernet header. What is the 'Type' field value (in hex)? What does this value tell the receiver about the next layer (Layer 3)?
    0x0800 IPv4

2. Header Length vs. Payload: In the IPv4 header, identify the 'Header Length' and 'Total Length' fields. Subtracting the header sizes, how many bytes are dedicated purely to the TCP segment?
    Header length = 20bytes
    Total lenght= 129bytes
    Payload size = 129-20=109bytes

3. The 3-Way Handshake Context: Look at the TCP flags. This packet has the 'PSH' and 'ACK' flags set. Based on your knowledge of TCP, could this be the very first packet of a connection? Why or why not?
    0x18 -> 0001 1000
    Cannot be the first packet of a connection because it does not have the Syn bit set

4. Hexadecimal Mapping: Locate the source IP address in the packet details. Then, find those same 4 bytes in the 'Hex Dump' pane at the bottom of Wireshark. Write down the hex values representing the source IP.
    Source Address: 192.168.1.10 -> c0 a8 01 0a

5. Application Layer: Does the HTTP data begin immediately after the TCP header? How does the receiver know where the TCP header ends and the HTTP request begins?
    Yes, the TCP header is right before the HTTP data, my first thought was that the last 2 bytes of the TCP header is Urgent Pointer: 0 -> 0x00 0x00 may besome kind of delimiter, but after investigating it seems that the answer is more likely related to the data Header Length: 20 bytes 

