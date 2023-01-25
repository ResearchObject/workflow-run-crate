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
"""

import argparse

from rocrate.rocrate import ROCrate


def as_list(value):
    if isinstance(value, list):
        return value
    return [value]


def dump_run_results(tool, action, control_action=None):
    instrument = action["instrument"]
    print(f"action {action.id}")
    if control_action:
        print("  step:", control_action["instrument"].id)
    print("  instrument:", instrument.id, f"({instrument.type})")
    print("  started:", action.get("startTime", "???"))
    print("  ended:", action.get("endTime", "???"))
    objects = {p.id: obj for obj in action.get("object", [])
               for p in as_list(obj.get("exampleOfWork", []))}
    results = {p.id: res for res in action.get("result", [])
               for p in as_list(res.get("exampleOfWork", []))}
    print("  inputs:")
    for in_ in tool["input"]:
        obj = objects.get(in_.id)
        print(f"    {in_.id}: {obj.get('value', obj.id) if obj else ''}")
    for obj in action.get("object", []):
        if "exampleOfWork" not in obj:
            print(f"    ???: {obj.get('value', obj.id)}")
    print("  outputs:")
    for out in tool["output"]:
        res = results.get(out.id)
        print(f"    {out.id}: {res.get('value', res.id) if res else ''}")
    for res in action.get("result", []):
        if "exampleOfWork" not in res:
            print(f"    ???: {res.get('value', res.id)}")


def main(args):
    crate = ROCrate(args.crate)
    wf = crate.mainEntity
    actions = {}
    for a in crate.contextual_entities:
        if a.type == "CreateAction":
            actions.setdefault(a["instrument"].id, []).append(a)
    assert len(actions[wf.id]) == 1
    wf_action = actions[wf.id][0]
    control_actions = {a: ca for ca in crate.contextual_entities
                       for a in as_list(ca.get("object", []))
                       if ca.type == "ControlAction"}
    dump_run_results(wf, wf_action)
    for tool in wf.get("hasPart", []):
        for a in actions.get(tool.id, []):
            print()
            dump_run_results(tool, a, control_actions.get(a))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("crate", metavar="CRATE",
                        help="input RO-Crate directory or zip file")
    main(parser.parse_args())

