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

import argparse
import json
from pathlib import Path

# from cwl_utils.parser import load_document_by_uri
from rocrate.rocrate import ROCrate


def get_workflow(root_dir):
    wf_dir = root_dir / "workflow"
    wf_path = wf_dir / "packed.cwl"
    # wf_def = load_document_by_uri(wf_path)
    input_path = wf_dir / "primary-job.json"
    output_path = wf_dir / "primary-output.json"
    with open(input_path) as f:
        input_data = json.load(f)
    with open(output_path) as f:
        output_data = json.load(f)
    return wf_path, input_data, output_data


def make_crate(args):
    crate = ROCrate(gen_preview=False)
    wf_source, input_data, output_data = get_workflow(args.root)
    with open(wf_source) as f:
        wf_data = json.load(f)
    workflow = crate.add_workflow(
        wf_source, wf_source.name, main=True, lang="cwl",
        lang_version=wf_data["cwlVersion"], gen_cwl=False
    )
    # workflow["name"] = ? How to map to the original wf file in snapshot?
    if args.license:
        crate.root_dataset["license"] = args.license
    if args.output.endswith(".zip"):
        crate.write_zip(args.output)
    else:
        crate.write(args.output)


def main(args):
    args.root = Path(args.root)
    if not args.output:
        args.output = f"{args.root.name}.crate.zip"
    print(f"generating {args.output}")
    make_crate(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("root", metavar="ROOT_DIR",
                        help="top-level directory (workflow repository)")
    parser.add_argument("-o", "--output", metavar="DIR OR ZIP",
                        help="output RO-Crate directory or zip file")
    parser.add_argument("-l", "--license", metavar="STRING",
                        help="license URL (or WorkflowHub-accepted id)")
    main(parser.parse_args())
