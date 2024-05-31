"""\
This script contains the SPARQL query for Competency Question 7 "Was the
execution successful?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/15 we decided to
represent this by adding an "actionStatus" property to actions, and consider
an execution successful if its value is "CompletedActionStatus" and not
successful if the value is "FailedActionStatus".
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>

SELECT ?action ?status
WHERE {
?action a s:CreateAction .
?action s:actionStatus ?status .
}
"""

qres = g.query(QUERY)
for row in qres:
    print(f"{row.action}, {row.status}")
