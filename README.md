# SIEM & Firewall Monitoring Tool 🛡️

## Description 📘
This project is an all-in-one Python tool for monitoring and securing a network. It includes a keylogger, a packet interceptor, and a basic firewall that blocks access to specific sites. It can log key presses, detect and prevent access to malicious websites, and send periodic reports via email.

## Features ⚡
- **Keylogger**: Records key presses and sends logs via email.
- **Site Access Detection**: Monitors outgoing traffic and blocks access to predefined sites.
- **SIEM Reporting**: Sends periodic security reports and keylogger data.
- **Email Notifications**: Uses SMTP to send reports and alerts.

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

## Requirements 🛠️
- Python 3
- Libraries:
  - `scapy`
  - `netfilterqueue`
  - `pynput`
  - `python-dotenv`

Install the required libraries with:
```bash
pip install scapy netfilterqueue pynput python-dotenv
```

## Firewall Configuration 🔥
To make the script work, you need to set up iptables rules to forward traffic to the Netfilter queue:

```bash
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

After running the script, reset the rules with:
```bash
iptables --flush
```

## Execution ▶️
Run the script with:
```bash
sudo python3 monitoring_tool.py
```

## Warning ⚠️
Running this script requires superuser privileges and modifies firewall rules. Use responsibly and only in controlled environments for educational or testing purposes!

## License 📄
Distributed under the MIT License.

---

Let me know if you want me to refine anything or add more details! 🚀

