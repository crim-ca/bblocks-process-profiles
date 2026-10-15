
# Process profile: OSPD 2026 RDPS-to-HRDPS U-Net downscaling step `ogc-ospd2026-downscaling-unet` (Schema)

`ospd.process-profiles.downscaling-unet.unet` *v0.1*

OGC API - Processes profile of the Resoterre CWL CommandLineTool `ogc-ospd2026-downscaling-unet`, a step of the RDPS-to-HRDPS U-Net downscaling workflow.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Source CWL
CWL CommandLineTool deployed as `ogc-ospd2026-downscaling-unet`. The resoterre tag `0.1.3-dev.10` counterpart is <https://github.com/Ouranosinc/resoterre/blob/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_unet.cwl>.
#### cwl
```cwl
cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  s: "https://schema.org/"
  cwltool: "http://commonwl.org/cwltool#"
  iana: "https://www.iana.org/assignments/media-types/"
  edam: "http://edamontology.org/"

id: ogc-ospd2026-downscaling-unet
label: RDPS-to-HRDPS U-Net downscaling inference
doc: |
  Run the RDPS to HRDPS U-Net downscaling inference over the provided input directory.
  The model, regridding matrices, geophysical fields and default configuration are baked
  into the inference image.

s:dateCreated: "2026-01-30T10:42:53-05:00"
s:version: "0.1.3.dev10"
s:softwareVersion: "v0.1.3-dev.10"
s:codeRepository: "https://github.com/Ouranosinc/resoterre"
s:license: "https://spdx.org/licenses/Apache-2.0"
s:citation: "https://github.com/Ouranosinc/resoterre/blob/v0.1.3-dev.10/CITATION.cff"
s:releaseNotes: "https://github.com/Ouranosinc/resoterre/blob/v0.1.3-dev.10/CHANGELOG.rst"
s:isBasedOn: "https://raw.githubusercontent.com/Ouranosinc/resoterre/v0.1.3-dev.10/notebooks/ml-model-package/unet_rdps_to_hrdps/unet_rdps_to_hrdps.json"

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
  - HRDPS
  - downscaling
  - super-resolution
  - U-Net
  - machine learning
  - inference
  - climate

requirements:
  InlineJavascriptRequirement: {}

  EnvVarRequirement:
    envDef:
      # to fix KeyError: 'getpwuid(): uid not found: 13798' in pytorch caching
      TORCHINDUCTOR_CACHE_DIR: "/tmp/torch_cache"
      HOME: "/tmp"
      USER: "cwluser"

  DockerRequirement:
    dockerPull: registry.gitlab.com/crim.ca/clients/ogc/ogc-ospd2026/resoterre-inference:0.1.3-dev.10

  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.config)
        entryname: config.yaml
        writable: false
      - entry: $(inputs.input_data)
        entryname: inputs
        writable: false

hints:
  cwltool:CUDARequirement:
    cudaComputeCapability: '3.0'
    cudaDeviceCountMax: 8
    cudaDeviceCountMin: 1
    cudaVersionMin: '11.4'

baseCommand: []

inputs:
  config:
    type: ["null", File]
    format:
    - "iana:application/yaml"
    - "edam:format_3750"
    doc: Inference configuration YAML
    inputBinding:
      position: 1
      prefix: --config
      valueFrom: config_yaml=config.yaml

  start_datetime:
    type: ["null", string]
    doc: Optional start datetime (ISO 8601) overriding the config's inference_start_datetime
    inputBinding:
      position: 2
      valueFrom: '$(self ? "start_datetime=" + self : null)'

  end_datetime:
    type: ["null", string]
    doc: Optional end datetime (ISO 8601) overriding the config's inference_end_datetime
    inputBinding:
      position: 3
      valueFrom: '$(self ? "end_datetime=" + self : null)'

  input_data:
    type: Directory
    doc: Directory containing input NetCDF files to be used for inference

  number_of_cores:
    type: boolean
    default: true
    doc: Internal flag; always emits -j1 to set the number of cores used for inference.
    inputBinding:
      position: 4
      valueFrom: "-j1"

  output_directory:
    type: boolean
    default: true
    doc: Internal flag; injects the runtime-determined output directory into the command line.
    inputBinding:
      position: 5
      valueFrom: '$("--directory=" + runtime.outdir)'

outputs:
  inference_output:
    type: Directory
    doc: Zarr output directory containing inference results
    outputBinding:
      # no trailing slash: a trailing slash collapses the glob to "." and clobbers sibling outputs
      glob: outputs/inference_*.zarr

```


