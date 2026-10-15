## RDPS-to-HRDPS U-Net downscaling

`ogc-ospd2026-downscaling-unet-workflow` runs the Resoterre climate downscaling pipeline:
it selects Regional Deterministic Prediction System (RDPS) forecast files for a requested time range,
downloads those files, and applies a trained U-Net to produce HRDPS-scale downscaled fields.
This workflow performs inference, not model training.

### Model and activity classification

The central operation is **machine-learning inference for climate-variable downscaling**.
The trained Resoterre U-Net is characterized by the **Resoterre RDPS to HRDPS U-Net MLM item**
in the [STAC Machine Learning Model block](bblocks://ogc.contrib.stac.extensions.mlm).
That example describes the model's inputs and outputs, tensor structures, training metadata,
runtime requirements and associated STAC extensions. The
[published model Item](https://hirondelle.crim.ca/stac/collections/stac-mlm-examples/items/ogc-ospd2026-downscaling-unet)
connects the executable process to that model characterization.
The [STAC Browser view](https://hirondelle.crim.ca/stac-browser/collections/stac-mlm-examples/items/ogc-ospd2026-downscaling-unet)
provides an interactive presentation of the same Item. Machine-readable model references use the STAC API URL.

The workflow is both an **ML activity** and a **geoprocessing activity**:
it applies a trained model to new inputs, making it an inference activity, and transforms
georeferenced RDPS climate fields into finer-resolution HRDPS-scale fields, making it spatial
data processing. These are complementary classifications of the same operation, not alternative
labels. The workflow references the
[ML activity types profile](bblocks://ogc.model.registered-item.ml-activity-types) and
[geoprocessing activity types profile](bblocks://ogc.model.registered-item.geoprocessing-activity-types);
its process-type example records the climate-downscaling and climate-downscaling-inference
activity types. File selection and download prepare the model inputs rather than train the model.

### Processing steps

The sequence follows the descriptions and input/output contracts of the three component processes:

1. [Generate file list](bblocks://ospd.process-profiles.downscaling-unet.generate-file-list)
   (`ogc-ospd2026-downscaling-generate-file-list`) selects the RDPS forecast files needed to cover
   `start_datetime` through `end_datetime`. It prepends `data_root` to each file reference and writes
   the `forecast_files` text file. `requires_previous_forecast_step` includes the preceding forecast
   step needed for cumulative variables such as precipitation. `include_year_month_subdirectory`
   controls whether the paths include year/month directories or use a flat layout.
2. [Download files](bblocks://ospd.process-profiles.downscaling-unet.download-files)
   (`ogc-ospd2026-downscaling-download-files`) reads the file list and downloads its entries into
   the working directory exposed as `input_data`. Its process description supports HTTP(S) URLs
   and local paths accessible from the execution container.
3. [U-Net inference](bblocks://ospd.process-profiles.downscaling-unet.unet)
   (`ogc-ospd2026-downscaling-unet`) reads the input NetCDF directory and runs RDPS-to-HRDPS
   downscaling over the requested time range. The inference image includes the trained model,
   regridding matrices, geophysical fields, and default configuration. An optional `config` YAML
   file overrides that configuration; the workflow also passes the requested start/end datetimes.

### Inputs and results

The required inputs are `start_datetime` and `end_datetime`. Optional inputs control forecast-step
selection, source path layout, the data root, and the inference configuration.
The workflow returns `forecast_files`, the selected source-file list, and `inference_output`,
a Zarr directory containing the inference results. The downloaded NetCDF directory is an intermediate
passed between the download and inference steps, not a separate workflow output.

### Execution examples and provenance

The **Examples** tab includes the CWL workflow application package, its OGC API process description,
the Application Package deployment reference and the process-type register entry linking the
workflow to its model and activity classifications. The **execution request** example provides
the JSON `inputs` body for the illustrated 2024-05-02 time range, the process execution endpoint,
and headers for asynchronous submission. The optional configuration is omitted to use the
inference image's default configuration.

The **CWLProv execution provenance** example records job
`d6f937f0-bdae-4dd5-9fa3-9e0686ed6715`, captured on 2026-09-28. It describes the workflow
and individual step runs, their plans, input/output entities, associated agents and PROV
relationships. Turtle, expanded JSON-LD, N-Triples, PROV-JSON, PROV-N and PROV-XML representations
are provided with links to their definitions in
[the PROV representation register](https://ogcincubator.github.io/bblocks-prov-jsonld-alt/).
The captured packed CWL and job-input document are also linked from that example, so the execution
metadata can be inspected alongside the workflow and submitted input values. The supplied metadata
are not a complete BagIt archive of the execution's data payloads.

The provenance content aligns with the process, job, input/output and agent relationships described
in [draft OGC API - Processes - Part 5: Provenance](https://docs.ogc.org/DRAFTS/26-038.html).
Metadata alignment does not by itself establish server conformance to that draft.
