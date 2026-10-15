
# Process profile: OSPD 2026 RDPS-to-HRDPS U-Net downscaling step `ogc-ospd2026-downscaling-generate-file-list` (Schema)

`ospd.process-profiles.downscaling-unet.generate-file-list` *v0.1*

OGC API - Processes profile of the Resoterre CWL CommandLineTool `ogc-ospd2026-downscaling-generate-file-list`, a step of the RDPS-to-HRDPS U-Net downscaling workflow.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Source CWL
CWL CommandLineTool deployed as `ogc-ospd2026-downscaling-generate-file-list`. The resoterre tag `0.1.3-dev.10` counterpart is <https://github.com/Ouranosinc/resoterre/blob/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_generate_file_list.cwl>.
#### cwl
```cwl
cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  s: "https://schema.org/"
  iana: "https://www.iana.org/assignments/media-types/"
  edam: "http://edamontology.org/"

id: ogc-ospd2026-downscaling-generate-file-list
label: List RDPS forecast files
doc: |
  List the RDPS forecast files required to cover the requested datetime range.
  Each listed file is prefixed with the provided data root so the result can be
  consumed directly by the download step.

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
  - forecast
  - file listing
  - downscaling

requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: registry.gitlab.com/crim.ca/clients/ogc/ogc-ospd2026/resoterre-base:0.1.3-dev.10

baseCommand: [python3, -c]

arguments:
  - |
      from datetime import datetime
      from resoterre.experiments.rdps_to_hrdps_downscaling.rdps_to_hrdps_workflow import rdps_datetimes_to_forecast_files
      import sys
      start_datetime = datetime.fromisoformat(sys.argv[1])
      end_datetime = datetime.fromisoformat(sys.argv[2])
      files = rdps_datetimes_to_forecast_files(
          start_datetime,
          end_datetime,
          requires_previous_forecast_step=sys.argv[3] == "1",
          include_year_month_subdirectory=sys.argv[4] == "1",
      )
      data_root = sys.argv[5].rstrip("/")
      print("\n".join(f"{data_root}/{path}" if data_root else str(path) for path in files))

inputs:
  start_datetime:
    type: string
    doc: Start datetime in ISO 8601 format, for example 2024-05-01T07:00:00.
    inputBinding:
      position: 2
  end_datetime:
    type: string
    doc: End datetime in ISO 8601 format, for example 2024-05-01T08:00:00.
    inputBinding:
      position: 3
  requires_previous_forecast_step:
    type: boolean
    default: true
    doc: |
      Whether the previous forecast step is required. Must be true for cumulative variables,
      such as precipitation.
    inputBinding:
      position: 4
      valueFrom: '$(self ? "1" : "0")'
  include_year_month_subdirectory:
    type: boolean
    default: true
    doc: |
      Whether the file paths include the year/month subdirectory, as on thredds (true),
      or are stored in a flat directory (false).
    inputBinding:
      position: 5
      valueFrom: '$(self ? "1" : "0")'
  data_root:
    type: string
    default: "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/"
    doc: |
      Root location prepended to each listed file. Set to an empty string to get relative paths.
    inputBinding:
      position: 6

outputs:
  forecast_files:
    type: File
    format: iana:text/plain
    outputBinding:
      glob: rdps_forecast_files.txt

stdout: rdps_forecast_files.txt

```


