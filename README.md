# bblocks-process-profiles

OGC Building Blocks register holding **process profiles** for the deployable CWL processes of the
OSPD 2026 reference workflows, plus Geonovum testbed operation profiles and an ML-based climate
downscaling workflow (CRIM fork additions). Identifier prefix: `ospd.process-profiles.`

This fork ([`crim-ca/bblocks-process-profiles`](https://github.com/crim-ca/bblocks-process-profiles))
tracks [`GeoLabs/bblocks-process-profiles`](https://github.com/GeoLabs/bblocks-process-profiles)
and adds the `downscaling-unet` group (see below) together with its model and activity-type
semantics. Other workflows are inherited from the GeoLabs repository, where some originate
back from previous CRIM contributions in earlier OSPD phases.

The CRIM fork supplies additional connectors to other OGC Building Blocks that are relevant for the
description of the Machine Learning based workflow, as well as semantics for integration with the ProcessType Registered Item.
It also provides relationships that allows profiling the process against its simultanous GeoAI (GeoproessingActivityType + MLActivityType) considerations.


| Workflow | Source (linked, not copied) |
|---|---|
| W1 Algae Bloom | [`crim-ca/ogc-ospd-phase1@5edd4ec`](https://github.com/crim-ca/ogc-ospd-phase1/tree/5edd4ec4cbd21e5fceb7c3f4b6c5d0ce809a57ea/ogc_app_pkg) (CC-BY-NC-SA-4.0) |
| W2 KindGrove | [`GeoLabs/bblocks-eoap-cct@291a741`](https://github.com/GeoLabs/bblocks-eoap-cct/blob/291a741c3f2b61da7607f1dbb7a777134374227d/_sources/cwl-to-ogcprocess/examples/mangrove-workflow.cwl) |
| W3 Water Bodies | [`GeoLabs/ogc-eo-application-package-hands-on@f472585`](https://github.com/GeoLabs/ogc-eo-application-package-hands-on/tree/f47258567ddf8efbc7c33fd1ec277e4f1b454883/water-bodies/app-pkg-multiple) (license unassigned upstream and in this fork; CC-BY-SA-4.0 assumed, see `scripts/sources.yaml` `w3`; tool images from `Terradue/ogc-eo-application-package-hands-on`) |
| W2b KindGrove (step notebooks) | [`GeoLabs/KindGrove` release `v0.0.2-rc2`](https://github.com/GeoLabs/KindGrove/releases/tag/v0.0.2-rc2) (CC-BY-NC-SA-4.0; prerelease, a GitHub Release asset pinned by sha256 rather than a git commit — the CWL is never committed to the repo tree, see `scripts/sources.yaml` `kindgrove_steps`). A ground-up reimplementation added alongside `kindgrove`, not replacing it — see `docs/WORKFLOW-COMPARISON.md` |
| OSPD 2026 Downscaling (CRIM) | [`Ouranosinc/resoterre@f08a79b`](https://github.com/Ouranosinc/resoterre/tree/f08a79b9a1906a8752c5774b050e90f81f2d1bcb/examples/deploy) (CWL pinned at the `0.1.3-dev.10` development line). Deployed on Weaver as `ogc-ospd2026-downscaling-*`. The model is described by the STAC MLM Item [`ogc-ospd2026-downscaling-unet`](https://hirondelle.crim.ca/stac/collections/stac-mlm-examples/items/ogc-ospd2026-downscaling-unet) |

## Building blocks

| Identifier | CWL class | Phase(s) | openEO |
|---|---|---|---|
| `ospd.process-profiles.algae-bloom.workflow-earth-search` | Workflow | Filter configuration, Selection / filtering, Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.algae-bloom.workflow-earth-search-process` | Workflow | Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.algae-bloom.workflow-copernicus` | Workflow | Filter configuration, Selection / filtering, Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.algae-bloom.workflow-copernicus-process` | Workflow | Data retrieval, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.algae-bloom.select-products-sentinel2` | CommandLineTool | Selection / filtering | closeMatch: processes.cubes.load_collection |
| `ospd.process-profiles.algae-bloom.download-band-sentinel2-stac-item` | CommandLineTool | Data retrieval | closeMatch: processes.cubes.load_collection, processes.cubes.filter_bands |
| `ospd.process-profiles.algae-bloom.download-band-sentinel2-product-safe` | CommandLineTool | Data retrieval | closeMatch: processes.cubes.load_collection, processes.cubes.filter_bands |
| `ospd.process-profiles.algae-bloom.reproject-image` | CommandLineTool | Pre-processing | closeMatch: processes.cubes.resample_spatial |
| `ospd.process-profiles.algae-bloom.calculate-band` | CommandLineTool | Scientific computation | closeMatch: processes.cubes.reduce_dimension |
| `ospd.process-profiles.algae-bloom.plot-image` | CommandLineTool | Export / aggregation | closeMatch: processes.cubes.save_result |
| `ospd.process-profiles.kindgrove.mangrove-workflow` | Workflow | Filter configuration, Selection / filtering, Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.kindgrove.parse-aoi` | CommandLineTool | Filter configuration | none |
| `ospd.process-profiles.kindgrove.mangrove` | CommandLineTool | Selection / filtering, Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.water-bodies.water-bodies` | Workflow | Data retrieval, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.water-bodies.detect-water-body` | Workflow | Data retrieval, Scientific computation | none |
| `ospd.process-profiles.water-bodies.crop` | CommandLineTool | Data retrieval | closeMatch: processes.cubes.load_collection, processes.cubes.filter_bands |
| `ospd.process-profiles.water-bodies.norm-diff` | CommandLineTool | Scientific computation | closeMatch: processes.math.indices.normalized_difference |
| `ospd.process-profiles.water-bodies.otsu` | CommandLineTool | Scientific computation | none |
| `ospd.process-profiles.water-bodies.stac` | CommandLineTool | Export / aggregation | closeMatch: processes.cubes.save_result |
| `ospd.process-profiles.kindgrove-steps.mangrove-workflow-steps` | Workflow | Filter configuration, Selection / filtering, Data retrieval, Pre-processing, Scientific computation, Export / aggregation | none |
| `ospd.process-profiles.kindgrove-steps.parse-aoi-steps` | CommandLineTool | Filter configuration | none |
| `ospd.process-profiles.kindgrove-steps.select-scene` | CommandLineTool | Selection / filtering | closeMatch: processes.cubes.load_collection |
| `ospd.process-profiles.kindgrove-steps.download-band` | CommandLineTool | Data retrieval | closeMatch: processes.cubes.load_collection, processes.cubes.filter_bands |
| `ospd.process-profiles.kindgrove-steps.reproject-band` | CommandLineTool | Pre-processing | closeMatch: processes.cubes.resample_spatial |
| `ospd.process-profiles.kindgrove-steps.calculate-indices` | CommandLineTool | Scientific computation | none |
| `ospd.process-profiles.kindgrove-steps.estimate-biomass` | CommandLineTool | Scientific computation | none |
| `ospd.process-profiles.kindgrove-steps.export-stac` | CommandLineTool | Export / aggregation | closeMatch: processes.cubes.save_result |

### OSPD 2026 RDPS-to-HRDPS U-Net downscaling (CRIM fork)

| Identifier | CWL class | Role |
|---|---|---|
| `ospd.process-profiles.downscaling-unet.workflow` | Workflow | Highlighted workflow profile: process, Application Package, provenance, process type, MLM and activity types |
| `ospd.process-profiles.downscaling-unet.generate-file-list` | CommandLineTool | Builds the RDPS forecast file list |
| `ospd.process-profiles.downscaling-unet.download-files` | CommandLineTool | Downloads the listed RDPS files |
| `ospd.process-profiles.downscaling-unet.unet` | CommandLineTool | U-Net inference producing the HRDPS-resolution Zarr |

The workflow block adds, beyond the common artefacts above:

- ML and geoprocessing activity types, with SHACL shapes, reusing `ogc.model.registered-item.*`
  and the STAC `mlm` extension (`ogc.contrib.stac.extensions.mlm`)
- an interaction graph of the blocks and example artefacts and a synthetic view of the captured provenance,
  generated with `_sources/downscaling-unet/workflow/diagrams/generate_diagrams.py` (Graphviz and `scripts/prov_synth.py`)
- model-domain spatial and temporal extents derived from the MLM Item, as GeoSPARQL and OWL-Time
- bindings of the MLM inputs, outputs and structure to the workflow, and a link between the
  Application Package plan and the captured CWLProv plan

### Geonovum testbed operations (GeoLabs)

`ospd.process-profiles.{sqlmm,raster,vector,terrain,pointcloud}.*` hold implementation profiles of
SQL/MM, raster, vector, terrain and point cloud operations, built on the imported
[`bblocks-generic-profiles`](https://geolabs.github.io/bblocks-generic-profiles/build/register.json)
register.

Shared: `ospd.process-profiles.process-type` — schema of a candidate process-type register entry (Activity 4).

## What each process profile contains

| Artefact | Validated against |
|---|---|
| `processDescription` (default schema) | this profile = `ogc.api.processes.v1.schemas.process` + `ogc.api.processes.v2.schemas.staticIndicator` + id/input/output constraints |
| raw `cwl-to-ogcprocess` output (when a manual correction was needed) | `ogc.api.processes.v1.schemas.process` |
| OGC Application Package (Part 2 deploy body, `executionUnit` = link to the CWL) | `ogc.api.processes.v2.schemas.ogcapppkg` |
| execute request / results | `ogc.api.processes.v1.schemas.execute` / `results` |
| provenance chain | `ogc.bbr.provenance.provenance` |
| process run (CommandLineTool) | `ogc.bbr.wf4ever.wfprov.ProcessRun` (gap GP-1 in the generic profile) |
| execution bundle (Workflow) | `ogc.bbr.provenance.execution` |
| process-type entry | `ospd.process-profiles.process-type` |

## Documentation

- [docs/DEVIATIONS.md](docs/DEVIATIONS.md) — deviations from / gaps in `eoap.cct.cwl-to-ogcprocess`
- [docs/PROVENANCE-GAPS.md](docs/PROVENANCE-GAPS.md) — gaps in `bblocks-generic-provenance-profile`
- [docs/OPENEO-EQUIVALENCES.md](docs/OPENEO-EQUIVALENCES.md) — equivalence decisions and criteria
- [docs/WORKFLOW-COMPARISON.md](docs/WORKFLOW-COMPARISON.md) — structural parallels and differences across W1/W2/W3
- [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md)
- [docs/VALIDATION.md](docs/VALIDATION.md) — validation status (Docker build passing, 63/63)
- `_sources/downscaling-unet/workflow/description.md` — downscaling workflow, MLM bindings and semantics

## Regenerating

```bash
# needs jq, python3 (pyyaml, prov>=2 for the W3C PROV-JSONLD examples), git, cwltool + Docker
python3 scripts/run_workflows.py --sources-root DIR --runs-root DIR --build-images --generate
#   clones the pinned sources (scripts/sources.yaml `repo:`/`commit:`, or downloads+checksums a
#   `release:` source) under --sources-root when missing, runs each entry under `runs:` with
#   `cwltool --provenance` (asks for the Copernicus S3 credentials, or reads
#   CDSE_S3_ACCESS_KEY / CDSE_S3_SECRET_KEY), stores the research objects under --runs-root as
#   named in `runs:`, then regenerates; --only NAME picks runs, --force replaces an existing bag,
#   --no-fetch leaves the clones/downloads alone
python3 scripts/generate.py --sources-root DIR --runs-root DIR   # regenerate only, never downloads
python3 scripts/validate_offline.py --deps-root ../   # pre-check only
./build.sh                                             # authoritative validation (Docker)
python3 _sources/downscaling-unet/workflow/validation/validate_semantics.py           # SHACL/RDF checks of the downscaling workflow (CRIM)
./view.sh                                              # http://localhost:9090
```

Generated files are overwritten; hand-written content lives in `scripts/profiles.yaml` and `docs/`.
The run-derived examples (times, engine, container images, output names and checksums) are read
from real `cwltool --provenance` research objects declared under `runs:` in `scripts/sources.yaml`;
those are local directories (the W1 one carries a 3.1 GB payload) and are not part of this
repository. Without them the generator stops.

## License

Apache-2.0 for this register. The W1 and W2b CWL files are CC-BY-NC-SA-4.0 and are **referenced by
URL only**.