### processDescription
OGC API - Processes processDescription returned by Weaver for the deployed CWL.
#### json
```json
{
  "id": "ogc-ospd2026-downscaling-unet",
  "version": "0.1.3.dev10",
  "title": "RDPS-to-HRDPS U-Net downscaling inference",
  "description": "Run the RDPS to HRDPS U-Net downscaling inference over the provided input directory.\nThe model, regridding matrices, geophysical fields and default configuration are baked\ninto the inference image.\n",
  "mutable": true,
  "keywords": [
    "inference",
    "U-Net",
    "HRDPS",
    "machine learning",
    "downscaling",
    "RDPS",
    "super-resolution",
    "climate",
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
      "value": "2026-01-30T10:42:53-05:00",
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
    "config": {
      "title": "config",
      "description": "Inference configuration YAML",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "contentMediaType": "application/yaml"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "application/yaml"
        }
      ]
    },
    "start_datetime": {
      "description": "Optional start datetime (ISO 8601) overriding the config's inference_start_datetime",
      "minOccurs": 0,
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
      "description": "Optional end datetime (ISO 8601) overriding the config's inference_end_datetime",
      "minOccurs": 0,
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
    "input_data": {
      "title": "input_data",
      "description": "Directory containing input NetCDF files to be used for inference",
      "minOccurs": 1,
      "maxOccurs": 1,
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
    },
    "number_of_cores": {
      "description": "Internal flag; always emits -j1 to set the number of cores used for inference.",
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
    "output_directory": {
      "description": "Internal flag; injects the runtime-determined output directory into the command line.",
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
    }
  },
  "outputs": {
    "inference_output": {
      "title": "inference_output",
      "description": "Zarr output directory containing inference results",
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
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/unet/context.jsonld",
  "id": "ogc-ospd2026-downscaling-unet",
  "version": "0.1.3.dev10",
  "title": "RDPS-to-HRDPS U-Net downscaling inference",
  "description": "Run the RDPS to HRDPS U-Net downscaling inference over the provided input directory.\nThe model, regridding matrices, geophysical fields and default configuration are baked\ninto the inference image.\n",
  "mutable": true,
  "keywords": [
    "inference",
    "U-Net",
    "HRDPS",
    "machine learning",
    "downscaling",
    "RDPS",
    "super-resolution",
    "climate",
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
      "value": "2026-01-30T10:42:53-05:00",
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
    "config": {
      "title": "config",
      "description": "Inference configuration YAML",
      "minOccurs": 0,
      "maxOccurs": 1,
      "schema": {
        "type": "string",
        "contentMediaType": "application/yaml"
      },
      "formats": [
        {
          "default": true,
          "mediaType": "application/yaml"
        }
      ]
    },
    "start_datetime": {
      "description": "Optional start datetime (ISO 8601) overriding the config's inference_start_datetime",
      "minOccurs": 0,
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
      "description": "Optional end datetime (ISO 8601) overriding the config's inference_end_datetime",
      "minOccurs": 0,
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
    "input_data": {
      "title": "input_data",
      "description": "Directory containing input NetCDF files to be used for inference",
      "minOccurs": 1,
      "maxOccurs": 1,
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
    },
    "number_of_cores": {
      "description": "Internal flag; always emits -j1 to set the number of cores used for inference.",
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
    "output_directory": {
      "description": "Internal flag; injects the runtime-determined output directory into the command line.",
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
    }
  },
  "outputs": {
    "inference_output": {
      "title": "inference_output",
      "description": "Zarr output directory containing inference results",
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
@prefix ns1: <https://w3id.org/ogc/api/schema/> .
@prefix ns2: <https://crim-ca.github.io/bblocks-process-profiles/def/$> .
@prefix ns3: <pp:> .
@prefix proc: <https://w3id.org/ogc/api/processes/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-unet> dcterms:description """Run the RDPS to HRDPS U-Net downscaling inference over the provided input directory.
The model, regridding matrices, geophysical fields and default configuration are baked
into the inference image.
""" ;
    dcterms:title "RDPS-to-HRDPS U-Net downscaling inference" ;
    :inputs [ proc:config [ dcterms:description "Inference configuration YAML" ;
                    dcterms:title "config" ;
                    proc:formats [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "application/yaml" ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:type "string" ;
                            ns1:contentMediaType "application/yaml" ] ] ;
            proc:end_datetime [ dcterms:description "Optional end datetime (ISO 8601) overriding the config's inference_end_datetime" ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "string" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:type "string" ] ] ;
            proc:input_data [ dcterms:description "Directory containing input NetCDF files to be used for inference" ;
                    dcterms:title "input_data" ;
                    proc:formats [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "application/directory" ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 1 ;
                    proc:schema [ proc:type "string" ;
                            ns1:contentEncoding "base64" ;
                            ns1:contentMediaType "application/directory" ;
                            ns1:format "binary" ] ] ;
            proc:number_of_cores [ dcterms:description "Internal flag; always emits -j1 to set the number of cores used for inference." ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "boolean" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:defaultValue true ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:default "true"^^rdf:JSON ;
                            proc:type "boolean" ] ] ;
            proc:output_directory [ dcterms:description "Internal flag; injects the runtime-determined output directory into the command line." ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "boolean" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:defaultValue true ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:default "true"^^rdf:JSON ;
                            proc:type "boolean" ] ] ;
            proc:start_datetime [ dcterms:description "Optional start datetime (ISO 8601) overriding the config's inference_start_datetime" ;
                    proc:literalDataDomains [ proc:dataType [ proc:name "string" ] ;
                            proc:default "true"^^rdf:JSON ;
                            proc:valueDefinition [ proc:anyValue false ] ] ;
                    proc:maxOccurs 1 ;
                    proc:minOccurs 0 ;
                    proc:schema [ proc:type "string" ] ] ] ;
    :jobControlOptions "async-execute" ;
    :metadata [ :role "https://schema.org/dateCreated" ;
            :value "2026-01-30T10:42:53-05:00" ],
        [ :role "https://schema.org/author" ;
            :value [ ns2:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "gauvin-st-denis.blaise@ouranos.ca" ;
                    :identifier "https://orcid.org/0009-0004-9049-2092" ;
                    :name "Blaise Gauvin St-Denis" ] ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns2:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "francis.charette-migneault@luqia.ca" ;
                    :identifier "https://orcid.org/0000-0003-4862-3349" ;
                    :name "Francis Charette-Migneault" ] ],
        [ :role "https://schema.org/author" ;
            :value [ ns2:schema "https://schema.org/Person" ;
                    :affiliation "Ouranos" ;
                    :email "smith.trevorj@ouranos.ca" ;
                    :identifier "https://orcid.org/0000-0001-5393-8359" ;
                    :name "Trevor James Smith" ] ],
        [ :role "https://schema.org/contributor" ;
            :value [ ns2:schema "https://schema.org/Person" ;
                    :affiliation "Technologies Luqia" ;
                    :email "nazim.azeli@luqia.ca" ;
                    :name "Nazim Azeli" ] ],
        <https://github.com/Ouranosinc/resoterre>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CHANGELOG.rst>,
        <https://github.com/Ouranosinc/resoterre/blob/0.1.3-dev.10/CITATION.cff>,
        <https://spdx.org/licenses/Apache-2.0> ;
    :mutable true ;
    :outputTransmission "reference",
        "value" ;
    :outputs [ proc:inference_output [ dcterms:description "Zarr output directory containing inference results" ;
                    dcterms:title "inference_output" ;
                    proc:formats [ proc:default "true"^^rdf:JSON ;
                            proc:mediaType "application/directory" ] ;
                    proc:schema [ proc:type "string" ;
                            ns1:contentEncoding "base64" ;
                            ns1:contentMediaType "application/directory" ;
                            ns1:format "binary" ] ] ] ;
    proc:keywords "HRDPS",
        "RDPS",
        "U-Net",
        "application",
        "climate",
        "downscaling",
        "inference",
        "machine learning",
        "super-resolution" ;
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
      "id": "ogc-ospd2026-downscaling-unet",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_unet.cwl",
    "type": "application/cwl+yaml",
    "rel": "http://www.opengis.net/def/rel/ogc/1.0/executionUnit"
  }
}

```

