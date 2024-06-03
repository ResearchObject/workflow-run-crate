"""\
This script contains the SPARQL query for Competency Question 2 "How much
memory/cpu/disk was used in run?". In the discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/10 we generalized
the issue to the representation of resources used by processes. The
corresponding specification was added to the profiles in
https://github.com/ResearchObject/workflow-run-crate/pull/71.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>
PREFIX wfrun: <https://w3id.org/ro/terms/workflow-run#>

SELECT ?action ?resource_usage ?property_id ?unit_code ?value
WHERE {
?action a s:CreateAction .
?resource_usage a s:PropertyValue .
?action wfrun:resourceUsage ?resource_usage .
?resource_usage s:propertyID ?property_id .
OPTIONAL { ?resource_usage s:unitCode ?unit_code } .
?resource_usage s:value ?value .
}
"""

qres = g.query(QUERY)
for row in qres:
    print(f"Action: {row.action}")
    print(f"  resource_usage: {row.resource_usage}")
    print(f"  property_id: {row.property_id}")
    print(f"  unit_code: {row.unit_code}")
    print(f"  value: {row.value}")