### processDescription
OGC API - Processes processDescription returned by Weaver for the deployed CWL.
#### json
```json
{
  "id": "ogc-ospd2026-downscaling-generate-file-list",
  "version": "0.1.3.dev10",
  "title": "List RDPS forecast files",
  "description": "List the RDPS forecast files required to cover the requested datetime range.\nEach listed file is prefixed with the provided data root so the result can be\nconsumed directly by the download step.\n",
  "mutable": true,
  "keywords": [
    "RDPS",
    "forecast",
    "file listing",
    "downscaling",
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
    "start_datetime": {
      "description": "Start datetime in ISO 8601 format, for example 2024-05-01T07:00:00.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string"
      },
      "literalDataDomains": [
        {
          "default": true,
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "end_datetime": {
      "description": "End datetime in ISO 8601 format, for example 2024-05-01T08:00:00.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string"
      },
      "literalDataDomains": [
        {
          "default": true,
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "requires_previous_forecast_step": {
      "description": "Whether the previous forecast step is required. Must be true for cumulative variables,\nsuch as precipitation.\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "boolean",
        "default": true
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": true,
          "dataType": {
            "name": "boolean"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "include_year_month_subdirectory": {
      "description": "Whether the file paths include the year/month subdirectory, as on thredds (true),\nor are stored in a flat directory (false).\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "boolean",
        "default": true
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": true,
          "dataType": {
            "name": "boolean"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "data_root": {
      "description": "Root location prepended to each listed file. Set to an empty string to get relative paths.\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "default": "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/"
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/",
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    }
  },
  "outputs": {
    "forecast_files": {
      "title": "forecast_files",
      "schema": {
        "oneOf": [
          {
            "type": "string",
            "contentMediaType": "text/plain"
          },
          {
            "type": "string",
            "contentMediaType": "text/html"
          },
          {
            "type": "string",
            "format": "binary",
            "contentMediaType": "application/pdf",
            "contentEncoding": "base64"
          }
        ]
      },
      "formats": [
        {
          "default": true,
          "mediaType": "text/plain"
        },
        {
          "mediaType": "text/html"
        },
        {
          "mediaType": "application/pdf"
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
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/generate-file-list/context.jsonld",
  "id": "ogc-ospd2026-downscaling-generate-file-list",
  "version": "0.1.3.dev10",
  "title": "List RDPS forecast files",
  "description": "List the RDPS forecast files required to cover the requested datetime range.\nEach listed file is prefixed with the provided data root so the result can be\nconsumed directly by the download step.\n",
  "mutable": true,
  "keywords": [
    "RDPS",
    "forecast",
    "file listing",
    "downscaling",
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
    "start_datetime": {
      "description": "Start datetime in ISO 8601 format, for example 2024-05-01T07:00:00.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string"
      },
      "literalDataDomains": [
        {
          "default": true,
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "end_datetime": {
      "description": "End datetime in ISO 8601 format, for example 2024-05-01T08:00:00.",
      "minOccurs": 1,
      "maxOccurs": 1,
      "schema": {
        "type": "string"
      },
      "literalDataDomains": [
        {
          "default": true,
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "requires_previous_forecast_step": {
      "description": "Whether the previous forecast step is required. Must be true for cumulative variables,\nsuch as precipitation.\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "boolean",
        "default": true
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": true,
          "dataType": {
            "name": "boolean"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "include_year_month_subdirectory": {
      "description": "Whether the file paths include the year/month subdirectory, as on thredds (true),\nor are stored in a flat directory (false).\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "boolean",
        "default": true
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": true,
          "dataType": {
            "name": "boolean"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    },
    "data_root": {
      "description": "Root location prepended to each listed file. Set to an empty string to get relative paths.\n",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "default": "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/"
      },
      "literalDataDomains": [
        {
          "default": true,
          "defaultValue": "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/",
          "dataType": {
            "name": "string"
          },
          "valueDefinition": {
            "anyValue": false
          }
        }
      ]
    }
  },
  "outputs": {
    "forecast_files": {
      "title": "forecast_files",
      "schema": {
        "oneOf": [
          {
            "type": "string",
            "contentMediaType": "text/plain"
          },
          {
            "type": "string",
            "contentMediaType": "text/html"
          },
          {
            "type": "string",
            "format": "binary",
            "contentMediaType": "application/pdf",
            "contentEncoding": "base64"
          }
        ]
      },
      "formats": [
        {
          "default": true,
          "mediaType": "text/plain"
        },
        {
          "mediaType": "text/html"
        },
        {
          "mediaType": "application/pdf"
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

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-generate-file-list> dcterms:description """List the RDPS forecast files required to cover the requested datetime range.
Each listed file is prefixed with the provided data root so the result can be
consumed directly by the download step.
""" ;
    dcterms:title "List RDPS forecast files" ;
    :inputs [ proc:data_root [ dcterms:description """Root location prepended to each listed file. Set to an empty string to get relative paths.
""" ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "string" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:defaultValue "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/" ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:default "\"https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/\""^^rdf:JSON ;
                            proc:type "string" ] ] ;
            proc:end_datetime [ dcterms:description "End datetime in ISO 8601 format, for example 2024-05-01T08:00:00." ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "string" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 1 ;
                    proc:schema [ proc:type "string" ] ] ;
            proc:include_year_month_subdirectory [ dcterms:description """Whether the file paths include the year/month subdirectory, as on thredds (true),
or are stored in a flat directory (false).
""" ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "boolean" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:defaultValue true ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:default "true"^^rdf:JSON ;
                            proc:type "boolean" ] ] ;
            proc:requires_previous_forecast_step [ dcterms:description """Whether the previous forecast step is required. Must be true for cumulative variables,
such as precipitation.
""" ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "boolean" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:defaultValue true ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:default "true"^^rdf:JSON ;
                            proc:type "boolean" ] ] ;
            proc:start_datetime [ dcterms:description "Start datetime in ISO 8601 format, for example 2024-05-01T07:00:00." ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "string" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 1 ;
                    proc:schema [ proc:type "string" ] ] ] ;
    :jobControlOptions "async-execute" ;
    :metadata [ :role "https://schema.org/dateCreated" ;
            :value "2026-09-04T11:45:32-04:00" ],
        [ :role "https://schema.org/author" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "gauvin-st-denis.blaise@ouranos.ca" ;
                    :identifier "https://orcid.org/0009-0004-9049-2092" ;
                    :name "Blaise Gauvin St-Denis" ] ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "nazim.azeli@luqia.ca" ;
                    :name "Nazim Azeli" ] ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "francis.charette-migneault@luqia.ca" ;
                    :identifier "https://orcid.org/0000-0003-4862-3349" ;
                    :name "Francis Charette-Migneault" ] ],
        [ :role "https://schema.org/author" ;
            :value [ ns1:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "smith.trevorj@ouranos.ca" ;
                    :identifier "https://orcid.org/0000-0001-5393-8359" ;
                    :name "Trevor James Smith" ] ],
        <https://github.com/Ouranosinc/resoterre>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff>,
        <https://spdx.org/licenses/Apache-2.0> ;
    :mutable true ;
    :outputTransmission "reference",
        "value" ;
    :outputs [ proc:forecast_files [ dcterms:title "forecast_files" ;
                    proc:formats [ proc:mediaType "text/html" ],
                        [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "text/plain" ],
                        [ proc:mediaType "application/pdf" ] ;
                    proc:schema [ ns2:oneOf [ proc:type "string" ;
                                    ns2:contentMediaType "text/html" ],
                                [ proc:type "string" ;
                                    ns2:contentEncoding "base64" ;
                                    ns2:contentMediaType "application/pdf" ;
                                    ns2:format "binary" ],
                                [ proc:type "string" ;
                                    ns2:contentMediaType "text/plain" ] ] ] ] ;
    proc:keywords "RDPS",
        "application",
        "downscaling",
        "file listing",
        "forecast" ;
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
      "id": "ogc-ospd2026-downscaling-generate-file-list",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_generate_file_list.cwl",
    "type": "application/cwl+yaml",
    "rel": "http://www.opengis.net/def/rel/ogc/1.0/executionUnit"
  }
}

```

