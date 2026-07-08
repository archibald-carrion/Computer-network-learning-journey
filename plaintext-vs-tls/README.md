# Plaintext vs. TLS: Why Encryption Matters

This project demonstrates the **need for TLS (Transport Layer Security)** by showing how easy it is to intercept unencrypted (plaintext) network traffic and how TLS prevents this.

---

## 📚 What is TLS?

**TLS (Transport Layer Security)** is a cryptographic protocol that secures communication over a network. It ensures:
- **Confidentiality**: Data is encrypted and cannot be read by eavesdroppers.
- **Integrity**: Data cannot be altered during transmission without detection.
- **Authentication**: You can verify the identity of the server (and optionally the client) using digital certificates.

TLS is the successor to SSL and is used by HTTPS, email (SMTPS), VoIP, and many other protocols.

---

## 🔍 Project Overview

This project includes two simple web servers:
1. **Plaintext HTTP Server** (`server_plaintext.py`): Submits login credentials in **unencrypted plaintext**.
2. **TLS/HTTPS Server** (`server_tls.py`): Submits the same login credentials, but **encrypted with TLS**.

By capturing the traffic from both servers (using Wireshark or tcpdump), you can **see the difference** and understand why TLS is essential.

---

## 🛠️ Setup

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)
- Wireshark or tcpdump (for traffic capture)
- OpenSSL (to generate a self-signed certificate for the TLS server)

### Generate a Self-Signed Certificate (for TLS Server)
Run this command in the `plaintext-vs-tls` directory to create `cert.pem` and `key.pem`:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

---

## 🚀 Running the Servers

### 1. Plaintext HTTP Server
```bash
python server_plaintext.py
```
- Access the server at: [http://localhost:8000](http://localhost:8000)
- Submit the login form and observe the **plaintext traffic** in Wireshark.

### 2. TLS/HTTPS Server
```bash
python server_tls.py
```
- Access the server at: [https://localhost:8443](https://localhost:8443)
  *(Your browser will warn about the self-signed certificate. Proceed anyway for this demo.)*
- Submit the login form and observe the **encrypted traffic** in Wireshark.

---

## 🔍 Capturing Traffic

### Using Wireshark
1. Start Wireshark and select your network interface.
2. Apply a filter for HTTP traffic: `http` or `tcp.port == 8000` (for plaintext).
3. Apply a filter for TLS traffic: `tls` or `tcp.port == 8443`.
4. Submit the login form on both servers and compare the captures.

### Using tcpdump
```bash
# Capture plaintext traffic (port 8000)
tcpdump -i lo -w plaintext.pcap port 8000

# Capture TLS traffic (port 8443)
tcpdump -i lo -w tls.pcap port 8443
```
- Open the `.pcap` files in Wireshark for analysis.

---

## 📌 What You’ll Observe

### Plaintext HTTP Server
- In Wireshark, you will **see the username and password in clear text** in the HTTP POST request.
- Example:
  ```
  POST /login HTTP/1.1
  Host: localhost:8000
  Content-Type: application/x-www-form-urlencoded
  
  username=test&password=secret123
  ```
- **This is a major security risk!** Anyone on the same network can intercept and read your credentials.

### TLS/HTTPS Server
- In Wireshark, you will **only see encrypted data** in the TLS records.
- The username and password are **not visible** in the capture.
- Example:
  ```
  TLSv1.2, Application Data (encrypted)
  ```
- **This is secure!** Even if someone intercepts the traffic, they cannot read the data without the encryption key.

---

## 🎯 Key Takeaways

1. **Plaintext is dangerous**: Without encryption, sensitive data like passwords, credit card numbers, and personal information can be easily intercepted.
2. **TLS encrypts everything**: With TLS, all data between the client and server is encrypted, protecting it from eavesdroppers.
3. **Always use HTTPS**: Never submit sensitive information over plaintext HTTP. Look for the padlock icon in your browser’s address bar.

---

## 📖 How TLS Works (Simplified)

1. **Handshake**: The client and server agree on a cipher suite and exchange keys.
   - The server sends its digital certificate to prove its identity.
   - The client and server generate a shared secret key (using asymmetric encryption).

2. **Encryption**: All data is encrypted using the shared secret key (symmetric encryption).

3. **Data Integrity**: TLS includes mechanisms to detect tampering with the data.

---

## 🔗 Related Resources
- [TLS Handshake Explained (Cloudflare)](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/)
- [OWASP: Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [Wireshark TLS Tutorial](https://www.wireshark.org/docs/wsug_html_chunked/wsug_graphics.html)

---

## 📝 Notes
- This demo uses a **self-signed certificate** for simplicity. In production, use certificates issued by a trusted Certificate Authority (CA).
- Modern browsers enforce HTTPS and warn users about plaintext HTTP sites.
- TLS is not just for web traffic—it’s used in email, VoIP, databases, and more.