#!/usr/bin/env python3
"""
EPG generator — produces a 7-day XMLTV file from channels.yaml.
Each channel shows the same title on a repeating hourly schedule.
Output: epg.xml (commit to repo for a stable raw GitHub URL)
"""

import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: run  pip install pyyaml")


DAYS_AHEAD = 7
OUTPUT_FILE = Path(__file__).parent / "epg.xml"
CHANNELS_FILE = Path(__file__).parent / "channels.yaml"


def load_channels(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    channels = data.get("channels", [])
    if not channels:
        sys.exit(f"No channels found in {path}")
    return channels


def fmt_time(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S +0000")


def build_xmltv(channels: list[dict]) -> ET.Element:
    root = ET.Element("tv", {
        "generator-info-name": "epg-generator",
        "generator-info-url": "https://github.com/ferryneil/crispy-umbrella",
    })

    for ch in channels:
        el = ET.SubElement(root, "channel", id=ch["id"])
        ET.SubElement(el, "display-name", lang="en").text = ch["display_name"]
        if ch.get("logo"):
            ET.SubElement(el, "icon", src=ch["logo"])

    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start_of_today = now.replace(hour=0)

    for ch in channels:
        for day in range(DAYS_AHEAD):
            day_start = start_of_today + timedelta(days=day)
            for hour in range(24):
                start = day_start + timedelta(hours=hour)
                stop = start + timedelta(hours=1)
                prog = ET.SubElement(root, "programme", {
                    "start": fmt_time(start),
                    "stop": fmt_time(stop),
                    "channel": ch["id"],
                })
                ET.SubElement(prog, "title", lang="en").text = ch["title"]
                if ch.get("description"):
                    ET.SubElement(prog, "desc", lang="en").text = ch["description"]

    return root


def indent(elem: ET.Element, level: int = 0) -> None:
    pad = "\n" + "    " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = pad
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = pad
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = pad


def main() -> None:
    channels = load_channels(CHANNELS_FILE)
    print(f"Loaded {len(channels)} channels")

    root = build_xmltv(channels)
    indent(root)

    tree = ET.ElementTree(root)
    ET.register_namespace("", "")

    with open(OUTPUT_FILE, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

    size_kb = OUTPUT_FILE.stat().st_size // 1024
    print(f"Written {OUTPUT_FILE}  ({size_kb} KB)")
    print(f"Covers {DAYS_AHEAD} days from {datetime.now(timezone.utc).date()}")


if __name__ == "__main__":
    main()
