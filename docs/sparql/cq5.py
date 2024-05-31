"""\
This script contains the SPARQL query for Competency Question 5 "How long does
this workflow component take to run?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/13 we decided that
this is best represented by the difference between the ending time and the
starting time of the action corresponding to each tool's execution.
"""

import rdflib
from pathlib import Path

CRATE = Path("ml-predict-pipeline-cwltool-runcrate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>

SELECT ?start ?end
WHERE {
?action a s:CreateAction .
?tool a s:SoftwareApplication .
?action s:instrument ?tool .
OPTIONAL { ?action s:startTime ?start } .
OPTIONAL { ?action s:endTime ?end }
}
"""

qres = g.query(QUERY)
for row in qres:
    print(f"{row.start}, {row.end}")
