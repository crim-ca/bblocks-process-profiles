
# Process profile: OSPD 2026 RDPS-to-HRDPS U-Net downscaling step `ogc-ospd2026-downscaling-download-files` (Schema)

`ospd.process-profiles.downscaling-unet.download-files` *v0.1*

OGC API - Processes profile of the Resoterre CWL CommandLineTool `ogc-ospd2026-downscaling-download-files`, a step of the RDPS-to-HRDPS U-Net downscaling workflow.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Source CWL
CWL CommandLineTool deployed as `ogc-ospd2026-downscaling-download-files`. The resoterre tag `0.1.3-dev.10` counterpart is <https://github.com/Ouranosinc/resoterre/blob/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_download_files.cwl>.
#### cwl
```cwl
cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  s: "https://schema.org/"
  iana: "https://www.iana.org/assignments/media-types/"
  edam: "http://edamontology.org/"

id: ogc-ospd2026-downscaling-download-files
label: Download listed files
doc: |
  Download every file referenced in a file list into the output working directory.
  Entries can be HTTP(S) URLs or local paths reachable from the container.

s:dateCreated: "2026-09-04T11:45:32-04:00"
s:version: "0.1.3.dev10"
s:softwareVersion: "v0.1.3-dev.10"
s:codeRepository: "https://github.com/Ouranosinc/resoterre"
s:license: "https://spdx.org/licenses/Apache-2.0"
s:citation: "https://github.com/Ouranosinc/resoterre/blob/v0.1.3-dev.10/CITATION.cff"
s:releaseNotes: "https://github.com/Ouranosinc/resoterre/blob/v0.1.3-dev.10/CHANGELOG.rst"

s:author:
  - class: s:Person
    s:identifier: "https://orcid.org/0009-0004-9049-2092"
    s:email: gauvin-st-denis.blaise@ouranos.ca
    s:name: Blaise Gauvin St-Denis
    s:affiliation: Ouranos
  - class: s:Person
    s:identifier: "https://orcid.org/0000-0001-5393-8359"
    s:email: smith.trevorj@ouranos.ca
    s:name: Trevor James Smith
    s:affiliation: Ouranos
s:contributor:
  - class: s:Person
    s:identifier: "https://orcid.org/0000-0003-4862-3349"
    s:email: francis.charette-migneault@luqia.ca
    s:name: Francis Charette-Migneault
    s:affiliation: Technologies Luqia
  - class: s:Person
    s:email: nazim.azeli@luqia.ca
    s:name: Nazim Azeli
    s:affiliation: Technologies Luqia

s:keywords:
  - RDPS
  - download
  - downscaling

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

```


