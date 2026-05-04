# config.py
"""
WARNING:
This script may only be used on networks and systems
for which explicit permission has been granted.
"""

# Targets to be scanned
TARGETS = [
    "x.x.x.x",  # Replace this with the IP address or subnet you want to scan
]

# Critical ports that must NOT be publicly/openly accessible
# Key = port, Value = description / risk
FORBIDDEN_PORTS = {

    # --- Remote management ---
    21:  "FTP (unencrypted)",
    22:  "SSH (internal / VPN only)",
    23:  "Telnet (insecure)",
    3389:"RDP (brute-force risk)",
    5900:"VNC (remote control)",

    # --- Windows / SMB ---
    135: "RPC",
    139: "NetBIOS",
    445: "SMB (ransomware risk)",

    # --- Databases ---
    1433:"MSSQL",
    3306:"MySQL",
    5432:"PostgreSQL",
    27017:"MongoDB",

    # --- Web / Admin panels ---
    80:  "HTTP / Admin Panel",
    443: "HTTPS / Admin Panel",
    8080:"HTTP Alt / Admin panel",
    8443:"HTTPS Alt / Admin panel",
    8000:"Custom web service",
    8888:"Custom web/admin",

    # --- UniFi / Network management ---
    8081:"UniFi device communication",
    8443:"UniFi Controller",
    8843:"UniFi Guest Portal HTTPS",
    6789:"UniFi Speedtest",
    10001:"UniFi Discovery",

    # --- IP Cameras / CCTV ---
    554:  "RTSP (camera stream)",
    8000:"DVR/NVR web interface",
    37777:"Dahua camera",
    34567:"Hikvision camera",
    8899:"Camera cloud/service port",

    # --- Virtualization / servers ---
    902: "VMware ESXi",
    903: "VMware Console",
    5985:"WinRM HTTP",
    5986:"WinRM HTTPS",

    # --- Mail ---
    25:  "SMTP (abuse / open relay)",
    110: "POP3",
    143: "IMAP",

    # --- Other frequently abused ---
    69:  "TFTP",
    161: "SNMP (information leak)",
    162: "SNMP Trap",
    541: "server?",
    9443: "Tungsten-https",
}

# Nmap binary (usually correct as-is)
NMAP_PATH = "nmap"
