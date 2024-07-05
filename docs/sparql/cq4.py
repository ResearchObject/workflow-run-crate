"""\
This script contains the SPARQL query for Competency Question 4 
"What is the environment/container file used in a specific workflow execution step?". 
In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/12 we identified
the term buildInstructions from CodeMeta which can point to e.g. 
Conda environment.
"""

import rdflib
from pathlib import Path

CRATE = Path("provenance_run_crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

print("WORKFLOW ENVIRONMENT")
print("====================")
QUERY1 = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>
PREFIX codemeta: <https://codemeta.github.io/terms/>

SELECT DISTINCT?workflow ?workflowName ?environment ?format ?profile ?profileName
WHERE {
?workflow a s:HowTo, bioschemas:ComputationalWorkflow ;
  codemeta:buildInstructions ?environment .

OPTIONAL { 
    ?workflow s:name ?workflowName 
}

?environment a s:MediaObject .

OPTIONAL { ?environment s:encodingFormat ?format } .
OPTIONAL { ?environment dct:conformsTo ?profile .
           ?profile s:name ?profileName .
         } .
}
"""

qres = g.query(QUERY1)
for row in qres:
    print("Workflow:", row.workflowName or row.workflow)

    print("  Environment:", row.environment)
    if (row.format):
        print("    Format:", row.format)
    if (row.profile):
        print("    Profile:", row.profileName or "", "<%s>" % row.profile)


print("WORKFLOW STEP ENVIRONMENTS")
print("==========================")

QUERY2 = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>
PREFIX codemeta: <https://codemeta.github.io/terms/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?step ?stepName ?environment ?format ?profile ?profileName
WHERE {
?workflow a s:HowTo, bioschemas:ComputationalWorkflow;
  s:step ?step .

?step a s:HowToStep ;
  codemeta:buildInstructions ?environment .
OPTIONAL { 
    ?step s:name ?stepName 
}

?environment a s:MediaObject .

OPTIONAL { ?environment s:encodingFormat ?format } .
OPTIONAL { ?environment dct:conformsTo ?profile .
           ?profile s:name ?profileName .
         } .
}
"""
qres = g.query(QUERY2)
for row in qres:
    print("Step:", row.stepName or row.step)
    print("  Environment:", row.environment)
    if (row.format):
        print("    Format:", row.format)
    if (row.profile):
        print("    Profile:", row.profileName or "", "<%s>" % row.profile)