### processDescription
OGC API - Processes processDescription returned by Weaver for the deployed CWL.
#### json
```json
{
  "id": "ogc-ospd2026-downscaling-download-files",
  "version": "0.1.3.dev10",
  "title": "Download listed files",
  "description": "Download every file referenced in a file list into the output working directory.\nEntries can be HTTP(S) URLs or local paths reachable from the container.\n",
  "mutable": true,
  "keywords": [
    "RDPS",
    "downscaling",
    "download",
    "application"
  ],
  "metadata": [
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0009-0004-9049-2092",
        "email": "gauvin-st-denis.blaise@ouranos.ca",
        "name": "Blaise Gauvin St-Denis",
        "affiliation": "Ouranos"
      },
      "role": "https://schema.org/author"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0000-0001-5393-8359",
        "email": "smith.trevorj@ouranos.ca",
        "name": "Trevor James Smith",
        "affiliation": "Ouranos"
      },
      "role": "https://schema.org/author"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff",
      "type": "text/plain",
      "rel": "https://schema.org/citation"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre",
      "type": "text/html",
      "rel": "https://schema.org/codeRepository"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0000-0003-4862-3349",
        "email": "francis.charette-migneault@luqia.ca",
        "name": "Francis Charette-Migneault",
        "affiliation": "Technologies Luqia"
      },
      "role": "https://schema.org/contributor"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "email": "nazim.azeli@luqia.ca",
        "name": "Nazim Azeli",
        "affiliation": "Technologies Luqia"
      },
      "role": "https://schema.org/contributor"
    },
    {
      "value": "2026-09-04T11:45:32-04:00",
      "role": "https://schema.org/dateCreated"
    },
    {
      "href": "https://spdx.org/licenses/Apache-2.0",
      "type": "text/plain",
      "rel": "https://schema.org/license"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst",
      "type": "text/plain",
      "rel": "https://schema.org/releaseNotes"
    }
  ],
  "inputs": {
    "file_list": {
      "title": "file_list",
      "description": "Text file holding one file reference per line.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "contentMediaType": "text/plain"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "text/plain"
        }
      ]
    }
  },
  "outputs": {
    "input_data": {
      "title": "input_data",
      "description": "Directory holding the downloaded files, ready to be used as the UNet input_data.",
      "schema": {
        "type": "string",
        "format": "binary",
        "contentMediaType": "application/directory",
        "contentEncoding": "base64"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "application/directory"
        }
      ]
    }
  },
  "jobControlOptions": [
    "async-execute"
  ],
  "outputTransmission": [
    "reference",
    "value"
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/download-files/context.jsonld",
  "id": "ogc-ospd2026-downscaling-download-files",
  "version": "0.1.3.dev10",
  "title": "Download listed files",
  "description": "Download every file referenced in a file list into the output working directory.\nEntries can be HTTP(S) URLs or local paths reachable from the container.\n",
  "mutable": true,
  "keywords": [
    "RDPS",
    "downscaling",
    "download",
    "application"
  ],
  "metadata": [
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0009-0004-9049-2092",
        "email": "gauvin-st-denis.blaise@ouranos.ca",
        "name": "Blaise Gauvin St-Denis",
        "affiliation": "Ouranos"
      },
      "role": "https://schema.org/author"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0000-0001-5393-8359",
        "email": "smith.trevorj@ouranos.ca",
        "name": "Trevor James Smith",
        "affiliation": "Ouranos"
      },
      "role": "https://schema.org/author"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff",
      "type": "text/plain",
      "rel": "https://schema.org/citation"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre",
      "type": "text/html",
      "rel": "https://schema.org/codeRepository"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "identifier": "https://orcid.org/0000-0003-4862-3349",
        "email": "francis.charette-migneault@luqia.ca",
        "name": "Francis Charette-Migneault",
        "affiliation": "Technologies Luqia"
      },
      "role": "https://schema.org/contributor"
    },
    {
      "value": {
        "$schema": "https://schema.org/Person",
        "email": "nazim.azeli@luqia.ca",
        "name": "Nazim Azeli",
        "affiliation": "Technologies Luqia"
      },
      "role": "https://schema.org/contributor"
    },
    {
      "value": "2026-09-04T11:45:32-04:00",
      "role": "https://schema.org/dateCreated"
    },
    {
      "href": "https://spdx.org/licenses/Apache-2.0",
      "type": "text/plain",
      "rel": "https://schema.org/license"
    },
    {
      "href": "https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst",
      "type": "text/plain",
      "rel": "https://schema.org/releaseNotes"
    }
  ],
  "inputs": {
    "file_list": {
      "title": "file_list",
      "description": "Text file holding one file reference per line.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "contentMediaType": "text/plain"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "text/plain"
        }
      ]
    }
  },
  "outputs": {
    "input_data": {
      "title": "input_data",
      "description": "Directory holding the downloaded files, ready to be used as the UNet input_data.",
      "schema": {
        "type": "string",
        "format": "binary",
        "contentMediaType": "application/directory",
        "contentEncoding": "base64"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "application/directory"
        }
      ]
    }
  },
  "jobControlOptions": [
    "async-execute"
  ],
  "outputTransmission": [
    "reference",
    "value"
  ]
}
```

