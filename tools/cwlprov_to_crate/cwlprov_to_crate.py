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
import hashlib
import json
import re
from itertools import chain
from pathlib import Path

import networkx as nx
from cwl_utils.parser import load_document_by_yaml
from rocrate.rocrate import ROCrate
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


def convert_cwl_type(cwl_type):
    if isinstance(cwl_type, list):
        s = set(convert_cwl_type(_) for _ in cwl_type)
        s.discard(None)
        return sorted(s)
    if isinstance(cwl_type, str):
        return CWL_TYPE_MAP[cwl_type]
    if cwl_type.type == "enum":
        return "Text"  # use actionOption to represent choices?
    if cwl_type.type == "array":
        return CWL_TYPE_MAP[cwl_type.items]
    if cwl_type.type == "record":
        return "PropertyValue"


def properties_from_cwl_param(cwl_p):
    def is_structured(cwl_type):
        return getattr(cwl_type, "type", None) in ("array", "record")
    properties = {
        "@type": "FormalParameter",
        "additionalType": convert_cwl_type(cwl_p.type)
    }
    if cwl_p.format:
        properties["encodingFormat"] = cwl_p.format
    if isinstance(cwl_p.type, list) and "null" in cwl_p.type:
        properties["valueRequired"] = "False"
    if is_structured(cwl_p.type):
        properties["multipleValues"] = "True"
    if hasattr(cwl_p, "default"):
        try:
            default_type = cwl_p.default["class"]
        except (TypeError, KeyError):
            if not is_structured(cwl_p.type) and cwl_p.default is not None:
                properties["defaultValue"] = str(cwl_p.default)
        else:
            if default_type in ("File", "Directory"):
                properties["defaultValue"] = cwl_p.default["location"]
        # TODO: support more cases
    if getattr(cwl_p.type, "type", None) == "enum":
        properties["valuePattern"] = "|".join(_.rsplit("/", 1)[-1] for _ in cwl_p.type.symbols)
    return properties


def get_fragment(uri):
    return uri.rsplit("#", 1)[-1]


def get_relative_uri(uri):
    doc, fragment = uri.rsplit("#", 1)
    return f"{doc.rsplit('/', 1)[-1]}#{fragment}"


def build_step_graph(cwl_wf):
    out_map = {}
    for s in cwl_wf.steps:
        for o in s.out:
            out_map[o] = get_fragment(s.id)
    graph = nx.DiGraph()
    for s in cwl_wf.steps:
        fragment = get_fragment(s.id)
        graph.add_node(fragment)
        for i in s.in_:
            source_fragment = out_map.get(i.source)
            if source_fragment:
                graph.add_edge(source_fragment, fragment)
    return graph


class Thing:

    def __init__(self, id_, label=None):
        self.id_ = id_
        self.label = label

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id_!r})"


class Agent(Thing):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.responsible = None


class SoftwareAgent(Agent):

    def __init__(self, id_, label=None, image=None):
        super().__init__(id_, label=label)
        self.image = image
        self.starter = None
        self.ender = None
        self.start_time = None
        self.end_time = None


class WorkflowEngine(SoftwareAgent):
    pass


class Person(Agent):

    def __init__(self, id_, label=None, name=None):
        super().__init__(id_, label=label)
        self.name = name or label


class Activity(Thing):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.plan = None
        self.starter = None
        self.ender = None
        self.start_time = None
        self.end_time = None
        self.in_params = {}
        self.out_params = {}
        self.steps = []
        self.job_id = None


class ProcessRun(Activity):
    pass


class WorkflowRun(Activity):
    pass


class Entity(Thing):

    def __init__(self, id_, label=None):
        super().__init__(id_, label=label)
        self.value = None
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


class Collection(Artifact):

    def __init__(self, id_):
        super().__init__(id_)
        self.members = []


class KeyEntityPair(Entity):

    def __init__(self, id_, key, entity):
        super().__init__(id_)
        self.key = key
        self.entity = entity

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id_!r}, {self.key!r}, {self.entity!r})"


class Dictionary(Collection):

    def __init__(self, id_, dict_members):
        super().__init__(id_)
        self.dict_members = dict_members

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id_!r}, {self.dict_members!r})"


