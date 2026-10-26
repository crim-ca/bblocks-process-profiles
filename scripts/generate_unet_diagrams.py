#!/usr/bin/env python3
"""
Regenerate the diagrams of the downscaling-unet workflow block.

Two SVG files are written under ``_sources/downscaling-unet/workflow/diagrams``:

* ``bblocks-interactions.svg`` rendered from the Mermaid definition ``bblocks-interactions.mmd``
  with the Mermaid CLI (``mmdc``), which needs a Chrome or Chromium executable.
* ``execution-provenance.svg`` rendered by ``prov_synth.py`` from the CWLProv metadata
  captured in the workflow examples.

The viewer does not render Mermaid code blocks, so the block documentation references the SVG files.
The Mermaid definition remains the source of truth for the interaction graph.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = ROOT / "_sources/downscaling-unet/workflow"
DIAGRAMS = BLOCK / "diagrams"
PROV_METADATA = BLOCK / "examples/prov/metadata"
PROV_TITLE = "CWLProv execution of the U-Net workflow (job d6f937f0)"


def render_interactions(mmdc: str, chrome: str) -> Path:
    """
    Render the Mermaid interaction graph to SVG with plain-text labels.
    """
    output = DIAGRAMS / "bblocks-interactions.svg"
    with tempfile.TemporaryDirectory() as tmp:
        puppeteer = Path(tmp) / "puppeteer.json"
        puppeteer.write_text(json.dumps({"executablePath": chrome, "args": ["--no-sandbox"]}))
        config = Path(tmp) / "mermaid.json"
        config.write_text(json.dumps({"flowchart": {"htmlLabels": False}}))
        subprocess.run(
            [mmdc, "-p", str(puppeteer), "-c", str(config), "-b", "white",
             "-i", str(DIAGRAMS / "bblocks-interactions.mmd"), "-o", str(output)],
            check=True,
        )
    return output


def render_provenance() -> Path:
    """
    Render the synthetic view of the captured provenance.
    """
    output = DIAGRAMS / "execution-provenance.svg"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/prov_synth.py"), str(PROV_METADATA),
         "--profiles", str(DIAGRAMS / "prov-profiles.yaml"), "--title", PROV_TITLE, "-o", str(output)],
        check=True,
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mmdc", default=shutil.which("mmdc"), help="path to the Mermaid CLI")
    parser.add_argument("--chrome", default=shutil.which("google-chrome") or shutil.which("chromium"),
                        help="path to the Chrome or Chromium executable used by the Mermaid CLI")
    parser.add_argument("--only", choices=["interactions", "provenance"], help="render only one diagram")
    args = parser.parse_args()
    if args.only != "provenance":
        if not args.mmdc or not args.chrome:
            parser.error("the Mermaid CLI (--mmdc) and a Chrome executable (--chrome) are required")
        print(render_interactions(args.mmdc, args.chrome))
    if args.only != "interactions":
        print(render_provenance())
    return 0


if __name__ == "__main__":
    sys.exit(main())
