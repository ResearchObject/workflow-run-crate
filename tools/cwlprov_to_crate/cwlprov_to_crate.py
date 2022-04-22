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
from rocrate.model.softwareapplication import SoftwareApplication


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
        self.agent = None
        self.plan = None
        self.starter = None
        self.ender = None
        self.start_time = None
        self.end_time = None
        self.in_params = {}
        self.out_params = {}
        self.steps = []


class ProcessRun(Activity):
    pass


class WorkflowRun(Activity):
    pass


class Entity(Thing):

    def __init__(self, id_, label=None, value=None):
        super().__init__(id_, label=label)
        self.value = value
        self.general_entity = None

    def get_path(self):
        if not (self.general_entity and getattr(self, "basename", None)):
            return None
        try:
            prefix, hash_ = self.general_entity.id_.strip().split(":")
        except ValueError:
            return None
        if prefix != "data":
            return None
        return Path("data") / hash_[:2] / hash_


class Plan(Entity):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.subprocesses = []


class Process(Plan):
    pass


class Workflow(Plan):
    pass


class Artifact(Entity):
    pass


class File(Artifact):

    def __init__(self, id_, basename=None):
        super().__init__(id_)
        self.basename = basename


class Provenance:

    def __init__(self, path_or_file):
        try:
            self.data = json.load(path_or_file)
        except AttributeError:
            with open(path_or_file) as f:
                self.data = json.load(f)
        self.agents = self.__read_agents()
        self.activities = self.__read_activities()
        self.entities = self.__read_entities()
        self.__read_specializations()
        self.__read_start_end()
        self.__read_params()
        self.__read_associations()

    @staticmethod
    def get_list(entry, key):
        value = entry.get(key, [])
        if not isinstance(value, list):
            value = [value]
        try:
            return [_["$"] if isinstance(_, dict) else _ for _ in value]
        except (TypeError, KeyError):
            raise ValueError(f"Malformed value for {key!r}: {entry.get(key)!r}")

    @staticmethod
    def get_types(record):
        return Provenance.get_list(record, "prov:type")

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

    def __read_entities(self):
        entities = {}
        for id_, entry in self.data["entity"].items():
            # FIXME: assumes "prov:value" values are scalar
            if not isinstance(entry, list):
                record = {k: Provenance.get_list(entry, k) for k in entry}
            else:
                record = {}
                for d in entry:
                    for k in d:
                        record.setdefault(k, []).extend(Provenance.get_list(d, k))
            types = set(record.get("prov:type", []))
            if "wfdesc:Workflow" in types:
                entities[id_] = Workflow(id_, label=record.get("prov:label", [None])[0])
            elif "wfdesc:Process" in types:
                entities[id_] = Process(id_, label=record.get("prov:label", [None])[0])
            elif "wf4ever:File" in types:
                entities[id_] = File(id_, basename=record.get("cwlprov:basename", [None])[0])
            elif "wfprov:Artifact" in types:
                entities[id_] = Artifact(id_, label=record.get("prov:label", [None])[0])
            else:
                entities[id_] = Entity(
                    id_,
                    label=record.get("prov:label", [None])[0],
                    value=record.get("prov:value", [None])[0],
                )
            try:
                entities[id_].subprocesses = record["wfdesc:hasSubProcess"]
            except KeyError:
                pass
        for id_, e in entities.items():
            try:
                e.subprocesses = [entities[_] for _ in e.subprocesses]
            except AttributeError:
                pass
        return entities

    def __read_specializations(self):
        for dummy, record in self.data.get("specializationOf", {}).items():
            specific = self.entities.get(record.get("prov:specificEntity"))
            if not specific:
                continue
            general = self.entities.get(record.get("prov:generalEntity"))
            if general:
                specific.general_entity = general

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

    def __read_params(self):
        for dummy, record in self.data.get("used", {}).items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            entity = self.entities.get(record.get("prov:entity"))
            if entity:
                activity.in_params[record["prov:role"]["$"]] = entity
        for dummy, record in self.data["wasGeneratedBy"].items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            entity = self.entities.get(record.get("prov:entity"))
            if entity:
                activity.out_params[record["prov:role"]["$"]] = entity

    def __read_associations(self):
        is_plan_for = {}
        for dummy, record in self.data["wasAssociatedWith"].items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            # TODO: agents; note that there can be many agents for an activity
            plan = self.entities.get(record.get("prov:plan"))
            if plan:
                activity.plan = plan  # assuming one plan per activity
                is_plan_for.setdefault(plan.id_, []).append(activity)
        for plan_id, activities in is_plan_for.items():
            plan = self.entities.get(plan_id)
            for act in activities:
                for sp in plan.subprocesses:
                    for step in is_plan_for[sp.id_]:
                        act.steps.append(step)


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


