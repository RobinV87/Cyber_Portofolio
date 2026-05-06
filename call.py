#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/mnt/c/Users/RobinVersloot/OneDrive - Cloud ÉÉN/SupportDesk/calllog/logs")

def today_file():
    return BASE_DIR / f"{datetime.now().date()}.md"

def ensure_file(path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# 📞 Bel-log – {datetime.now().date()}\n\n")

def log_call(args):
    now = datetime.now()
    time = now.strftime("%H:%M")
    direction = "Inkomend" if args.inbound else "Uitgaand"

    entry = f"""## {time} – {direction}
**Klant:** {args.client}  
"""
    if args.contact:
        entry += f"**Contact:** {args.contact}  \n"
    if args.case:
        entry += f"**Case:** {args.case}  \n"
    if args.subject:
        entry += f"**Onderwerp:** {args.subject}  \n"

    entry += "**Notities:**\n"
    if args.notes:
        for line in args.notes.split("\\n"):
            entry += f"- {line}\n"
    else:
        entry += "-\n"

    entry += "\n---\n\n"

    file = today_file()
    ensure_file(file)
    with file.open("a") as f:
        f.write(entry)

    print(f"✅ Belletje gelogd in {file}")

def main():
    parser = argparse.ArgumentParser(description="CLI bel-log")
    sub = parser.add_subparsers(dest="cmd")

    log = sub.add_parser("log")
    log.add_argument("client", help="Klantnaam")
    log.add_argument("--contact", help="Contactpersoon")
    log.add_argument("--case", help="Case-nummer")
    log.add_argument("--subject", help="Onderwerp")
    log.add_argument("--notes", help="Notities (use \\n voor meerdere regels)")
    log.add_argument("--inbound", action="store_true", help="Inkomend gesprek")

    args = parser.parse_args()
    if args.cmd == "log":
        log_call(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