#### jsonld
```jsonld
{
  "@context": "https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/unet/context.jsonld",
  "processDescription": {
    "process": {
      "id": "ogc-ospd2026-downscaling-unet",
      "version": "0.1.3.dev10"
    }
  },
  "executionUnit": {
    "href": "https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_unet.cwl",
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

<https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_unet.cwl> a <https://crim-ca.github.io/bblocks-process-profiles/def/application/cwl+yaml> ;
    :rel "http://www.opengis.net/def/rel/ogc/1.0/executionUnit" .

<https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-unet> ns1:version "0.1.3.dev10" .

[] :processDescription [ ns1:process <https://hirondelle.crim.ca/weaver/processes/ogc-ospd2026-downscaling-unet> ] ;
    proc:executionUnit <https://github.com/Ouranosinc/resoterre/raw/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy/downscaling_unet.cwl> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Profile of the OGC API - Processes processDescription of `ogc-ospd2026-downscaling-unet`
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
      const: ogc-ospd2026-downscaling-unet
      x-jsonld-id: '@id'
    inputs:
      type: object
      required:
      - input_data
      propertyNames:
        enum:
        - config
        - start_datetime
        - end_datetime
        - input_data
        - number_of_cores
        - output_directory
    outputs:
      type: object
      required:
      - inference_output
      propertyNames:
        enum:
        - inference_output
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

* YAML version: [schema.yaml](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/unet/schema.json)
* JSON version: [schema.json](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/unet/schema.yaml)


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
[context.jsonld](https://crim-ca.github.io/bblocks-process-profiles/build/annotated/process-profiles/downscaling-unet/unet/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/crim-ca/bblocks-process-profiles](https://github.com/crim-ca/bblocks-process-profiles)
* Path: `_sources/downscaling-unet/unet`