#### jsonld
```jsonld
{
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/generate-file-list/context.jsonld",
  "processDescription": {
    "process": {
      "id": "ogc-ospd2026-downscaling-generate-file-list",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_generate_file_list.cwl",
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

<https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_generate_file_list.cwl> a <https://crim-ca.github.io/bblocks-process-profiles/def/application/cwl+yaml> ;
    :rel "http://www.opengis.net/def/rel/ogc/1.0/executionUnit" .

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-generate-file-list> ns1:version "0.1.3.dev10" .

[] :processDescription [ ns1:process <https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-generate-file-list> ] ;
    proc:executionUnit <https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_generate_file_list.cwl> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Profile of the OGC API - Processes processDescription of `ogc-ospd2026-downscaling-generate-file-list`
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
      const: ogc-ospd2026-downscaling-generate-file-list
      x-jsonld-id: '@id'
    inputs:
      type: object
      required:
      - start_datetime
      - end_datetime
      propertyNames:
        enum:
        - start_datetime
        - end_datetime
        - requires_previous_forecast_step
        - include_year_month_subdirectory
        - data_root
    outputs:
      type: object
      required:
      - forecast_files
      propertyNames:
        enum:
        - forecast_files
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

* YAML version: [schema.yaml](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/generate-file-list/schema.json)
* JSON version: [schema.json](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/generate-file-list/schema.yaml)


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
[context.jsonld](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/generate-file-list/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/crim-ca/bblocks-process-profiles](https://github.com/crim-ca/bblocks-process-profiles)
* Path: `_sources/downscaling-unet/generate-file-list`

