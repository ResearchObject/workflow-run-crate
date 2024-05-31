"""\
This script contains the SPARQL query for Competency Question 8 "What are the
inputs and outputs of the overall workflow?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/16 we identified
them as the "object" and "result" of the action corresponding to the
workflow's execution.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>

SELECT ?obj
WHERE {
?action a s:CreateAction .
?workflow a bioschemas:ComputationalWorkflow .
?action s:instrument ?workflow .
OPTIONAL { ?action s:object ?obj } .
}
"""

qres = g.query(QUERY)
print("INPUTS")
print("======")
for row in qres:
    print(row.obj)

QUERY = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>

SELECT ?res
WHERE {
?action a s:CreateAction .
?workflow a bioschemas:ComputationalWorkflow .
?action s:instrument ?workflow .
OPTIONAL { ?action s:result ?res } .
}
"""

qres = g.query(QUERY)
print("OUTPUTS")
print("=======")
for row in qres:
    print(row.res)