#### ttl
```ttl
@prefix : <https://crim-ca.github.io/bblocks-process-profiles/def/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <https://crim-ca.github.io/bblocks-process-profiles/def/$> .
@prefix ns2: <https://w3id.org/ogc/api/schema/> .
@prefix ns3: <pp:> .
@prefix proc: <https://w3id.org/ogc/api/processes/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-download-files> dcterms:description """Download every file referenced in a file list into the output working directory.
Entries can be HTTP(S) URLs or local paths reachable from the container.
""" ;
    dcterms:title "Download listed files" ;
    :inputs [ proc:file_list [ dcterms:description "Text file holding one file reference per line." ;
                    dcterms:title "file_list" ;
                    proc:formats [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "text/plain" ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 1 ;
                    proc:schema [ proc:type "string" ;
                            ns2:contentMediaType "text/plain" ] ] ] ;
    :jobControlOptions "async-execute" ;
    :metadata [ :role "https://schema.org/author" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "smith.trevorj@ouranos.ca" ;
                    :identifier "https://orcid.org/0000-0001-5393-8359" ;
                    :name "Trevor James Smith" ] ],
        [ :role "https://schema.org/dateCreated" ;
            :value "2026-09-04T11:45:32-04:00" ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "nazim.azeli@luqia.ca" ;
                    :name "Nazim Azeli" ] ],
        [ :role "https://schema.org/author" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "gauvin-st-denis.blaise@ouranos.ca" ;
                    :identifier "https://orcid.org/0009-0004-9049-2092" ;
                    :name "Blaise Gauvin St-Denis" ] ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "francis.charette-migneault@luqia.ca" ;
                    :identifier "https://orcid.org/0000-0003-4862-3349" ;
                    :name "Francis Charette-Migneault" ] ],
        <https://github.com/Ouranosinc/resoterre>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff>,
        <https://spdx.org/licenses/Apache-2.0> ;
    :mutable true ;
    :outputTransmission "reference",
        "value" ;
    :outputs [ proc:input_data [ dcterms:description "Directory holding the downloaded files, ready to be used as the UNet input_data." ;
                    dcterms:title "input_data" ;
                    proc:formats [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "application/directory" ] ;
                    proc:schema [ proc:type "string" ;
                            ns2:contentEncoding "base64" ;
                            ns2:contentMediaType "application/directory" ;
                            ns2:format "binary" ] ] ] ;
    proc:keywords "RDPS",
        "application",
        "download",
        "downscaling" ;
    ns3:version "0.1.3.dev10" .

<https://github.com/Ouranosinc/resoterre> a <https://crim-ca.github.io/bblocks-process-profiles/def/text/html> ;
    :rel "https://schema.org/codeRepository" .

<https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst> a <https://crim-ca.github.io/bblocks-process-profiles/def/text/plain> ;
    :rel "https://schema.org/releaseNotes" .

<https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff> a <https://crim-ca.github.io/bblocks-process-profiles/def/text/plain> ;
    :rel "https://schema.org/citation" .

<https://spdx.org/licenses/Apache-2.0> a <https://crim-ca.github.io/bblocks-process-profiles/def/text/plain> ;
    :rel "https://schema.org/license" .


```


### OGC Application Package (deploy)
Part 2 deploy body: the execution unit is a link to the CWL pinned at the resoterre `0.1.3-dev.10` tag commit.
#### json
```json
{
  "processDescription": {
    "process": {
      "id": "ogc-ospd2026-downscaling-download-files",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_download_files.cwl",
    "type": "application/cwl+yaml",
    "rel": "http://www.opengis.net/def/rel/ogc/1.0/executionUnit"
  }
}

```

#### jsonld
```jsonld
{
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/download-files/context.jsonld",
  "processDescription": {
    "process": {
      "id": "ogc-ospd2026-downscaling-download-files",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_download_files.cwl",
    "type": "application/cwl+yaml",
    "rel": "http://www.opengis.net/def/rel/ogc/1.0/executionUnit"
  }
}
```

