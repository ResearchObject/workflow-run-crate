"""\
This script contains the SPARQL query for Competency Question 9 "What is the
source code version of the component executed in a workflow step?". In
https://github.com/ResearchObject/workflow-run-crate/pull/42 we ended up using
"softwareVersion" with a fallback on "version" on the "SoftwareApplication"
entity, which is used both in Process Run Crates and Provenance Run Crates for
individual tools.
"""

import rdflib
from pathlib import Path

CRATE = Path("process_run_crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>

SELECT ?name ?version
WHERE {
?app a s:SoftwareApplication .
?app s:name ?name .
OPTIONAL { ?app s:softwareVersion ?version } .
OPTIONAL { ?app s:version ?version } .
}
"""

qres = g.query(QUERY)
for row in qres:
    print(row.name, row.version)
