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

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

print("WORKFLOW ENVIRONMENT(S)")
print("=======================")
QUERY1 = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>
PREFIX codemeta: <https://codemeta.github.io/terms/>

SELECT ?environment ?format ?profile ?profileName
WHERE {
?workflow a s:HowTo, bioschemas:ComputationalWorkflow ;
  codemeta:buildInstructions ?environment .

?environment a s:MediaObject .

OPTIONAL { ?environment s:encodingFormat ?format } .
OPTIONAL { ?environment s:conformsTo ?profile .
           ?profile s:name ?profileName .
         } .
}
"""

qres = g.query(QUERY1)
for row in qres:
    print(row.obj)


print("WORKFLOW TOOL ENVIRONMENT(S)")
print("===========================")

QUERY2 = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>
PREFIX codemeta: <https://codemeta.github.io/terms/>

SELECT ?environment ?format ?profile ?profileName
WHERE {
?workflow a s:HowTo, bioschemas:ComputationalWorkflow;
  s:step ?step .

?step a s:HowToStep ;
  codemeta:buildInstructions ?environment .

?environment a s:MediaObject .

OPTIONAL { ?environment s:encodingFormat ?format } .
OPTIONAL { ?environment s:conformsTo ?profile .
           ?profile s:name ?profileName .
         } .
}
"""
qres = g.query(QUERY2)
for row in qres:
    print(row.res)
