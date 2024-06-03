"""\
This script contains the SPARQL query for Competency Question 11 "How
were workflow parameters used in tool runs?". The discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/25 resulted
in the specification on describing parameter connections added with pull
request https://github.com/ResearchObject/workflow-run-crate/pull/35.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX	dcterms: <http://purl.org/dc/terms/>
PREFIX	s: <http://schema.org/>
PREFIX	bs: <https://bioschemas.org/>
PREFIX	bswf: <https://bioschemas.org/ComputationalWorkflow#>
PREFIX	bswfprofile: <https://bioschemas.org/profiles/ComputationalWorkflow/>
PREFIX	rocrate: <https://w3id.org/ro/crate/>
PREFIX	wfcrate: <https://w3id.org/workflowhub/workflow-ro-crate/>
PREFIX	wfhprofile: <https://about.workflowhub.eu/Workflow-RO-Crate/>
PREFIX	wrterm: <https://w3id.org/ro/terms/workflow-run#>

SELECT DISTINCT ?execution  ?formal_parameter ?formal_parameter_name ?step ?step_source_name ?step_formal_parameter ?step_formal_parameter_name  ?input ?additional_type ?input_value
WHERE   {
    # This first part is just matching
    # Workflow RO-Crates and its main entity
    ?rocratejson
        a s:CreativeWork ;
        dcterms:conformsTo ?rocrateprofile ;
        dcterms:conformsTo ?wfcrateprofile ;
        s:about ?rootdataset .
    ?rootdataset a s:Dataset .
    FILTER (
        STRSTARTS(str(?rocrateprofile), str(rocrate:))
    )
    FILTER (
        ?wfcrateprofile = wfhprofile: || STRSTARTS(str(?wfcrateprofile), str(wfcrate:))
    )
    ?rootdataset
        s:mainEntity ?main_entity .
    ?main_entity
        a bs:ComputationalWorkflow ;
        dcterms:conformsTo ?bsworkflowprofile ;
        bswf:input ?formal_parameter ;
        s:step ?step .
    FILTER (
        STRSTARTS(str(?bsworkflowprofile), str(bswfprofile:))
    )
    ?formal_parameter
        a bs:FormalParameter ;
        s:name ?formal_parameter_name .
    
    # We are taking here only one execution
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
    ?execution s:object ?input .
    ?input s:exampleOfWork ?formal_parameter .
    ?parameter_connection
        a wrterm:ParameterConnection ;
        wrterm:sourceParameter ?formal_parameter ;
        wrterm:targetParameter ?step_formal_parameter .
    ?step_formal_parameter
        a bs:FormalParameter ;
        s:name ?step_formal_parameter_name .
    ?step_source
        a s:SoftwareApplication ;
        s:name ?step_source_name ;
        bswf:input ?step_formal_parameter .
    ?step
        a s:HowToStep ;
        s:workExample ?step_source .

    # Now the details about the input
    ?formal_parameter
        s:additionalType ?additional_type .
    {
        # A file, which is a schema.org MediaObject
        BIND ( "File" AS ?additional_type )
        ?input
            a s:MediaObject ;
            s:name ?input_value .
    } UNION {
        # A directory, which is a schema.org Dataset
        BIND ( "Dataset" AS ?additional_type )
        ?input
            a s:Dataset ;
            s:name ?input_value .
        FILTER EXISTS { 
            # subquery to determine it is not an empty Dataset
            SELECT ?dircomp
            WHERE { 
                ?input
                    s:hasPart+ ?dircomp .
                ?dircomp
                    a s:MediaObject .
            }
        }
    } UNION {
        # A single property value, which can be either Integer, Text, Boolean or Float
        VALUES (?additional_type) { ( "Integer" ) ( "Text" ) ( "Boolean" ) ( "Float" ) }
        ?input
            a s:PropertyValue ;
            s:value ?input_value .
    } UNION {
        # A combination of files or directories or property values
        BIND ( "Collection" AS ?additional_type )
        VALUES ( ?leaf_type ) { ( s:Integer ) ( s:Text ) ( s:Boolean ) ( s:Float ) ( s:MediaObject ) ( s:Dataset ) }
        ?input
            a s:Collection ;
            s:hasPart+ ?component .
        ?component
            a ?leaf_type .
        OPTIONAL {
            ?component s:name ?input_value .
        }
        OPTIONAL {
            ?component s:alternateName ?input_value .
        }
        OPTIONAL {
            ?component s:value ?input_value .
        }
    }
}
"""

qres = g.query(QUERY)
for i_row, row in enumerate(qres):
    print(f"\nTuple {i_row}")
    for key, val in row.asdict().items():
        print(f"{key} => {val}")
