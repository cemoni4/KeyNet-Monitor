# 🛡️ KeyNet-Monitor — Network & System Security Tool

## 📘 Description
KeyNet-Monitor is a comprehensive security tool built with Python that combines real-time packet interception, keystroke logging, and SIEM-like reporting. It helps monitor and protect your system by capturing suspicious activity, blocking unauthorized website access, and sending regular security reports via email.

## ⚡ Features
- **Keylogger:** Logs keystrokes and sends periodic reports.
- **Packet Interceptor:** Monitors network packets and blocks access to blacklisted sites (e.g., cisco.com).
- **SIEM Reporting:** Generates and emails security event reports every minute.
- **Email Notifications:** Sends logs and alerts through SMTP.
- **Firewall Management:** Automatically configures iptables rules for traffic interception.

## 🛠️ Requirements
- Python 3
- Libraries: `scapy`, `pynput`, `netfilterqueue`, `dotenv`

Install dependencies with:
```bash
pip install scapy pynput netfilterqueue python-dotenv
```

## 🔧 Firewall Configuration
Enable NetfilterQueue with:
```bash
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

Reset rules when finished:
```bash
iptables --flush
```

## 🚀 Execution
Create a `.env` file with your email credentials:
```
SENDER_EMAIL="your_email@example.com"
SENDER_PASSWORD="your_password"
RECIPIENT_EMAIL="recipient@example.com"
```

## How to Change the Blocked Site 🛠️
By default, the script blocks access to `cisco.com`. You can change the blocked site by modifying the `packet_callback` function in the script:

```python
if "cisco.com" in payload:  # Change 'cisco.com' to the site you want to block
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_src = scapy_packet[scapy.IP].src
    print(f"[BLOCKED] Accesso a sito malevolo bloccato! {current_time} - IP: {ip_src}")

    detected_sites.append(f"{current_time} - {ip_src} tentativo di accesso a cisco.com")
    packet.drop()
    return
```

Simply replace `cisco.com` with the domain you want to block, save the script, and run it again! 🔧

Run the script with superuser privileges:
```bash
sudo python3 SIEM.py
```

## ⚠️ Warning
This tool is for educational and research purposes only. Use it responsibly and only in environments where you have explicit authorization.

## 📄 License
Distributed under the MIT License.

---