#### ttl
```ttl
@prefix : <https://crim-ca.github.io/bblocks-process-profiles/def/> .
@prefix ns1: <pp:> .
@prefix proc: <https://w3id.org/ogc/api/processes/> .

<https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_download_files.cwl> a <https://crim-ca.github.io/bblocks-process-profiles/def/application/cwl+yaml> ;
    :rel "http://www.opengis.net/def/rel/ogc/1.0/executionUnit" .

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-download-files> ns1:version "0.1.3.dev10" .

[] :processDescription [ ns1:process <https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-download-files> ] ;
    proc:executionUnit <https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_download_files.cwl> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Profile of the OGC API - Processes processDescription of `ogc-ospd2026-downscaling-download-files`
  (CWL CommandLineTool), step of the Resoterre RDPS-to-HRDPS U-Net downscaling workflow.
  Pins the process id and the input/output names; the input/output schemas are those
  derived from the CWL.
allOf:
- $ref: https://ogcincubator.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/process/schema.yaml
- $ref: https://geolabs.github.io/bblock-ogcapi-processes-part2/build/annotated/api/processes/v2/schemas/staticIndicator/schema.yaml
- type: object
  required:
  - id
  - version
  - inputs
  - outputs
  properties:
    id:
      const: ogc-ospd2026-downscaling-download-files
      x-jsonld-id: '@id'
    inputs:
      type: object
      required:
      - file_list
      propertyNames:
        enum:
        - file_list
    outputs:
      type: object
      required:
      - input_data
      propertyNames:
        enum:
        - input_data
$defs:
  rawProcessDescription:
    $ref: https://ogcincubator.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/process/schema.yaml
  applicationPackage:
    $ref: https://geolabs.github.io/bblock-ogcapi-processes-part2/build/annotated/api/processes/v2/schemas/ogcapppkg/schema.yaml
x-jsonld-extra-terms:
  cwl:
    x-jsonld-id: pp:cwl
    x-jsonld-type: '@id'
  type: '@type'
  title: http://purl.org/dc/terms/title
  description: http://purl.org/dc/terms/description
  version: pp:version
  process:
    x-jsonld-id: pp:process
    x-jsonld-type: '@id'
  executionUnit:
    x-jsonld-id: https://w3id.org/ogc/api/processes/executionUnit
    x-jsonld-type: '@id'
  href: '@id'
  activityTypes:
    x-jsonld-id: pp:activityType
    x-jsonld-type: '@id'
    x-jsonld-container: '@set'
  inRegister:
    x-jsonld-id: https://w3id.org/ogc/rim/inRegister
    x-jsonld-type: '@id'
  source: pp:source
  cwlClass: pp:cwlClass
  cwlId: pp:cwlId
x-jsonld-vocab: https://crim-ca.github.io/bblocks-process-profiles/def/
x-jsonld-prefixes:
  dct: http://purl.org/dc/terms/
  proc: https://w3id.org/ogc/api/processes/
  rim: https://w3id.org/ogc/rim/
  mlact: https://w3id.org/ogc/rim/ml-activity/
  geoproc: https://w3id.org/ogc/rim/geoprocessing/

```

Links to the schema:

* YAML version: [schema.yaml](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/download-files/schema.json)
* JSON version: [schema.json](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/download-files/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "@vocab": "https://crim-ca.github.io/bblocks-process-profiles/def/",
    "inputs": {
      "@context": {
        "@vocab": "https://w3id.org/ogc/api/processes/",
        "schema": {
          "@context": {
            "@vocab": "https://w3id.org/ogc/api/schema/"
          },
          "@id": "proc:schema"
        },
        "type": "proc:type"
      }
    },
    "outputs": {
      "@context": {
        "@vocab": "https://w3id.org/ogc/api/processes/",
        "schema": {
          "@context": {
            "@vocab": "https://w3id.org/ogc/api/schema/"
          },
          "@id": "proc:schema"
        },
        "type": "proc:type"
      }
    },
    "id": "@id",
    "cwl": {
      "@id": "pp:cwl",
      "@type": "@id"
    },
    "type": "@type",
    "title": "dct:title",
    "description": "dct:description",
    "version": "pp:version",
    "process": {
      "@id": "pp:process",
      "@type": "@id"
    },
    "executionUnit": {
      "@id": "proc:executionUnit",
      "@type": "@id"
    },
    "href": "@id",
    "activityTypes": {
      "@id": "pp:activityType",
      "@type": "@id",
      "@container": "@set"
    },
    "inRegister": {
      "@id": "rim:inRegister",
      "@type": "@id"
    },
    "source": "pp:source",
    "cwlClass": "pp:cwlClass",
    "cwlId": "pp:cwlId",
    "keywords": "proc:keywords",
    "nullable": "proc:nullable",
    "$ref": {
      "@id": "proc:ref",
      "@type": "@id"
    },
    "default": {
      "@id": "proc:default",
      "@type": "@json"
    },
    "enum": {
      "@id": "proc:enum",
      "@container": "@set"
    },
    "minOccurs": "proc:minOccurs",
    "maxOccurs": "proc:maxOccurs",
    "dct": "http://purl.org/dc/terms/",
    "proc": "https://w3id.org/ogc/api/processes/",
    "rim": "https://w3id.org/ogc/rim/",
    "mlact": "rim:ml-activity/",
    "geoproc": "rim:geoprocessing/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/download-files/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/crim-ca/bblocks-process-profiles](https://github.com/crim-ca/bblocks-process-profiles)
* Path: `_sources/downscaling-unet/download-files`

