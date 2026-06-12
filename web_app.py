#!/usr/bin/env python3
"""
EPG Config Builder — web UI
Run: python web_app.py
Then open: http://localhost:5000
"""

import gzip
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from flask import Flask, jsonify, render_template, request

try:
    import yaml
except ImportError:
    sys.exit("Run: pip install pyyaml flask")

app = Flask(__name__)
CONFIG_FILE = Path(__file__).parent / "config.yaml"
TIMEOUT = 30

# ---------------------------------------------------------------------------
# M3U / EPG parsing helpers
# ---------------------------------------------------------------------------

def _attr(line: str, name: str) -> str:
    """Extract a quoted or unquoted attribute from an M3U/header line."""
    m = re.search(rf'{re.escape(name)}="([^"]*)"', line)
    if m:
        return m.group(1).strip()
    m = re.search(rf'{re.escape(name)}=([^\s,]+)', line)
    return m.group(1).strip() if m else ""


def parse_m3u(text: str) -> dict:
    epg_url = ""
    channels = []
    pending = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.upper().startswith("#EXTM3U"):
            epg_url = _attr(line, "url-tvg") or _attr(line, "x-tvg-url")

        elif line.upper().startswith("#EXTINF:"):
            display = line.rsplit(",", 1)[-1].strip() if "," in line else ""
            pending = {
                "tvg_id":      _attr(line, "tvg-id"),
                "tvg_name":    _attr(line, "tvg-name") or display,
                "tvg_logo":    _attr(line, "tvg-logo"),
                "group":       _attr(line, "group-title") or "Uncategorised",
                "display_name": display,
                "url":         "",
            }

        elif not line.startswith("#") and pending is not None:
            pending["url"] = line
            channels.append(pending)
            pending = None

    return {"epg_url": epg_url, "channels": channels}


def fetch_text(url: str) -> str | None:
    req = Request(url, headers={"User-Agent": "epg-config-builder/1.0"})
    try:
        with urlopen(req, timeout=TIMEOUT) as r:
            data = r.read()
    except URLError as exc:
        return None
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        try:
            data = gzip.decompress(data)
        except Exception:
            pass
    return data.decode("utf-8", errors="replace")


def epg_channels_from_xml(text: str) -> list[dict]:
    """Return [{id, name}] from an XMLTV string."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    result = []
    for ch in root.findall("channel"):
        cid = ch.get("id", "")
        names = [el.text for el in ch.findall("display-name") if el.text]
        result.append({"id": cid, "name": names[0] if names else cid})
    return sorted(result, key=lambda c: c["name"].lower())


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/load_m3u")
def api_load_m3u():
    url = (request.json or {}).get("url", "").strip()
    if not url:
        return jsonify(error="No URL provided"), 400

    text = fetch_text(url)
    if text is None:
        return jsonify(error=f"Could not fetch: {url}"), 502

    parsed = parse_m3u(text)
    categories = sorted({ch["group"] for ch in parsed["channels"]})
    return jsonify(
        epg_url=parsed["epg_url"],
        channels=parsed["channels"],
        categories=categories,
        count=len(parsed["channels"]),
    )


@app.post("/api/load_epg")
def api_load_epg():
    url = (request.json or {}).get("url", "").strip()
    if not url:
        return jsonify(error="No EPG URL provided"), 400

    text = fetch_text(url)
    if text is None:
        return jsonify(error=f"Could not fetch EPG: {url}"), 502

    channels = epg_channels_from_xml(text)
    return jsonify(channels=channels, count=len(channels))


@app.get("/api/config")
def api_get_config():
    if not CONFIG_FILE.exists():
        return jsonify(config=None)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return jsonify(config=yaml.safe_load(f))


@app.post("/api/save_config")
def api_save_config():
    body = request.json or {}
    new_live: list[dict] = body.get("live_channels", [])
    new_source: dict | None = body.get("source")  # {label, url}

    # Load existing config or start fresh
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    else:
        cfg = {}

    cfg.setdefault("sources", [])
    cfg.setdefault("live_channels", [])
    cfg.setdefault("custom_channels", [])

    # Merge / replace source
    if new_source and new_source.get("url"):
        existing_urls = {s.get("url") for s in cfg["sources"]}
        if new_source["url"] not in existing_urls:
            cfg["sources"].append(new_source)

    # Merge live channels — update existing entry or append
    existing_by_id = {ch["channel_id"]: ch for ch in cfg["live_channels"]}
    for ch in new_live:
        cid = ch["channel_id"]
        existing_by_id[cid] = ch  # overwrite / add
    cfg["live_channels"] = list(existing_by_id.values())

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return jsonify(
        ok=True,
        live_count=len(cfg["live_channels"]),
        source_count=len(cfg["sources"]),
    )


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("EPG Config Builder running at http://localhost:5000")
    app.run(debug=True, port=5000)
