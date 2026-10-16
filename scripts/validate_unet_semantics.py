"""Validate U-Net activity contracts and the separate execution enrichment.

Run in the resoterre environment with pySHACL >= 0.30. Older postprocessor images
use pySHACL 0.21, which does not enforce the upstream nested activity-type shapes.
"""

import json
from pathlib import Path
from urllib.request import urlopen

import pyshacl
from rdflib import DCTERMS, RDF, Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parents[1]
BLOCK = ROOT / "_sources/downscaling-unet/workflow"
REGISTER = "https://ogcincubator.github.io/registered-item-model/_sources/"
MODEL = "https://hirondelle.crim.ca/stac/collections/stac-mlm-examples/items/ogc-ospd2026-downscaling-unet"
MLACT = Namespace("https://w3id.org/ogc/rim/ml-activity/")
MLM = Namespace("https://w3id.org/ogc/stac/mlm/")
OA = Namespace("http://www.w3.org/ns/oa#")
PROV = Namespace("http://www.w3.org/ns/prov#")
SH = Namespace("http://www.w3.org/ns/shacl#")


def main() -> None:
    """
    Check positive and negative graphs, model selectors and captured-run identity.
    """
    if tuple(int(part) for part in pyshacl.__version__.split(".")[:2]) < (0, 30):
        raise RuntimeError("Use pySHACL >= 0.30 to enforce the upstream nested activity-type shapes.")
    shapes = Graph().parse(BLOCK / "shapes.shacl", format="turtle")
    closure = Graph()
    for block in ("core-ontology", "activity-type", "geoprocessing-activity-types", "ml-activity-types"):
        shapes.parse(f"{REGISTER}{block}/shapes.shacl", format="turtle")
        closure.parse(f"{REGISTER}{block}/ontology.ttl", format="turtle")
    for resource in ("activity-types.ttl", "examples/model-bindings.ttl"):
        closure.parse(BLOCK / resource, format="turtle")

    captured = Graph().parse(BLOCK / "examples/prov/metadata/provenance/primary.cwlprov.ttl")
    enrichment = Graph().parse(BLOCK / "examples/inference-enrichment.ttl")
    positive = closure + enrichment + captured
    conforms, _, report = pyshacl.validate(positive, shacl_graph=shapes, advanced=True)
    assert conforms, report
    print("PASS: activity definitions, bindings and enriched capture")

    expected_shapes = {
        "nonspatial-activity-fail.ttl": URIRef(
            "https://w3id.org/ogc/rim/geoprocessing/GeoprocessingActivityTypesShape"
        ),
        "missing-ml-output-type-fail.ttl": MLACT.InferenceActivityTypesShape,
        "missing-ml-specification-fail.ttl": MLACT.ActivityInputShape,
        "missing-inference-contract-fail.ttl": URIRef(
            "https://crim-ca.github.io/bblocks-process-profiles/def/InferenceExecutionShape"
        ),
    }
    fixtures = sorted((BLOCK / "tests").glob("*.ttl")) + sorted((BLOCK / "validation").glob("*.ttl"))
    for fixture in fixtures:
        graph = closure + Graph().parse(fixture)
        conforms, results, report = pyshacl.validate(graph, shacl_graph=shapes, advanced=True)
        assert not conforms, f"{fixture.name} unexpectedly passed"
        expected = expected_shapes[fixture.name]
        sources = {expected, *shapes.objects(expected, SH.property)}
        assert sources.intersection(results.objects(None, SH.sourceShape)), report
        print(f"PASS: {fixture.name} rejected by the expected shape")

    with urlopen(MODEL, timeout=60) as response:
        item = json.load(response)
    bindings = list(closure.subjects(RDF.type, OA.SpecificResource))
    assert len(bindings) == 3, "Expected two model input bindings and one output binding"
    for binding in bindings:
        selector = closure.value(binding, OA.hasSelector)
        pointer = str(closure.value(selector, RDF.value))
        value = item
        for token in pointer.lstrip("/").split("/"):
            key = token.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
        assert value["name"] == str(closure.value(binding, MLM.io_name)), pointer
    print("PASS: all three bindings select the named specifications in the published model")

    run = URIRef("urn:uuid:557e2aff-6780-4a25-aaa4-1b7100ceff82")
    assert (run, RDF.type, PROV.Activity) in captured
    assert (run, DCTERMS.type, URIRef(
        "https://crim-ca.github.io/bblocks-process-profiles/def/activity-type/climate-downscaling-inference"
    )) in enrichment
    assert not list(enrichment.triples((None, MLACT.accelerator, None)))
    assert not list(enrichment.triples((None, URIRef("https://w3id.org/ogc/rim/actionType"), None)))
    for entity in enrichment.subjects(DCTERMS.isPartOf, None):
        container = enrichment.value(entity, DCTERMS.isPartOf)
        assert (container, RDF.type, PROV.Entity) in captured
    print("PASS: capture identifiers reused; no CUDA or register-action claim introduced")


if __name__ == "__main__":
    main()
