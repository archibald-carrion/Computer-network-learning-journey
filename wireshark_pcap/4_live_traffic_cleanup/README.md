# Assignment: Real-World Traffic Sniffing & Feature Extraction

## Objective
Capture live network traffic, isolate specific application personas, and use Wireshark filters to export a clean, focused dataset for analysis.

---

## Part 1: Data Collection & Cleanup

- Start a Wireshark capture on your active interface.
- Generate 30 seconds of **'Chat'** and **'Video'** traffic as instructed.
- **Isolate Stream A**:
  - Find a chat packet
  - Right-click → Follow → TCP Stream
  - Note the stream index (e.g., `tcp.stream eq 5`)
- **Isolate Stream B**:
  - Find a video packet
  - Right-click → Follow → TCP Stream
  - Note the stream index (e.g., `tcp.stream eq 12`)
- **Apply Global Filter**:
  - In the filter bar, combine both streams using OR:
    ```
    tcp.stream eq 5 or tcp.stream eq 12
    ```
- **Export Clean File**:
  - Go to: `File → Export Specified Packets...`
  - Select **Displayed**
  - Save as:
    ```
    my_traffic.pcap
    ```

---

## Part 2: Manual Identification

1. Verify your cleanup:
   - Does your new `.pcap` file contain any packets other than your two chosen streams?
      yes, lots
   - How can you tell?
      many different ips, and protocols

2. Compare the total byte count of both streams:
   - What percentage of your total capture is dedicated to the video stream?

---

## Part 3: Automated Math (Python)

Run the provided statistical analysis script against your `my_traffic.pcap` file and complete the table:

| Application | Pkt Count | Mean Size (Bytes) | Max Size (Bytes) |
|------------|----------|-------------------|------------------|
| Chat Flow  |17        | 54                |   54             |
| Video Flow |4168      | ~1200B              |      1292       |