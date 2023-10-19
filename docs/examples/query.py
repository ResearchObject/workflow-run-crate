# Copyright 2023 CRS4.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""\
Perform a sample query on a Workflow Run RO-Crate.

The query returns all actions together with their instruments, start and end
times.
"""

from pathlib import Path
import argparse
import rdflib


query = """\
PREFIX schema: <http://schema.org/>
SELECT ?action ?instrument ?start ?end
WHERE {
  ?action a schema:CreateAction .
  ?action schema:instrument ?instrument .
  OPTIONAL { ?action schema:startTime ?start } .
  OPTIONAL { ?action schema:endTime ?end }
}
"""


def main(args):
    args.crate = Path(args.crate)
    g = rdflib.Graph()
    g.parse(args.crate / "ro-crate-metadata.json")
    qres = g.query(query)
    for row in qres:
        print(f"action: {row.action}")
        print(f"instrument: {row.instrument}")
        if row.start:
            print(f"start: {row.start}")
        if row.end:
            print(f"end: {row.end}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("crate", metavar="RO-Crate", help="RO-Crate directory")
    main(parser.parse_args())
