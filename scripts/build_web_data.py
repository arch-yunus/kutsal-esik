#!/usr/bin/env python3
"""
scripts/build_web_data.py
Veri (data/*.json) ve döküman (docs/*.md) dosyalarını web/js/data.js dosyasına derler.
"""

import json
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    docs_dir = root / "docs"

    quotes = json.loads((data_dir / "quotes.json").read_text(encoding="utf-8"))
    concepts = json.loads((data_dir / "concepts.json").read_text(encoding="utf-8"))
    timeline = json.loads((data_dir / "timeline.json").read_text(encoding="utf-8"))
    traditions = json.loads((data_dir / "traditions.json").read_text(encoding="utf-8"))
    bibliography = json.loads((data_dir / "bibliography.json").read_text(encoding="utf-8"))

    docs = {}
    for md_file in sorted(docs_dir.glob("*.md")):
        docs[md_file.stem] = md_file.read_text(encoding="utf-8")

    bundle = {
        "quotes": quotes,
        "concepts": concepts,
        "timeline": timeline,
        "traditions": traditions,
        "bibliography": bibliography,
        "docs": docs,
    }

    out_path = root / "web" / "js" / "data.js"
    out_path.write_text(
        "window.KUTSAL_ESIK_DATA = " + json.dumps(bundle, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(f"[OK] Web veri paketi basariyla derlendi: {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
