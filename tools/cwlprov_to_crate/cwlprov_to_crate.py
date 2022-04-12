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
from rocrate.model.contextentity import ContextEntity


class Thing:

    def __init__(self, id_, label=None):
        self.id_ = id_
        self.label = label


class Agent(Thing):
    pass


class SoftwareAgent(Agent):

    def __init__(self, id_, label=None, image=None):
        super().__init__(id_, label=label)
        self.image = image


class WorkflowEngine(SoftwareAgent):
    pass


class Person(Agent):

    def __init__(self, id_, label=None, name=None):
        super().__init__(id_, label=label)
        self.name = name or label


class Activity(Thing):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.starter = None
        self.ender = None
        self.start_time = None
        self.end_time = None


class ProcessRun(Activity):
    pass


class WorkflowRun(Activity):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.steps = []


class Provenance:

    def __init__(self, path_or_file):
        try:
            self.data = json.load(path_or_file)
        except AttributeError:
            with open(path_or_file) as f:
                self.data = json.load(f)
        self.agents = self.__read_agents()
        self.activities = self.__read_activities()
        self.__read_start_end()

    @staticmethod
    def get_types(record):
        entry = record.get("prov:type", [])
        if not isinstance(entry, list):
            entry = [entry]
        try:
            return [_["$"] for _ in entry]
        except (TypeError, KeyError):
            raise ValueError(f"Unexpected type entry: {entry!r}")

    def __read_agents(self):
        agents = {}
        for id_, record in self.data["agent"].items():
            types = set(Provenance.get_types(record))
            if "prov:Person" in types:
                agents[id_] = Person(
                    id_,
                    label=record.get("prov:label"),
                    name=record.get("prov:name"),
                )
            elif "wfprov:WorkflowEngine" in types:
                agents[id_] = WorkflowEngine(id_, label=record.get("prov:label"))
            elif "prov:SoftwareAgent" in types:
                agents[id_] = SoftwareAgent(
                    id_,
                    label=record.get("prov:label"),
                    image=record.get("cwlprov:image"),
                )
            else:
                agents[id_] = Agent(id_, label=record.get("prov:label"))
        return agents

    def __read_activities(self):
        activities = {}
        for id_, record in self.data["activity"].items():
            types = set(Provenance.get_types(record))
            if "wfprov:WorkflowRun" in types:
                activities[id_] = WorkflowRun(id_, label=record.get("prov:label"))
            elif "wfprov:ProcessRun" in types:
                activities[id_] = ProcessRun(id_, label=record.get("prov:label"))
            else:
                activities[id_] = Activity(id_, label=record.get("prov:label"))
        return activities

    def __read_start_end(self):
        for dummy, record in self.data["wasStartedBy"].items():
            activity = self.activities.get(record.get("prov:activity"))
            if activity:
                activity.starter = self.agents.get(record.get("prov:starter"))
                activity.start_time = record.get("prov:time")
        for dummy, record in self.data["wasEndedBy"].items():
            activity = self.activities.get(record.get("prov:activity"))
            if activity:
                activity.ender = self.agents.get(record.get("prov:ender"))
                activity.end_time = record.get("prov:time")


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


def read_prov(root_dir):
    prov_dir = root_dir / "metadata" / "provenance"
    with open(prov_dir / "primary.cwlprov.json") as f:
        return json.load(f)


def add_action(crate, prov):
    sel = [_ for _ in prov.activities.values() if type(_) == WorkflowRun]
    if len(sel) != 1:
        raise ValueError(f"Unexpected number of workflow runs: {len(sel)}")
    wf_run = sel[0]
    action = crate.add(ContextEntity(crate, properties={
        "@type": "CreateAction",
        "name": wf_run.label,
        "startTime": wf_run.start_time,
        "endTime": wf_run.end_time,
    }))
    action["instrument"] = crate.mainEntity
    return action


def make_crate(args):
    crate = ROCrate(gen_preview=False)
    wf_source, input_data, output_data = get_workflow(args.root)
    with open(wf_source) as f:
        wf_data = json.load(f)
    workflow = crate.add_workflow(
        wf_source, wf_source.name, main=True, lang="cwl",
        lang_version=wf_data["cwlVersion"], gen_cwl=False
    )
    # How to map to the original workflow file in "snapshot"?
    workflow["name"] = args.workflow_name or args.root.name
    if args.license:
        crate.root_dataset["license"] = args.license
    prov = Provenance(args.root / "metadata" / "provenance" / "primary.cwlprov.json")
    action = add_action(crate, prov)
    crate.root_dataset["mentions"] = [action]
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
    parser.add_argument("-w", "--workflow-name", metavar="STRING",
                        help="original workflow name")
    main(parser.parse_args())