# add to ro-crate-py?
def update_property(entity, name, item):
    """\
    Add ``item`` to the values of property ``name`` in ``entity``
    """
    value = entity.get(name, [])
    if not isinstance(value, list):
        value = [value]
    value = list(set(value + [item]))
    entity[name] = value[0] if len(value) == 1 else value


def convert_value(value):
    # str(True) == "True" (same for False), so booleans map to Schema.org types.
    # Is there any type for which str() might be inappropriate?
    return str(value)


def add_params(crate, source, prov_params):
    wf_params, action_params = [], []
    for k, v in prov_params.items():
        path = v.get_path()
        if not path and not v.value:
            continue
        k = k.split(":", 1)[-1]
        wf_p = crate.add(ContextEntity(crate, f"#param-{k}", properties={
            "@type": "FormalParameter",
            "name": k,
        }))
        wf_params.append(wf_p)
        if path:
            action_p = crate.dereference(path.as_posix())
            if not action_p:
                action_p = crate.add_file(source / path, path)
        elif v.value:
            action_p = crate.add(ContextEntity(crate, f"#pv-{k}", properties={
                "@type": "PropertyValue",
                "name": k,
                "value": convert_value(v.value),
            }))
        update_property(action_p, "exampleOfWork", wf_p)
        action_params.append(action_p)
    return wf_params, action_params


def add_action(crate, source, activity, parent_instrument=None):
    workflow = crate.mainEntity
    action = crate.add(ContextEntity(crate, properties={
        "@type": "CreateAction",
        "name": activity.label,
        "startTime": activity.start_time,
        "endTime": activity.end_time,
    }))
    try:
        step = activity.plan.id_.strip().split("/", 1)[1]
    except IndexError:
        instrument = workflow
    else:
        instrument_id = f"{workflow.id}#{step}"
        instrument = crate.add(SoftwareApplication(crate, instrument_id, properties={
            "name": instrument_id,
        }))
    action["instrument"] = instrument
    if parent_instrument:
        update_property(parent_instrument, "hasPart", instrument)
    instrument["input"], action["object"] = add_params(crate, source, activity.in_params)
    instrument["output"], action["result"] = add_params(crate, source, activity.out_params)
    for step in activity.steps:
        add_action(crate, source, step, parent_instrument=instrument)
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
    sel = [_ for _ in prov.activities.values() if type(_) == WorkflowRun]
    if len(sel) != 1:
        raise ValueError(f"Unexpected number of workflow runs: {len(sel)}")
    workflow_run = sel[0]
    action = add_action(crate, args.root, workflow_run)
    crate.root_dataset["mentions"] = [action]
    if args.output.suffix == ".zip":
        crate.write_zip(args.output)
    else:
        crate.write(args.output)


def main(args):
    args.root = Path(args.root)
    if not args.output:
        args.output = f"{args.root.name}.crate.zip"
    print(f"generating {args.output}")
    args.output = Path(args.output)
    make_crate(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("root", metavar="ROOT_DIR",
                        help="top-level directory of the CWLProv RO")
    parser.add_argument("-o", "--output", metavar="DIR OR ZIP",
                        help="output RO-Crate directory or zip file")
    parser.add_argument("-l", "--license", metavar="STRING",
                        help="license URL (or WorkflowHub-accepted id)")
    parser.add_argument("-w", "--workflow-name", metavar="STRING",
                        help="original workflow name")
    main(parser.parse_args())
