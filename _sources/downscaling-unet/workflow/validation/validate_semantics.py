"""Validate U-Net activity contracts and the separate execution enrichment.

Run in the resoterre environment with pySHACL >= 0.30, from any directory. Older postprocessor images
use pySHACL 0.21, which does not enforce the upstream nested activity-type shapes.
"""

import json
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

import pyshacl
from rdflib import DCTERMS, RDF, Graph, Literal, Namespace, URIRef

BLOCK = Path(__file__).resolve().parents[1]
REGISTER = "https://ogcincubator.github.io/registered-item-model/_sources/"
MODEL = "https://hirondelle.crim.ca/stac/collections/stac-mlm-examples/items/ogc-ospd2026-downscaling-unet"
MLACT = Namespace("https://w3id.org/ogc/rim/ml-activity/")
MLM = Namespace("https://w3id.org/ogc/stac/mlm/")
OA = Namespace("http://www.w3.org/ns/oa#")
PROV = Namespace("http://www.w3.org/ns/prov#")
SH = Namespace("http://www.w3.org/ns/shacl#")
BINDING = Namespace("https://crim-ca.github.io/bblocks-process-profiles/def/model-binding/downscaling-unet/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
TIME = Namespace("http://www.w3.org/2006/time#")
PP = Namespace("https://crim-ca.github.io/bblocks-process-profiles/def/")


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

    domain_cases = (
        (BINDING["model-spatial-domain"], GEO.asWKT, PP.ModelSpatialDomainShape),
        (BINDING["model-start"], TIME.inXSDDateTimeStamp, PP.ModelTemporalEndpointShape),
        (BINDING["model-end"], TIME.inXSDDateTimeStamp, PP.ModelTemporalEndpointShape),
        (URIRef(
            "https://crim-ca.github.io/bblocks-process-profiles/def/activity-type/climate-downscaling-inference"
        ), DCTERMS.temporal, PP.ModelApplicabilityShape),
        (URIRef(
            "https://crim-ca.github.io/bblocks-process-profiles/def/run/"
            "d6f937f0-bdae-4dd5-9fa3-9e0686ed6715/rdps-input"
        ), PP.modelTemporalDomain, PP.EntityModelDomainShape),
    )
    for subject, predicate, expected_shape in domain_cases:
        graph = positive + Graph()
        graph.remove((subject, predicate, None))
        conforms, results, report = pyshacl.validate(graph, shacl_graph=shapes, advanced=True)
        assert not conforms, f"Missing {predicate} unexpectedly passed"
        sources = set(shapes.objects(expected_shape, SH.property))
        assert sources.intersection(results.objects(None, SH.sourceShape)), report
    print("PASS: missing model geometry, endpoints and applicability links rejected")

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
    fixtures = sorted((BLOCK / "validation").glob("*-fail.ttl"))
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
    assert len(bindings) == 9, "Expected specifications, structures, geometry and both temporal endpoints"
    for binding in bindings:
        selector = closure.value(binding, OA.hasSelector)
        pointer = str(closure.value(selector, RDF.value))
        value = item
        for token in pointer.lstrip("/").split("/"):
            key = token.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
        name = closure.value(binding, MLM.io_name)
        if name is not None:
            assert value["name"] == str(name), pointer
        elif "structure" in str(binding):
            assert {"shape", "dim_order", "data_type"} <= value.keys(), pointer
        elif pointer == "/geometry":
            assert value["type"] == "Polygon", pointer
        else:
            assert isinstance(value, str), pointer
            datetime.fromisoformat(value.replace("Z", "+00:00"))
    properties = item["properties"]
    assert datetime.fromisoformat(properties["start_datetime"].replace("Z", "+00:00")) <= datetime.fromisoformat(
        properties["end_datetime"].replace("Z", "+00:00")
    ), "Model temporal interval is reversed"
    polygon = item["geometry"]
    rings = [
        "(" + ", ".join(f"{longitude} {latitude}" for longitude, latitude in ring) + ")"
        for ring in polygon["coordinates"]
    ]
    expected_wkt = "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POLYGON (" + ", ".join(rings) + ")"
    actual_wkt = closure.value(BINDING["model-spatial-domain"], GEO.asWKT)
    assert " ".join(str(actual_wkt).split()) == expected_wkt, "RDF geometry differs from the published model"
    for endpoint, key in (("model-start", "start_datetime"), ("model-end", "end_datetime")):
        actual = closure.value(BINDING[endpoint], TIME.inXSDDateTimeStamp)
        assert isinstance(actual, Literal)
        assert datetime.fromisoformat(str(actual).replace("Z", "+00:00")) == datetime.fromisoformat(
            properties[key].replace("Z", "+00:00")
        ), f"RDF {endpoint} differs from the published model"
    print("PASS: specifications, structures and extents resolve in the published model")

    run = URIRef("urn:uuid:557e2aff-6780-4a25-aaa4-1b7100ceff82")
    assert (run, RDF.type, PROV.Activity) in captured
    assert (run, DCTERMS.type, URIRef(
        "https://crim-ca.github.io/bblocks-process-profiles/def/activity-type/climate-downscaling-inference"
    )) in enrichment
    assert not list(enrichment.triples((None, MLACT.accelerator, None)))
    assert not list(enrichment.triples((None, URIRef("https://w3id.org/ogc/rim/actionType"), None)))
    packed_plan = URIRef(
        "arcp://uuid,d6f937f0-bdae-4dd5-9fa3-9e0686ed6715/"
        "workflow/packed.cwl#main/ogc-ospd2026-downscaling-unet"
    )
    assert (packed_plan, RDF.type, PROV.Plan) in captured
    assert packed_plan in enrichment.objects(None, PROV.hadPlan)
    for predicate in (MLACT.model, MLACT.framework, MLACT.performsTask, MLACT.input, MLACT.output, MLACT.structure):
        assert list(enrichment.subjects(RDF.predicate, predicate)), f"Missing explicit mapping for {predicate}"
        assert not list(enrichment.triples((None, predicate, None))), f"Unexpected direct assertion: {predicate}"
    framework_statement = enrichment.value(predicate=RDF.predicate, object=MLACT.framework)
    assert str(enrichment.value(framework_statement, RDF.object)) == item["properties"]["mlm:framework"]
    tasks = {
        str(enrichment.value(statement, RDF.object)).removeprefix(str(MLM))
        for statement in enrichment.subjects(RDF.predicate, MLACT.performsTask)
    }
    assert tasks == set(item["properties"]["mlm:tasks"])
    structure_statements = list(enrichment.subjects(RDF.predicate, MLACT.structure))
    assert len(structure_statements) == 3
    for statement in structure_statements:
        structure = enrichment.value(statement, RDF.object)
        assert (structure, RDF.type, OA.SpecificResource) in closure
    for entity in enrichment.subjects(DCTERMS.isPartOf, None):
        container = enrichment.value(entity, DCTERMS.isPartOf)
        assert (container, RDF.type, PROV.Entity) in captured
    runtime = URIRef(
        "https://crim-ca.github.io/bblocks-process-profiles/def/run/"
        "d6f937f0-bdae-4dd5-9fa3-9e0686ed6715/runtime-environment"
    )
    assert (run, PROV.used, runtime) in enrichment
    assert enrichment.value(runtime, DCTERMS.source) is not None
    print("PASS: captured plan reused; complete ML mappings and runtime reference; no register-action claim")


if __name__ == "__main__":
    main()
