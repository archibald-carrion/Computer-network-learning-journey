# What is PCAP (first principles)

**PCAP = Packet Capture**

It’s both:

1. a **file format**
2. and a **concept**: recording raw network traffic

> A PCAP file is basically a **binary log of packets as they appeared on the wire**

---

# 📦 What’s inside a PCAP file?

Think of it like a time-ordered stream:

```
[Packet 1]
  timestamp
  raw bytes (Ethernet frame)

[Packet 2]
  timestamp
  raw bytes

...
```

Each packet includes:

* **timestamp** (when it was seen)
* **L2 frame** (Ethernet, Wi-Fi, etc.)
* which contains:

  * IP header
  * TCP/UDP header
  * payload (actual data)

👉 It’s *not interpreted* — it’s **ground truth bytes**

---

# 🔬 Example Stack Inside PCAP

One packet might decode to:

```
Ethernet
  → IP
    → TCP
      → HTTP
```

But the PCAP itself just stores:

```
0x45 0x00 0x00 0x3c ...
```
