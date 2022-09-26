# Copyright 2022 CRS4.
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
Generate a Workflow Run RO-Crate from a CWLProv RO.
"""

import sys, os
import argparse
import hashlib
import json
import re
from pathlib import Path

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from cwlprov_to_crate.cwlprov_to_crate import ProvCrateBuilder
from provenance_profile import ProvenanceProfile

import networkx as nx
import prov.model
from cwl_utils.parser import load_document_by_yaml
# from cwlprov.ro import ResearchObject
# from cwlprov.prov import Provenance
# from cwlprov.utils import first
# from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
from rocrate.model.softwareapplication import SoftwareApplication

WORKFLOW_BASENAME = "packed.cwl"

CWL_TYPE_MAP = {
    "string": "Text",
    "int": "Integer",
    "long": "Integer",
    "float": "Float",
    "double": "Float",
    "Any": "DataType",
    "boolean": "Boolean",
    "File": "File",
    "Directory": "Dataset",
    "null": None,
}

SCATTER_JOB_PATTERN = re.compile(r"^(.+)_\d+$")

def get_fragment(uri):
    return uri.rsplit("#", 1)[-1]

def get_workflow(wf_path):
    """\
    Read the Galaxy workflow definition.

    Returns a dictionary where tools / workflows are mapped by their ids.

    Does not use load_document_by_uri, so we can hack the json to work around
    issues.
    """
    wf_path = Path(wf_path)
    with open(wf_path, "rt") as f:
        json_wf = json.load(f)
    graph = json_wf.get("$graph", [json_wf])
    # https://github.com/common-workflow-language/cwltool/pull/1506
    for n in graph:
        ns = n.pop("$namespaces", {})
        if ns:
            json_wf.setdefault("$namespaces", {}).update(ns)
    defs = load_document_by_yaml(json_wf, wf_path.absolute().as_uri())
    if not isinstance(defs, list):
        defs = [defs]
    def_map = {}
    for d in defs:
        k = get_fragment(d.id)
        if k == "main":
            k = wf_path.name
        def_map[k] = d
    return def_map


def main(args):
    args.root = Path(args.root)
    if not args.output:
        args.output = f"{args.root.name}.crate.zip"
    args.output = Path(args.output)
    ga_prov = ProvenanceProfile(args.root, "PDG", "https://orcid.org/0000-0002-8940-4946")
    builder = ProvCrateBuilder(args.root, args.workflow_name, args.license, prov=ga_prov.document, run=args.runid)
    crate = builder.build()
    if args.output.suffix == ".zip":
        crate.write_zip(args.output)
    else:
        crate.write(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("root", metavar="ROOT_DIR",
                        help="top-level directory of the Galaxy export")
    parser.add_argument("-o", "--output", metavar="DIR OR ZIP",
                        help="output RO-Crate directory or zip file")
    parser.add_argument("-l", "--license", metavar="STRING",
                        help="license URL (or WorkflowHub-accepted id)")
    parser.add_argument("-w", "--workflow-name", metavar="STRING",
                        help="original workflow name")
    parser.add_argument("-r", "--runid", metavar="STRING",
                        help="run id")
    main(parser.parse_args())
