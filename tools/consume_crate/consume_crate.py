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
Example of consuming a Workflow Run RO-Crate.

NOTE: for now this is just a quick check that a "minimal" provenance crate
(i.e., without entities for engine, engine run, step and step run) stands on
its own.
"""

import argparse

from rocrate.rocrate import ROCrate


def as_list(value):
    if isinstance(value, list):
        return value
    return [value]


def dump_run_results(tool, action):
    print("  started:", action["startTime"])
    print("  ended:", action["endTime"])
    print("  inputs:")
    objects = {p.id: obj for obj in action["object"]
               for p in as_list(obj["exampleOfWork"])}
    results = {p.id: res for res in action["result"]
               for p in as_list(res["exampleOfWork"])}
    for in_ in tool["input"]:
        obj = objects[in_.id]
        print(f"    {in_.id}: {obj.get('value', obj.id)}")
    for out in tool["output"]:
        res = results[out.id]
        print(f"    {out.id}: {res.get('value', res.id)}")


def main(args):
    crate = ROCrate(args.crate)
    wf = crate.mainEntity
    actions = {_["instrument"].id: _ for _ in crate.contextual_entities
               if _.type == "CreateAction"}
    print("workflow")
    print("--------")
    print(wf.id)
    dump_run_results(wf, actions[wf.id])
    print()
    print("tools")
    print("-----")
    for tool in wf["hasPart"]:
        print(tool.id)
        dump_run_results(tool, actions[tool.id])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("crate", metavar="CRATE",
                        help="input RO-Crate directory or zip file")
    main(parser.parse_args())
