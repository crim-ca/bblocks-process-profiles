#!/usr/bin/env python3
"""
Regenerate the diagrams of the downscaling-unet workflow block.

Two SVG files are written next to this script:

* ``bblocks-interactions.svg`` rendered from the Graphviz definition ``bblocks-interactions.dot``
  with ``dot``. Graphviz places the edge labels beside the lines, which Mermaid cannot do.
* ``execution-provenance.svg`` rendered by ``prov_synth.py`` from the CWLProv metadata
  captured in the workflow examples.

The viewer does not render diagram code blocks, so the block documentation references the SVG files.
The Graphviz definition remains the source of truth for the interaction graph.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

DIAGRAMS = Path(__file__).resolve().parent
BLOCK = DIAGRAMS.parent
ROOT = BLOCK.parents[2]
PROV_METADATA = BLOCK / "examples/prov/metadata"
PROV_TITLE = "CWLProv execution of the U-Net workflow (job d6f937f0)"


def join_waypoint_edges(svg: str) -> str:
    """
    Close the small gaps Graphviz leaves where an edge is split on invisible waypoint nodes.
    """
    pattern = re.compile(r'(<title>(?:[^<]*&#45;&gt;RPT|RPT&#45;&gt;RPT2|RPT2&#45;&gt;[^<]*)</title>\s*<path[^>]* d=")([^"]*)"')
    matches = list(pattern.finditer(svg))
    if len(matches) != 3:
        return svg
    first, middle, last = (m.group(2) for m in matches)
    first_end = re.findall(r"-?[\d.]+,-?[\d.]+", first)[-1]
    last_start = re.findall(r"-?[\d.]+,-?[\d.]+", last)[0]
    points = re.findall(r"-?[\d.]+,-?[\d.]+", middle)
    points[0], points[-1] = first_end, last_start
    fixed = f"M{points[0]}C" + " ".join(points[1:])
    return svg.replace(f'd="{middle}"', f'd="{fixed}"', 1)


def render_interactions(dot: str) -> Path:
    """
    Render the Graphviz interaction graph to SVG.
    """
    output = DIAGRAMS / "bblocks-interactions.svg"
    subprocess.run([dot, "-Tsvg", str(DIAGRAMS / "bblocks-interactions.dot"), "-o", str(output)], check=True)
    output.write_text(join_waypoint_edges(output.read_text(encoding="utf-8")), encoding="utf-8")
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
    parser.add_argument("--dot", default=shutil.which("dot"), help="path to the Graphviz dot executable")
    parser.add_argument("--only", choices=["interactions", "provenance"], help="render only one diagram")
    args = parser.parse_args()
    if args.only != "provenance":
        if not args.dot:
            parser.error("Graphviz dot is required, install it or use --dot")
        print(render_interactions(args.dot))
    if args.only != "interactions":
        print(render_provenance())
    return 0


if __name__ == "__main__":
    sys.exit(main())