class Folder(Dictionary):

    def __init__(self, id_, dict_members):
        super().__init__(id_, dict_members)
        self.__basename = None

    @property
    def basename(self):
        if not self.__basename:
            m = hashlib.sha1()
            for pair in self.dict_members:
                path = pair.entity.get_path()
                m.update(path.name.encode())
            self.__basename = m.hexdigest()
        return self.__basename


class Provenance:

    def __init__(self, path_or_file):
        try:
            self.data = json.load(path_or_file)
        except AttributeError:
            with open(path_or_file) as f:
                self.data = json.load(f)
        self.prefixes = self.data["prefix"]
        self.agents = self.__read_agents()
        self.activities = self.__read_activities()
        self.entities = self.__read_entities()
        self.items = {}
        for d in self.agents, self.activities, self.entities:
            self.items.update(d)
        self.__read_members()
        self.__read_specializations()
        self.__read_start_end()
        self.__read_params()
        self.__read_associations()
        self.__read_delegations()

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
            if isinstance(record, list) and "prov:has_provenance" in chain(*record):
                raise RuntimeError("sub-workflows not supported yet")
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
            elif "prov:KeyEntityPair" in types:
                key = record["prov:pairKey"][0]
                entity = record["prov:pairEntity"][0]
                entities[id_] = KeyEntityPair(id_, key, entity)
            elif "ro:Folder" in types:
                assert "prov:Dictionary" in types
                entities[id_] = Folder(id_, record["prov:hadDictionaryMember"])
            elif "prov:Dictionary" in types:
                entities[id_] = Dictionary(id_, record["prov:hadDictionaryMember"])
            elif "prov:Collection" in types:
                entities[id_] = Collection(id_)
            elif "wfprov:Artifact" in types:
                entities[id_] = Artifact(id_, label=record.get("prov:label", [None])[0])
            else:
                entities[id_] = Entity(id_, label=record.get("prov:label", [None])[0])
            entities[id_].value = record.get("prov:value", [None])[0]
            try:
                entities[id_].subprocesses = record["wfdesc:hasSubProcess"]
            except KeyError:
                pass
        for id_, e in entities.items():
            if hasattr(e, "subprocesses"):
                e.subprocesses = [entities[_] for _ in e.subprocesses]
            if hasattr(e, "entity"):
                e.entity = entities[e.entity]
            if hasattr(e, "dict_members"):
                e.dict_members = [entities[_] for _ in e.dict_members]
        return entities

    def __read_members(self):
        for dummy, record in self.data.get("hadMember", {}).items():
            collection = self.entities.get(record.get("prov:collection"))
            assert isinstance(collection, Collection)
            member = self.entities.get(record.get("prov:entity"))
            collection.members.append(member)

    def __read_specializations(self):
        for dummy, record in self.data.get("specializationOf", {}).items():
            specific = self.entities.get(record.get("prov:specificEntity"))
            if not specific:
                continue
            general = self.entities.get(record.get("prov:generalEntity"))
            if general:
                specific.general_entity = general

    def __read_start_end(self):
        # "prov:activity" and "prov:starter" point to both activities and agents
        for dummy, record in self.data["wasStartedBy"].items():
            started = self.items.get(record.get("prov:activity"))
            if started:
                starter = self.items.get(record.get("prov:starter"))
                if starter:
                    started.starter = starter
                started.start_time = record.get("prov:time")
        for dummy, record in self.data["wasEndedBy"].items():
            ended = self.items.get(record.get("prov:activity"))
            if ended:
                ender = self.items.get(record.get("prov:ender"))
                if ender:
                    ended.ender = ender
                ended.end_time = record.get("prov:time")

    def __read_params(self):
        # In the case of a single tool run, cwltool reports one WorkflowRun
        # and no ProcessRun. In this case, some parameters are duplicated and
        # the duplicate's role has the original workflow name as the step part
        single_tool = not any(type(_) is ProcessRun for _ in self.activities.values())
        for dummy, record in self.data.get("used", {}).items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            entity = self.entities.get(record.get("prov:entity"))
            if entity:
                role = record["prov:role"]["$"]
                if single_tool and len(role.split("/")) > 2:
                    continue
                activity.in_params[role] = entity
        for dummy, record in self.data.get("wasGeneratedBy", {}).items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            entity = self.entities.get(record.get("prov:entity"))
            if entity:
                role = record["prov:role"]["$"]
                # workflow output roles have a phantom "primary" step (cwltool bug?)
                parts = role.split("/")
                try:
                    p = parts.pop(1)
                    if p == "primary":
                        role = "/".join(parts)
                except IndexError:
                    pass
                if single_tool and len(parts) > 2:
                    continue
                activity.out_params[role] = entity

    def __read_associations(self):
        is_plan_for = {}
        for dummy, record in self.data["wasAssociatedWith"].items():
            activity = self.activities.get(record.get("prov:activity"))
            if not activity:
                continue
            # TODO: agents; note that there can be many agents for an activity
            plan_id = record.get("prov:plan")
            plan = self.entities.get(plan_id)
            if not plan:
                plan = self.__get_plan_for_scatter_job(plan_id)
            if plan:
                activity.plan = plan  # assuming one plan per activity
                is_plan_for.setdefault(plan.id_, []).append(activity)
                activity.job_id = plan_id
        for plan_id, activities in is_plan_for.items():
            plan = self.entities.get(plan_id)
            for act in activities:
                for sp in plan.subprocesses:
                    for step in is_plan_for[sp.id_]:
                        act.steps.append(step)

    def __get_plan_for_scatter_job(self, plan_id):
        if not plan_id:
            return None
        m = SCATTER_JOB_PATTERN.match(plan_id)
        if not m:
            return None
        return self.entities.get(m.groups()[0])

    def __read_delegations(self):
        for dummy, record in self.data.get("actedOnBehalfOf", {}).items():
            delegate = self.agents.get(record.get("prov:delegate"))
            if delegate:
                delegate.responsible = self.agents.get(record.get("prov:responsible"))


