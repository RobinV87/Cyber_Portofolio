#!/usr/bin/env python3

import subprocess
import logging
import argparse
import re
import os
from datetime import datetime

from config import TARGETS, FORBIDDEN_PORTS, NMAP_PATH


# ======================================================
# Argument parsing
# ======================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Automated Nmap Security Scanner")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show scan progress and findings"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
    "--syn",
    action="store_true",
    help="Use TCP SYN scan (-sS), requires root"
    )

    parser.add_argument(
    "--service",
    action="store_true",
    help="Enable service/version detection (-sV)"
    )


    return parser.parse_args()


# ======================================================
# Logging
# ======================================================
def setup_logging(debug=False):
    os.makedirs("logs", exist_ok=True)

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        filename="logs/scan.log",
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# ======================================================
# Run Nmap & store RAW output
# ======================================================
def run_nmap(target, use_syn=False, use_service=False):
    command = [
        NMAP_PATH,
        "-Pn",
        "--exclude-ports", "5060,2000"
    ]

    if use_syn:
        command.append("-sS")

    if use_service:
        command.append("-sV")

    command.append(target)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    os.makedirs("reports/nmap_raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_target = target.replace(".", "_")
    raw_file = f"reports/nmap_raw/{timestamp}_{safe_target}.nmap.txt"

    with open(raw_file, "w") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\n\n--- STDERR ---\n")
            f.write(result.stderr)

    return result.stdout

# ======================================================
# Parse forbidden ports
# ======================================================
def parse_nmap_output(output, target):
    findings = []

    for line in output.splitlines():
        match = re.match(r"(\d+)/tcp\s+open", line)
        if not match:
            continue

        port = int(match.group(1))
        port_info = FORBIDDEN_PORTS.get(port)

        if not port_info:
            continue

        # Support legacy + new config format
        if isinstance(port_info, dict):
            service = port_info.get("service", "Unknown")
            severity = port_info.get("severity", "MED")
            comment = port_info.get("comment", "")
        else:
            service = port_info
            severity = "MED"
            comment = "Legacy definition"

        findings.append({
            "target": target,
            "port": port,
            "service": service,
            "severity": severity,
            "comment": comment,
            "status": "OPEN"
        })

    return findings


# ======================================================
# Main
# ======================================================
def main():
    args = parse_args()
    setup_logging(debug=args.debug)

    if args.verbose:
        print(f"[INFO] Scan started at {datetime.now().isoformat()}")

    all_findings = []

    for target in TARGETS:
        if args.verbose:
            print(f"[INFO] Scanning target: {target}")

        output = run_nmap(
            target,
            use_syn=args.syn,
            use_service=args.service
        )

        findings = parse_nmap_output(output, target)

        if findings:
            all_findings.extend(findings)
            if args.verbose:
                for f in findings:
                    print(
                        f"[{f['severity']}] {f['target']} "
                        f"- Port {f['port']} ({f['service']}) OPEN"
                    )
        else:
            if args.verbose:
                print(f"[OK] No forbidden ports found on {target}")

    if args.verbose:
        print(f"[INFO] Scan completed – {len(all_findings)} finding(s)")


# ======================================================
# Entrypoint
# ======================================================
if __name__ == "__main__":
    main()
