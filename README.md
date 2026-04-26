[README_termshark.md](https://github.com/user-attachments/files/27102555/README_termshark.md)
# 🦈 TermShark für Termux

Wireshark-ähnlicher Paketsniffer für Android (Termux)

> ⚠️ **Nur für eigenes Netzwerk verwenden!**

---

## Features

| Feature | Beschreibung |
|---------|-------------|
| Live Sniffer | Pakete in Echtzeit anzeigen |
| Filter | HTTP, HTTPS, DNS, SSH, oder nach IP |
| Protokoll-Erkennung | 15+ Protokolle automatisch erkannt |
| Statistik | Übersicht am Ende des Scans |
| Auto-Interface | wlan0 wird automatisch erkannt |

---

## Installation

```bash
# 1. Pakete installieren
pkg update && pkg install python tcpdump -y

# 2. Repo klonen
git clone https://github.com/Sfffff954/scane-for-termux.git

# 3. Rein
cd scane-for-termux

# 4. Starten (Root empfohlen)
tsu
python termshark.py
```

---

## Update

```bash
cd scane-for-termux
git pull
```

---

## Menü

```
╔══════════════════════════════════════╗
║        TermShark für Termux          ║
║   Wireshark-ähnlicher Paketsniffer   ║
╚══════════════════════════════════════╝

  1 - Alle Pakete sniffern
  2 - Nur HTTP/HTTPS
  3 - Nur DNS
  4 - Nur SSH
  5 - Nach IP filtern
  q - Beenden
```

---

## Output Beispiel

```
  No    Time      Quelle                  Ziel                    Protokoll   Größe
  ─────────────────────────────────────────────────────────────────────────────────
  1     12:00:01  192.168.1.100:443    →  192.168.1.1:51234      HTTPS      128 bytes
  2     12:00:01  192.168.1.1:53       →  192.168.1.100:12345    DNS        64 bytes
```

---

## Voraussetzungen

| Paket | Installation |
|-------|-------------|
| Termux | [F-Droid](https://f-droid.org/packages/com.termux/) |
| tcpdump | `pkg install tcpdump` |
| Root | `pkg install tsu` |

# 1. Pakete installieren
pkg update && pkg install python tcpdump tsu -y

# 2. Repo klonen
git clone https://github.com/Sfffff954/TermShark-f-r-Termux-Wireshark--hnlicher-Paketsniffer-.git

# 3. Rein
cd TermShark-f-r-Termux-Wireshark--hnlicher-Paketsniffer-

# 4. Starten
tsu
python termshark.py

---

## Lizenz

MIT — Nur für legale Nutzung im eigenen Netzwerk.
