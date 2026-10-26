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
import shutil
import subprocess
import sys
from pathlib import Path

DIAGRAMS = Path(__file__).resolve().parent
BLOCK = DIAGRAMS.parent
ROOT = BLOCK.parents[2]
PROV_METADATA = BLOCK / "examples/prov/metadata"
PROV_TITLE = "CWLProv execution of the U-Net workflow (job d6f937f0)"


def render_interactions(dot: str) -> Path:
    """
    Render the Graphviz interaction graph to SVG.
    """
    output = DIAGRAMS / "bblocks-interactions.svg"
    subprocess.run([dot, "-Tsvg", str(DIAGRAMS / "bblocks-interactions.dot"), "-o", str(output)], check=True)
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
