cwlVersion: v1.2
class: CommandLineTool
s:version: "0.1.3.dev10"
$namespaces:
  s: https://schema.org/
  iana: "https://www.iana.org/assignments/media-types/"
  edam: "http://edamontology.org/"

id: ogc-ospd2026-downscaling-download-files
doc: |
  Download every file referenced in a file list into the output working directory.
  Entries can be HTTP(S) URLs or local paths reachable from the container.

requirements:
  NetworkAccess:
    networkAccess: true
  DockerRequirement:
    dockerPull: registry.gitlab.com/crim.ca/clients/ogc/ogc-ospd2026/resoterre-base:0.1.3-dev.10

baseCommand: [python3, -c]

arguments:
  - |
      import shutil
      import sys
      import urllib.request
      from pathlib import Path
      from urllib.parse import urlparse
      destination = Path(".")
      references = [line.strip() for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
      for reference in references:
          target = destination / reference.rsplit("/", 1)[-1]
          scheme = urlparse(reference).scheme
          if scheme in ("http", "https"):
              with urllib.request.urlopen(reference) as response, target.open("wb") as handle:
                  shutil.copyfileobj(response, handle)
          else:
              source = reference[len("file://"):] if scheme == "file" else reference
              shutil.copyfile(source, target)
          print(f"{reference} -> {target}", file=sys.stderr)

inputs:
  file_list:
    type: File
    format: iana:text/plain
    doc: Text file holding one file reference per line.
    inputBinding:
      position: 2

outputs:
  input_data:
    type: Directory
    doc: Directory holding the downloaded files, ready to be used as the UNet input_data.
    outputBinding:
      glob: "."