def get_workflow(wf_path):
    """\
    Read the packed CWL workflow.

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


class ProvCrateBuilder:

    def __init__(self, root, workflow_name=None, license=None):
        self.root = Path(root)
        self.workflow_name = workflow_name
        self.license = license
        self.wf_path = self.root / "workflow" / WORKFLOW_BASENAME
        self.cwl_defs = get_workflow(self.wf_path)
        self.step_maps = self._get_step_maps(self.cwl_defs)
        self.param_map = {}
        self.prov = Provenance(self.root / "metadata" / "provenance" / "primary.cwlprov.json")
        sel = [_ for _ in self.prov.agents.values() if type(_) == WorkflowEngine]
        if len(sel) != 1:
            raise ValueError(f"Unexpected number of workflow engines: {len(sel)}")
        self.engine = sel[0]
        sel = [_ for _ in self.prov.activities.values() if type(_) == WorkflowRun]
        if len(sel) != 1:
            raise ValueError(f"Unexpected number of workflow runs: {len(sel)}")
        self.workflow_run = sel[0]
        self.agent = getattr(self.engine.starter, "responsible", None)
        # avoid duplicates - not handled by ro-crate-py, see
        # https://github.com/ResearchObject/ro-crate-py/issues/132
        self.control_actions = {}

    @staticmethod
    def _get_step_maps(cwl_defs):
        rval = {}
        for k, v in cwl_defs.items():
            if hasattr(v, "steps"):
                graph = build_step_graph(v)
                pos_map = {f: i for i, f in enumerate(nx.topological_sort(graph))}
                rval[k] = {}
                for s in v.steps:
                    f = get_fragment(s.id)
                    rval[k][f] = {"tool": get_fragment(s.run), "pos": pos_map[f]}
        return rval

    def build(self):
        crate = ROCrate(gen_preview=False)
        self.add_workflow(crate)
        self.add_engine_run(crate)
        self.add_action(crate, self.workflow_run)
        self.add_param_connections()
        return crate

    def add_workflow(self, crate):
        lang_version = self.cwl_defs[WORKFLOW_BASENAME].cwlVersion
        properties = {
            "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow", "HowTo"],
            "name": self.workflow_name or self.wf_path.name
        }
        workflow = crate.add_workflow(
            self.wf_path, self.wf_path.name, main=True, lang="cwl",
            lang_version=lang_version, gen_cwl=False, properties=properties
        )
        if self.license:
            crate.root_dataset["license"] = self.license
        cwl_workflow = self.cwl_defs[workflow.id]
        workflow["input"] = self.add_params(crate, cwl_workflow.inputs)
        workflow["output"] = self.add_params(crate, cwl_workflow.outputs)
        for s in getattr(cwl_workflow, "steps", []):
            step_fragment = get_fragment(s.id)
            step_id = f"{workflow.id}#{step_fragment}"
            pos = self.step_maps[workflow.id][step_fragment]["pos"]
            step = crate.add(ContextEntity(crate, step_id, properties={
                "@type": "HowToStep",
                "position": str(pos),
            }))
            tool = self.add_tool(crate, workflow, s.run)
            step["workExample"] = tool
            workflow.append_to("step", step)
        return workflow

    def add_tool(self, crate, workflow, cwl_tool):
        if isinstance(cwl_tool, str):
            tool_fragment = get_fragment(cwl_tool)
            cwl_tool = self.cwl_defs[tool_fragment]
        else:
            tool_fragment = get_fragment(cwl_tool.id)
        tool_id = f"{workflow.id}#{tool_fragment}"
        tool = crate.dereference(tool_id)
        if tool:
            return tool
        if hasattr(cwl_tool, "steps"):
            raise RuntimeError("subworkflows not supported yet")
        if hasattr(cwl_tool, "expression"):
            raise RuntimeError("ExpressionTool not supported yet")
        properties = {"name": tool_fragment}
        if cwl_tool.doc:
            properties["description"] = cwl_tool.doc
        tool = crate.add(SoftwareApplication(crate, tool_id, properties=properties))
        tool["input"] = self.add_params(crate, cwl_tool.inputs)
        tool["output"] = self.add_params(crate, cwl_tool.outputs)
        workflow.append_to("hasPart", tool)
        return tool

    def add_params(self, crate, cwl_params):
        params = []
        for cwl_p in cwl_params:
            p_id = get_relative_uri(cwl_p.id)
            properties = properties_from_cwl_param(cwl_p)
            properties["name"] = get_fragment(p_id)
            p = crate.add(ContextEntity(crate, p_id, properties=properties))
            params.append(p)
            self.param_map[p_id] = p
        return params

    def add_engine_run(self, crate):
        roc_engine = crate.add(SoftwareApplication(crate, properties={
            "name": self.engine.label or "workflow engine"
        }))
        roc_engine_run = crate.add(ContextEntity(crate, properties={
            "@type": "OrganizeAction",
            "name": f"Run of {roc_engine['name']}",
            "startTime": self.engine.start_time,
        }))
        roc_engine_run["instrument"] = roc_engine
        if isinstance(self.agent, Person):
            agent_id = None
            try:
                prefix, ref = self.agent.id_.split(":", 1)
            except ValueError:
                pass
            else:
                if prefix == "orcid":
                    agent_id = self.prov.prefixes.get("orcid", "https://orcid.org/") + ref
                elif prefix == "id":
                    agent_id = "#" + ref
            roc_engine_run["agent"] = crate.add(ContextEntity(crate, agent_id, properties={
                "@type": "Person",
                "name": self.agent.name
            }))
        crate.root_dataset["mentions"] = [roc_engine_run]

    def add_action(self, crate, activity, parent_instrument=None):
        workflow = crate.mainEntity
        roc_engine_run = crate.root_dataset["mentions"][0]
        action = crate.add(ContextEntity(crate, properties={
            "@type": "CreateAction",
            "name": activity.label,
            "startTime": activity.start_time,
            "endTime": activity.end_time,
        }))
        plan_tag = activity.plan.id_.strip().split(":", 1)[-1]
        if isinstance(activity, WorkflowRun):
            if plan_tag != "main":
                raise RuntimeError("sub-workflows not supported yet")
            instrument = workflow
            roc_engine_run["result"] = action

            def to_wf_p(k):
                return k
        else:
            tool_name = self.step_maps[parent_instrument.id][plan_tag]["tool"]
            instrument = crate.dereference(f"{workflow.id}#{tool_name}")
            control_action = self.control_actions.get(plan_tag)
            if not control_action:
                control_action = crate.add(ContextEntity(crate, properties={
                    "@type": "ControlAction",
                    "name": f"orchestrate {tool_name}",
                }))
                step = crate.dereference(f"{workflow.id}#{plan_tag}")
                control_action["instrument"] = step
                roc_engine_run.append_to("object", control_action, compact=True)
                self.control_actions[plan_tag] = control_action
            control_action.append_to("object", action, compact=True)
            job_tag = activity.job_id.strip().split(":", 1)[-1]

            def to_wf_p(k):
                return k.replace(job_tag, tool_name)
        action["instrument"] = instrument
        action["object"] = self.add_action_params(crate, activity, to_wf_p, "in")
        action["result"] = self.add_action_params(crate, activity, to_wf_p, "out")
        for job in activity.steps:
            self.add_action(crate, job, parent_instrument=instrument)

    def add_action_params(self, crate, activity, to_wf_p, io="in"):
        action_params = []
        prov_params = getattr(activity, f"{io}_params")
        for k, v in prov_params.items():
            k = k.replace("wf:", "packed.cwl#")
            wf_p = crate.dereference(to_wf_p(k))
            k = get_fragment(k)
            value = self.convert_param(v, crate)
            if isinstance(v, (File, Folder)):
                action_p = value
            else:
                # FIXME: assuming arrays and records don't have nested structured types
                if isinstance(value, dict):
                    value = [crate.add(ContextEntity(crate, f"#pv-{k}/{nk}", properties={
                        "@type": "PropertyValue",
                        "name": f"{k}/{nk}",
                        "value": nv,
                    })) for nk, nv in value.items()]
                action_p = crate.add(ContextEntity(crate, f"#pv-{k}", properties={
                    "@type": "PropertyValue",
                    "name": k,
                }))
                action_p["value"] = value
            action_p.append_to("exampleOfWork", wf_p, compact=True)
            action_params.append(action_p)
        return action_params

    def convert_param(self, prov_param, crate):
        if isinstance(prov_param, File):
            path = prov_param.get_path()
            action_p = crate.dereference(path.name)
            if not action_p:
                action_p = crate.add_file(self.root / path, path.name)
            return action_p
        if isinstance(prov_param, Folder):
            action_p = crate.dereference(prov_param.basename)
            if not action_p:
                action_p = crate.add_directory(prov_param.basename)
                for pair in prov_param.dict_members:
                    path = pair.entity.get_path()
                    dest = Path(prov_param.basename) / path.name
                    part = crate.dereference(dest.as_posix())
                    if not part:
                        part = crate.add_file(self.root / path, dest)
                    action_p.append_to("hasPart", part)
            return action_p
        if prov_param.value:
            return str(prov_param.value)
        if hasattr(prov_param, "dict_members"):
            return dict(
                (_.key, self.convert_param(_.entity, crate))
                for _ in prov_param.dict_members if _.key != "@id"
            )
        if hasattr(prov_param, "members"):
            return [self.convert_param(_, crate) for _ in prov_param.members]
        raise RuntimeError(f"No value to convert for {prov_param}")

    def add_param_connections(self):
        def connect(source, target):
            source_p = self.param_map[f"{WORKFLOW_BASENAME}#{source}"]
            target_p = self.param_map[f"{WORKFLOW_BASENAME}#{target}"]
            source_p.append_to("connectedTo", target_p, compact=True)
        for wf_name, sm in self.step_maps.items():
            def_ = self.cwl_defs[wf_name]
            out_map = {}
            for step in def_.steps:
                step_name = get_fragment(step.id)
                tool_name = sm[step_name]["tool"]
                for o in step.out:
                    o_name = get_fragment(o)
                    out_map[o_name] = o_name.replace(step_name, tool_name)
            for step in def_.steps:
                step_name = get_fragment(step.id)
                tool_name = sm[step_name]["tool"]
                for mapping in getattr(step, "in_", []):
                    from_param = get_fragment(mapping.source)
                    try:
                        from_param = out_map[from_param]
                    except KeyError:
                        pass  # only needed if source is from another step
                    to_param = get_fragment(mapping.id).replace(step_name, tool_name)
                    connect(from_param, to_param)
            for out in getattr(def_, "outputs", []):
                from_param = out_map[get_fragment(out.outputSource)]
                to_param = get_fragment(out.id)
                connect(from_param, to_param)


def main(args):
    args.root = Path(args.root)
    if not args.output:
        args.output = f"{args.root.name}.crate.zip"
    print(f"generating {args.output}")
    args.output = Path(args.output)
    builder = ProvCrateBuilder(args.root, args.workflow_name, args.license)
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
                        help="top-level directory of the CWLProv RO")
    parser.add_argument("-o", "--output", metavar="DIR OR ZIP",
                        help="output RO-Crate directory or zip file")
    parser.add_argument("-l", "--license", metavar="STRING",
                        help="license URL (or WorkflowHub-accepted id)")
    parser.add_argument("-w", "--workflow-name", metavar="STRING",
                        help="original workflow name")
    main(parser.parse_args())
