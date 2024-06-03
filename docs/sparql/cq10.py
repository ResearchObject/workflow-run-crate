"""\
This script contains the SPARQL query for Competency Question 10 "What is the
script used to wrap up a software component?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/18 we realized
that we were already representing the wrappers, and the issue was actually to
represent their dependencies. The corresponding specification was added to the
profiles in https://github.com/ResearchObject/workflow-run-crate/pull/67.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>

SELECT ?tool ?req ?main_req ?version
WHERE {
?tool a s:SoftwareApplication .
?action a s:CreateAction .
?action s:instrument ?tool .
?tool s:softwareRequirements ?req .
?tool s:mainEntity ?main_req .
?req s:version ?version .
}
"""

qres = g.query(QUERY)
for row in qres:
    print(f"Tool: {row.tool}")
    print(f"  main requirement: {row.main_req}")
    print(f"  requirement: {row.req}")
    print(f"    version: {row.version}")
