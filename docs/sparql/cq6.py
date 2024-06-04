"""\
This script contains the SPARQL query for Competency Question 6 "How long does
this workflow take to run?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/14 we decided that
this is best represented by the difference between the ending time and the
starting time of the action corresponding to the workflow's execution.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>
PREFIX bioschemas: <https://bioschemas.org/>

SELECT ?start ?end
WHERE {
?action a s:CreateAction .
?workflow a bioschemas:ComputationalWorkflow .
?action s:instrument ?workflow .
OPTIONAL { ?action s:startTime ?start } .
OPTIONAL { ?action s:endTime ?end }
}
"""

qres = g.query(QUERY)
for row in qres:
    print(f"{row.start}, {row.end}")
