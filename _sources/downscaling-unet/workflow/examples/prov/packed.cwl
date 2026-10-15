{
  "cwlVersion": "v1.2",
  "class": "Workflow",
  "id": "ogc-ospd2026-downscaling-unet-workflow",
  "doc": "Chain the RDPS forecast file listing with the UNet downscaling inference.\nThe first step derives the RDPS files required for the requested datetime range,\nthe second step downloads them into a local directory and the last step runs the\ninference on that directory.\n",
  "inputs": [
    {
      "type": "string",
      "id": "start_datetime",
      "doc": "Start datetime in ISO 8601 format, for example 2024-05-01T07:00:00."
    },
    {
      "type": "string",
      "id": "end_datetime",
      "doc": "End datetime in ISO 8601 format, for example 2024-05-01T08:00:00."
    },
    {
      "type": "boolean",
      "default": true,
      "id": "requires_previous_forecast_step",
      "doc": "Whether the previous forecast step is required. Must be true for cumulative variables,\nsuch as precipitation.\n"
    },
    {
      "type": "boolean",
      "default": true,
      "id": "include_year_month_subdirectory",
      "doc": "Whether the listed paths include the year/month subdirectory, as on thredds (true),\nor are stored in a flat directory (false).\n"
    },
    {
      "type": "string",
      "default": "https://pavics.ouranos.ca/twitcher/ows/proxy/thredds/fileServer/birdhouse/disk3/ouranos/geoconnections/RDPS/",
      "id": "data_root",
      "doc": "Root location prepended to each listed file, used to download the RDPS files."
    },
    {
      "type": [
        "null",
        "File"
      ],
      "id": "config",
      "format": [
        "iana:application/yaml",
        "edam:format_3750"
      ],
      "doc": "Optional inference configuration YAML overriding the one built into the Docker image."
    }
  ],
  "outputs": [
    {
      "type": "File",
      "id": "forecast_files",
      "format": "iana:text/plain",
      "outputSource": "ogc-ospd2026-downscaling-generate-file-list/forecast_files"
    },
    {
      "type": "Directory",
      "id": "inference_output",
      "outputSource": "ogc-ospd2026-downscaling-unet/inference_output"
    }
  ],
  "steps": {
    "ogc-ospd2026-downscaling-generate-file-list": {
      "in": {
        "start_datetime": "start_datetime",
        "end_datetime": "end_datetime",
        "requires_previous_forecast_step": "requires_previous_forecast_step",
        "include_year_month_subdirectory": "include_year_month_subdirectory",
        "data_root": "data_root"
      },
      "out": [
        "forecast_files"
      ],
      "run": "ogc-ospd2026-downscaling-generate-file-list"
    },
    "ogc-ospd2026-downscaling-download-files": {
      "in": {
        "file_list": "ogc-ospd2026-downscaling-generate-file-list/forecast_files"
      },
      "out": [
        "input_data"
      ],
      "run": "ogc-ospd2026-downscaling-download-files",
      "doc": "Download the listed RDPS files into a flat local directory."
    },
    "ogc-ospd2026-downscaling-unet": {
      "in": {
        "config": "config",
        "input_data": "ogc-ospd2026-downscaling-download-files/input_data",
        "start_datetime": "start_datetime",
        "end_datetime": "end_datetime"
      },
      "out": [
        "inference_output"
      ],
      "run": "ogc-ospd2026-downscaling-unet"
    }
  },
  "$namespaces": {
    "edam": "http://edamontology.org/",
    "iana": "https://www.iana.org/assignments/media-types/"
  }
}