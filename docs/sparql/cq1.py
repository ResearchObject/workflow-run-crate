"""\
This script contains the SPARQL query for Competency Question 1 "What
container images (e.g., Docker) were used by the run?". The discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/9 resulted in
the specification on describing container images added with pull request
https://github.com/ResearchObject/workflow-run-crate/pull/64.
"""

import rdflib
from pathlib import Path

CRATE = Path("workflow_run_crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX	dcterms: <http://purl.org/dc/terms/>
PREFIX	s: <http://schema.org/>
PREFIX	bs: <https://bioschemas.org/>
PREFIX	bswfprofile: <https://bioschemas.org/profiles/ComputationalWorkflow/>
PREFIX	rocrate: <https://w3id.org/ro/crate/>
PREFIX	wfcrate: <https://w3id.org/workflowhub/workflow-ro-crate/>
PREFIX	wfhprofile: <https://about.workflowhub.eu/Workflow-RO-Crate/>
PREFIX	wrterm: <https://w3id.org/ro/terms/workflow-run#>
PREFIX	wikidata: <https://www.wikidata.org/wiki/>

SELECT ?execution ?container ?container_additional_type ?type_of_container ?type_of_container_type ?container_registry ?container_name ?container_tag ?container_sha256 ?container_platform ?container_arch
WHERE   {
    # This first part is just matching
    # Workflow RO-Crates and its main entity
    ?rocratejson
        a s:CreativeWork ;
        dcterms:conformsTo ?rocrateprofile ;
        s:about ?rootdataset .
    ?rootdataset a s:Dataset .
    FILTER (
        STRSTARTS(str(?rocrateprofile), str(rocrate:))
    ) .
    ?rocratejson dcterms:conformsTo ?wfcrateprofile .
    FILTER (
        ?wfcrateprofile = wfhprofile: || STRSTARTS(str(?wfcrateprofile), str(wfcrate:))
    ) .
    ?rootdataset
        s:mainEntity ?main_entity .
    ?main_entity
        a bs:ComputationalWorkflow ;
        dcterms:conformsTo ?bsworkflowprofile .
    FILTER (
        STRSTARTS(str(?bsworkflowprofile), str(bswfprofile:))
    ) .

    # We are taking here only the first execution
    {
        SELECT  ?execution
        WHERE   {
            ?rootdataset s:mentions ?execution .
            ?execution
                a s:CreateAction ;
                s:instrument ?main_entity .
        }
        LIMIT 1
    }

    # We are assuming the workflow is the original, instead of a derivation
    ?execution wrterm:containerImage ?container .
    ?container
        a wrterm:ContainerImage ;
        s:additionalType ?container_additional_type .
    OPTIONAL {
        ?container
            s:softwareRequirements ?container_type ;
            s:applicationCategory ?type_of_container .
        ?container_type
            a s:SoftwareApplication ;
            s:applicationCategory ?type_of_container_type .
        FILTER(
            STRSTARTS(str(?type_of_container), str(wikidata:)) &&
            STRSTARTS(str(?type_of_container_type), str(wikidata:))
        ) .
    }
    OPTIONAL {
        ?container wrterm:registry ?container_registry .
    }
    OPTIONAL {
        ?container s:name ?container_name .
    }
    OPTIONAL {
        ?container wrterm:tag ?container_tag .
    }
    OPTIONAL {
        ?container wrterm:sha256 ?container_sha256 .
    }
    OPTIONAL {
        ?container
            a s:SoftwareApplication ;
            s:operatingSystem ?container_platform .
    }
    OPTIONAL {
        ?container
            a s:SoftwareApplication ;
            s:processorRequirements ?container_arch .
    }
}
"""

qres = g.query(QUERY)
for i_row, row in enumerate(qres):
    print(f"\nTuple {i_row}")
    for key, val in row.asdict().items():
        print(f"{key} => {val}")
