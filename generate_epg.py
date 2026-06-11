#!/usr/bin/env python3
"""
EPG generator

Normal usage:
    python generate_epg.py            # fetch sources, write epg.xml

Discover channel IDs available in a source feed:
    python generate_epg.py --discover <url>
"""

import argparse
import gzip
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency — run: pip install pyyaml")

CONFIG_FILE = Path(__file__).parent / "config.yaml"
OUTPUT_FILE = Path(__file__).parent / "epg.xml"
CUSTOM_DAYS = 7
TIMEOUT = 60


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def fetch_url(url: str) -> bytes | None:
    req = Request(url, headers={"User-Agent": "epg-generator/1.0"})
    try:
        with urlopen(req, timeout=TIMEOUT) as r:
            return r.read()
    except URLError as exc:
        print(f"  WARNING: could not fetch {url}: {exc}", file=sys.stderr)
        return None


def fetch_xmltv(url: str) -> ET.Element | None:
    """Download a URL and parse as XMLTV.  Handles .gz compression."""
    print(f"  Fetching {url} ...")
    data = fetch_url(url)
    if data is None:
        return None
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    try:
        return ET.fromstring(data.decode("utf-8", errors="replace"))
    except ET.ParseError as exc:
        print(f"  WARNING: XML parse error for {url}: {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# XMLTV extraction
# ---------------------------------------------------------------------------

def extract_channels_and_programmes(
    root: ET.Element,
    wanted_ids: set[str],
) -> tuple[dict[str, ET.Element], list[ET.Element]]:
    channels: dict[str, ET.Element] = {}
    programmes: list[ET.Element] = []

    for ch in root.findall("channel"):
        cid = ch.get("id", "")
        if cid in wanted_ids:
            channels[cid] = ch

    for prog in root.findall("programme"):
        if prog.get("channel") in wanted_ids:
            programmes.append(prog)

    return channels, programmes


# ---------------------------------------------------------------------------
# Custom (24/7 loop) channel schedule
# ---------------------------------------------------------------------------

def generate_custom_programmes(ch: dict) -> list[ET.Element]:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    progs = []
    for day in range(CUSTOM_DAYS):
        for hour in range(24):
            start = today + timedelta(days=day, hours=hour)
            stop = start + timedelta(hours=1)
            prog = ET.Element("programme", {
                "start": start.strftime("%Y%m%d%H%M%S +0000"),
                "stop": stop.strftime("%Y%m%d%H%M%S +0000"),
                "channel": ch["id"],
            })
            ET.SubElement(prog, "title", lang="en").text = ch["title"]
            if ch.get("description"):
                ET.SubElement(prog, "desc", lang="en").text = ch["description"]
            progs.append(prog)
    return progs


# ---------------------------------------------------------------------------
# XML pretty-print
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Discover mode
# ---------------------------------------------------------------------------

def cmd_discover(url: str) -> None:
    root = fetch_xmltv(url)
    if root is None:
        sys.exit(1)
    channels = root.findall("channel")
    if not channels:
        print("No <channel> elements found in feed.")
        return
    print(f"\n{'ID':<40}  Display name")
    print("-" * 70)
    for ch in sorted(channels, key=lambda c: c.get("id", "")):
        cid = ch.get("id", "")
        names = [el.text for el in ch.findall("display-name") if el.text]
        print(f"{cid:<40}  {names[0] if names else '(no name)'}")
    print(f"\n{len(channels)} channels listed.")
    print("Copy the IDs you want into the 'live_channels' section of config.yaml.")


# ---------------------------------------------------------------------------
# Main generate
# ---------------------------------------------------------------------------

def cmd_generate() -> None:
    if not CONFIG_FILE.exists():
        sys.exit(f"Config not found: {CONFIG_FILE}")

    with open(CONFIG_FILE, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    sources: list[dict] = cfg.get("sources", [])
    live: list[dict] = cfg.get("live_channels", [])
    custom: list[dict] = cfg.get("custom_channels", [])

    wanted_ids = {ch["channel_id"] for ch in live}
    found_channels: dict[str, ET.Element] = {}
    found_programmes: list[ET.Element] = []

    # Fetch and extract from each source
    if sources and wanted_ids:
        print("Fetching live EPG sources...")
        for src in sources:
            root = fetch_xmltv(src["url"])
            if root is None:
                continue
            chs, progs = extract_channels_and_programmes(root, wanted_ids)
            found_channels.update(chs)
            found_programmes.extend(progs)
            print(f"  -> matched {len(chs)} channels, {len(progs)} programmes")

    # Build output
    out = ET.Element("tv", {
        "generator-info-name": "epg-generator",
        "generator-info-url": "https://github.com/ferryneil/crispy-umbrella",
    })

    # Live channel elements
    for cfg_ch in live:
        cid = cfg_ch["channel_id"]
        if cid in found_channels:
            out.append(found_channels[cid])
        else:
            # Source didn't return this channel — create a minimal stub
            el = ET.SubElement(out, "channel", id=cid)
            ET.SubElement(el, "display-name", lang="en").text = cfg_ch.get("display_name", cid)
            if cfg_ch.get("logo"):
                ET.SubElement(el, "icon", src=cfg_ch["logo"])

    # Custom channel elements
    for ch in custom:
        el = ET.SubElement(out, "channel", id=ch["id"])
        ET.SubElement(el, "display-name", lang="en").text = ch.get("display_name", ch["id"])
        if ch.get("logo"):
            ET.SubElement(el, "icon", src=ch["logo"])

    # Programmes from live sources
    for prog in found_programmes:
        out.append(prog)

    # Programmes for custom channels
    for ch in custom:
        for prog in generate_custom_programmes(ch):
            out.append(prog)

    indent(out)
    with open(OUTPUT_FILE, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        ET.ElementTree(out).write(f, encoding="utf-8", xml_declaration=False)

    size_kb = OUTPUT_FILE.stat().st_size // 1024
    missing = [ch["channel_id"] for ch in live if ch["channel_id"] not in found_channels]

    print(f"\nWritten {OUTPUT_FILE}  ({size_kb} KB)")
    print(f"  Live channels: {len(found_channels)}/{len(live)} matched, {len(found_programmes)} programmes")
    print(f"  Custom channels: {len(custom)}  ({CUSTOM_DAYS}-day dummy schedule)")
    if missing:
        print(f"\n  Channels not found in any source (check IDs with --discover):")
        for m in missing:
            print(f"    {m}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--discover", metavar="URL",
                        help="list all channel IDs available in a source feed and exit")
    args = parser.parse_args()

    if args.discover:
        cmd_discover(args.discover)
    else:
        cmd_generate()


if __name__ == "__main__":
    main()
