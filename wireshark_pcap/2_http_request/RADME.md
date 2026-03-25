# Analyze a synthetic HTTP capture to understand how TCP manages state, data integrity, and flow control

## Part 1: Encapsulation & Headers
1. Header Sizes: Open the generated .pcap in Wireshark. Looking at the first SYN packet, calculate the total size of the headers (Ethernet + IP + TCP). How many bytes of actual 'user data' are in this packet?
    54 bytes, no user data

2. Addressing: Identify the Source Port and Destination Port. Why is the destination port usually a 'well-known' number (80), while the source port is a large, seemingly random number?
    Source Address: 192.168.1.10; Source Port: 55340
    Destination Address: 192.168.1.20; Destination Port: 80
    It makes sense that the destination port is well defined because it is linked to a service like HTTP on 80, SSH on 22, telnet on 23, etc.
    After investigating, looks like the source port is usually pseudo-random and ephemeral ports, for multiple reasons, like security and handling multiple connectiosn at the same time.

3. The 'Next Sequence Number': In the HTTP Request packet, Wireshark provides a field called 'Next Sequence Number.' How is this value calculated based on the current Sequence Number and the TCP segment length?
    Looks like its the Sequence Number: 1    (relative sequence number) plus the [TCP Segment Len: 47]
        -> [Next Sequence Number: 48    (relative sequence number)]

## Part 2: The Three-Way Handshake
4. Flag Logic: List the TCP Flags (bits) that are set to 1 in each of the first three packets. Why is the ACK flag not set in the very first packet?
    1 -> Syn
    2 -> Ack, Syn
    3 -> Ack
    The first packet does not have the ack flag set because it does not have receive approval from the destinator yet

5. Relative vs. Raw: In Wireshark, sequence numbers are often displayed as 'Relative'. Switch to 'Raw' values. What is the actual raw sequence number of the SYN-ACK packet, and why do protocols use large random numbers?
    The sequence number of the SYN-ACK packet is Sequence Number: 1001
    Protocols use large random raw sequence numbers to ensure each connection startr in an unpredictable point in the seuqnece space (for security reasons) and avoiding confusion with packets from previous interactions.
    
