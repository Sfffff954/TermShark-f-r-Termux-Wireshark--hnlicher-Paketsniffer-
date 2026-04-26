#!/usr/bin/env python3
"""
TermShark - Wireshark-ähnlicher Sniffer für Termux
Benötigt: pkg install tcpdump python
Nur für eigenes Netzwerk verwenden!
"""

import subprocess
import sys
import os
import re
import signal
from datetime import datetime
from collections import defaultdict

# ─── Farben ───────────────────────────────────────────────
R="\033[91m"; G="\033[92m"; Y="\033[93m"
B="\033[94m"; C="\033[96m"; M="\033[95m"; W="\033[0m"; BOLD="\033[1m"

# ─── Statistiken ──────────────────────────────────────────
stats = defaultdict(int)
connections = {}
packet_count = 0

PROTOCOLS = {
    "53":  "DNS",
    "80":  "HTTP",
    "443": "HTTPS",
    "22":  "SSH",
    "21":  "FTP",
    "23":  "Telnet",
    "25":  "SMTP",
    "110": "POP3",
    "143": "IMAP",
    "3306":"MySQL",
    "5900":"VNC",
    "3389":"RDP",
    "1883":"MQTT",
    "8080":"HTTP-Alt",
}

def get_protocol(port):
    return PROTOCOLS.get(str(port), "TCP/UDP")

def get_color(proto):
    colors = {
        "DNS": C, "HTTP": G, "HTTPS": B,
        "SSH": Y, "FTP": R, "Telnet": R,
        "MySQL": M, "VNC": R, "RDP": R,
    }
    return colors.get(proto, W)

def get_interface():
    try:
        r = subprocess.run(["ip","route"], capture_output=True, text=True)
        for line in r.stdout.split("\n"):
            if "default" in line:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == "dev":
                        return parts[i+1]
    except:
        pass
    return "wlan0"

def parse_packet(line):
    """Parst tcpdump Output Zeile"""
    global packet_count
    try:
        # Format: HH:MM:SS.ms IP src.port > dst.port: Flags
        m = re.search(r'(\d+:\d+:\d+\.\d+).*?(\d+\.\d+\.\d+\.\d+)\.?(\d+)?\s*>\s*(\d+\.\d+\.\d+\.\d+)\.?(\d+)?', line)
        if not m:
            return None

        time_str = m.group(1)[:8]
        src_ip   = m.group(2)
        src_port = m.group(3) or "?"
        dst_ip   = m.group(4)
        dst_port = m.group(5) or "?"

        proto = get_protocol(dst_port) if dst_port != "?" else get_protocol(src_port)
        color = get_color(proto)
        packet_count += 1

        # Länge
        length_m = re.search(r'length (\d+)', line)
        length = length_m.group(1) if length_m else "?"

        stats[proto] += 1

        return {
            "no": packet_count,
            "time": time_str,
            "src": f"{src_ip}:{src_port}",
            "dst": f"{dst_ip}:{dst_port}",
            "proto": proto,
            "color": color,
            "length": length,
        }
    except:
        return None

def print_packet(p):
    print(
        f"  {Y}{p['no']:<5}{W} "
        f"{p['time']}  "
        f"{G}{p['src']:<23}{W} → "
        f"{R}{p['dst']:<23}{W} "
        f"{p['color']}{p['proto']:<10}{W} "
        f"{p['length']} bytes"
    )

def print_stats():
    print(f"\n{BOLD}{C}╔══════ Statistik ══════╗{W}")
    print(f"{BOLD}{C}║ Pakete gesamt: {packet_count:<6} ║{W}")
    print(f"{BOLD}{C}╠═══════════════════════╣{W}")
    for proto, count in sorted(stats.items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 20)
        print(f"{BOLD}{C}║{W} {proto:<10} {count:<5} {G}{bar}{W}")
    print(f"{BOLD}{C}╚═══════════════════════╝{W}")

def banner():
    print(f"""
{C}{BOLD}╔══════════════════════════════════════╗
║        TermShark für Termux          ║
║   Wireshark-ähnlicher Paketsniffer   ║
╚══════════════════════════════════════╝{W}
  {Y}No  Time      Quelle                  Ziel                    Protokoll   Größe{W}
  {"─"*85}""")

def menu():
    iface = get_interface()
    print(f"""
{C}{BOLD}╔══════════════════════════════════════╗
║        TermShark für Termux          ║
╚══════════════════════════════════════╝{W}

  Interface erkannt: {G}{iface}{W}

  {BOLD}1{W} - Alle Pakete sniffern
  {BOLD}2{W} - Nur HTTP/HTTPS
  {BOLD}3{W} - Nur DNS
  {BOLD}4{W} - Nur SSH
  {BOLD}5{W} - Nach IP filtern
  {BOLD}q{W} - Beenden
""")
    choice = input(f"{C}> {W}").strip().lower()
    return choice, iface

def build_filter(choice, iface):
    filters = {
        "1": "",
        "2": "port 80 or port 443",
        "3": "port 53",
        "4": "port 22",
    }
    if choice in filters:
        return filters[choice], iface
    elif choice == "5":
        ip = input(f"IP-Adresse: ").strip()
        return f"host {ip}", iface
    elif choice == "q":
        sys.exit(0)
    else:
        return "", iface

def check_tcpdump():
    try:
        subprocess.run(["tcpdump","--version"], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def sniff(filter_str, iface):
    global packet_count, stats
    packet_count = 0
    stats = defaultdict(int)

    cmd = ["tcpdump", "-i", iface, "-l", "-n", "-q"]
    if filter_str:
        cmd += filter_str.split()

    print(f"\n{Y}[*] Starte Sniffer auf {iface}... (Ctrl+C zum Stoppen){W}\n")
    banner()

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True)
        for line in proc.stdout:
            p = parse_packet(line.strip())
            if p:
                print_packet(p)
    except KeyboardInterrupt:
        proc.terminate()
        print_stats()
    except PermissionError:
        print(f"\n{R}[!] Kein Root. Starte mit: sudo python termshark.py{W}")
    except Exception as e:
        print(f"\n{R}Fehler: {e}{W}")

def main():
    if not check_tcpdump():
        print(f"{R}tcpdump nicht gefunden!{W}")
        print(f"{Y}Installiere: pkg install tcpdump{W}")
        sys.exit(1)

    while True:
        choice, iface = menu()
        filter_str, iface = build_filter(choice, iface)
        sniff(filter_str, iface)
        input(f"\n{Y}[Enter] zurück...{W}")

if __name__ == "__main__":
    main()
