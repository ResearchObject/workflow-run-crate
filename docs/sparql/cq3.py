"""\
This script contains the SPARQL query for Competency Question 3 "What are the
configuration files used in a workflow execution step?". The discussion on
https://github.com/ResearchObject/workflow-run-crate/issues/11 resulted in
realizing that the use case needed in practice was representing a
configuration file for the workflow engine, especially from the example given
by StreamFlow. The configuration file is added to the "object" attribute of
the "OrganizeAction" corresponding to the workflow execution. Since the other
objects of the OrganizeAction are of "ControlAction" type, in the query we
filter them out to get the configuration file.
"""

import rdflib
from pathlib import Path

CRATE = Path("crate")

g = rdflib.Graph()
g.parse(CRATE/"ro-crate-metadata.json")

QUERY = """\
PREFIX s: <http://schema.org/>

SELECT ?conf
WHERE {
?action a s:OrganizeAction .
?action s:object ?conf .
FILTER NOT EXISTS { ?conf a s:ControlAction }
}
"""

qres = g.query(QUERY)
for row in qres:
    print(row.conf)
