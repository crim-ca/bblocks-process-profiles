cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
  iana: "https://www.iana.org/assignments/media-types/"
  edam: "http://edamontology.org/"

id: ogc-ospd2026-downscaling-unet
doc: |
  Run the RDPS to HRDPS U-Net downscaling inference over the provided input directory.
  The model, regridding matrices, geophysical fields and default configuration are baked
  into the inference image.

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
