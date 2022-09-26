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
from pathlib import Path

import networkx as nx
import prov.model
from bdbag.bdbagit import BDBag
from cwl_utils.parser import load_document_by_yaml
from cwlprov.ro import ResearchObject
from cwlprov.prov import Provenance
from cwlprov.utils import first
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


def get_step_part(relative_uri):
    parts = relative_uri.split("/", 2)
    if len(parts) > 2:
        return parts[1]


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
        self.ro = ResearchObject(BDBag(str(root)))
        self.with_prov = set(str(_) for _ in self.ro.resources_with_provenance())
        self.prov = Provenance(self.ro)
        self.workflow_run = self.prov.activity()
        self.roc_engine_run = None
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

    def _resolve_plan(self, activity):
        job_qname = activity.plan()
        plan = activity.provenance.entity(job_qname)
        if not plan:
            m = SCATTER_JOB_PATTERN.match(str(job_qname))
            if m:
                plan = activity.provenance.entity(m.groups()[0])
        return plan

    def get_members(self, entity):
        membership = self.prov.record_with_attr(
            prov.model.ProvMembership, entity.id, prov.model.PROV_ATTR_COLLECTION
        )
        member_ids = (_.get_attribute(prov.model.PROV_ATTR_ENTITY) for _ in membership)
        return (self.prov.entity(first(_)) for _ in member_ids)

    def get_dict(self, entity):
        d = {}
        for qname in entity.record.get_attribute("prov:hadDictionaryMember"):
            kvp = self.prov.entity(qname)
            key = first(kvp.record.get_attribute("prov:pairKey"))
            entity_id = first(kvp.record.get_attribute("prov:pairEntity"))
            d[key] = self.prov.entity(entity_id)
        return d

    def build(self):
        crate = ROCrate(gen_preview=False)
        self.add_workflow(crate)
        self.add_engine_run(crate)
        self.add_action(crate, self.workflow_run)
        # self.add_param_connections()
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
            self.add_step(crate, workflow, s)
        return workflow

    def add_step(self, crate, workflow, cwl_step):
        step_fragment = get_fragment(cwl_step.id)
        step_id = f"{self.wf_path.name}#{step_fragment}"
        pos = self.step_maps[get_fragment(workflow.id)][step_fragment]["pos"]
        step = crate.add(ContextEntity(crate, step_id, properties={
            "@type": "HowToStep",
            "position": str(pos),
        }))
        tool = self.add_tool(crate, workflow, cwl_step.run)
        step["workExample"] = tool
        workflow.append_to("step", step)

    def add_tool(self, crate, workflow, cwl_tool):
        if isinstance(cwl_tool, str):
            tool_fragment = get_fragment(cwl_tool)
            cwl_tool = self.cwl_defs[tool_fragment]
        else:
            tool_fragment = get_fragment(cwl_tool.id)
        if hasattr(cwl_tool, "expression"):
            raise RuntimeError("ExpressionTool not supported yet")
        tool_id = f"{self.wf_path.name}#{tool_fragment}"
        tool = crate.dereference(tool_id)
        if tool:
            return tool
        properties = {"name": tool_fragment}
        if cwl_tool.doc:
            properties["description"] = cwl_tool.doc
        if hasattr(cwl_tool, "steps"):
            properties["@type"] = ["SoftwareSourceCode", "ComputationalWorkflow", "HowTo"]
        else:
            properties["@type"] = "SoftwareApplication"
        tool = crate.add(ContextEntity(crate, tool_id, properties=properties))
        tool["input"] = self.add_params(crate, cwl_tool.inputs)
        tool["output"] = self.add_params(crate, cwl_tool.outputs)
        workflow.append_to("hasPart", tool)
        if hasattr(cwl_tool, "steps"):
            tool["programmingLanguage"] = workflow["programmingLanguage"]
            for s in getattr(cwl_tool, "steps", []):
                self.add_step(crate, tool, s)
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
        engine = self.workflow_run.start().starter_activity()
        roc_engine = crate.add(SoftwareApplication(crate, properties={
            "name": engine.label or "workflow engine"
        }))
        roc_engine_run = crate.add(ContextEntity(crate, properties={
            "@type": "OrganizeAction",
            "name": f"Run of {roc_engine['name']}",
            "startTime": engine.start().time.isoformat(),
        }))
        roc_engine_run["instrument"] = roc_engine
        self.add_agent(crate, roc_engine_run, engine)
        self.roc_engine_run = roc_engine_run

    def add_agent(self, crate, roc_engine_run, engine):
        delegate = engine.start().starter_activity()
        try:
            delegation = next(self.prov.record_with_attr(
                prov.model.ProvDelegation, delegate.id, prov.model.PROV_ATTR_DELEGATE
            ))
        except StopIteration:
            return
        responsible = delegation.get_attribute(prov.model.PROV_ATTR_RESPONSIBLE)
        agent = sum((self.prov.prov_doc.get_record(_) for _ in responsible), [])
        for a in agent:
            if "prov:Person" not in set(str(_) for _ in a.get_asserted_types()):
                continue
            agent_id = a.identifier.uri
            if not agent_id.startswith("http"):
                agent_id = "#" + agent_id.rsplit(":", 1)[-1]
            ro_a = crate.add(ContextEntity(crate, agent_id, properties={
                "@type": "Person",
                "name": a.label
            }))
            roc_engine_run.append_to("agent", ro_a, compact=True)

    def add_action(self, crate, activity, parent_instrument=None):
        print("add_action for:", repr(activity.label))
        workflow = crate.mainEntity
        action = crate.add(ContextEntity(crate, properties={
            "@type": "CreateAction",
            "name": activity.label,
            # "startTime": activity.start().time.isoformat(),
            # "endTime": activity.end().time.isoformat(),
        }))
        # job_qname = activity.plan()
        # plan = self._resolve_plan(job_qname)
        plan = self._resolve_plan(activity)
        plan_tag = plan.id.localpart
        print("plan_tag:", plan_tag)
        if plan_tag == "main":
            assert str(activity.type) == "wfprov:WorkflowRun"
            instrument = workflow
            self.roc_engine_run["result"] = action
            crate.root_dataset["mentions"] = [action]

            def to_wf_p(k):
                return k
        else:
            tool_name = self.step_maps[parent_instrument.id][plan_tag]["tool"]
            instrument = crate.dereference(f"{workflow.id}#{tool_name}")
            print(" ", tool_name, instrument)
            control_action = self.control_actions.get(plan_tag)
            if not control_action:
                control_action = crate.add(ContextEntity(crate, properties={
                    "@type": "ControlAction",
                    "name": f"orchestrate {tool_name}",
                }))
                step = crate.dereference(f"{workflow.id}#{plan_tag}")
                control_action["instrument"] = step
                self.roc_engine_run.append_to("object", control_action, compact=True)
                self.control_actions[plan_tag] = control_action
            control_action.append_to("object", action, compact=True)
            if activity.uri in self.with_prov:
                nested_prov = Provenance(self.ro, activity.uri)
                activity = nested_prov.activity()
                print("  run_id:", nested_prov.run_id)

            def to_wf_p(k):
                return k.replace(activity.plan().localpart, tool_name)
        action["instrument"] = instrument
        action["object"] = self.add_action_params(crate, activity, to_wf_p, "usage")
        action["result"] = self.add_action_params(crate, activity, to_wf_p, "generation")
        for job in activity.steps():
            self.add_action(crate, job, parent_instrument=instrument)

    def add_action_params(self, crate, activity, to_wf_p, ptype="usage"):
        action_params = []
        print(activity.label)
        for rel in getattr(activity, ptype)():
            k = get_relative_uri(rel.role.uri)
            if str(activity.type) == "wfprov:WorkflowRun":
                # workflow output roles have a phantom step part
                if ptype == "generation":
                    parts = k.split("/", 2)
                    k = parts[0] + "/" + parts[2]
                # In the case of a single tool run, cwltool reports one WorkflowRun
                # and no ProcessRun. In this case, some parameters are duplicated and
                # the duplicate's role has the original workflow name as the step part
                if not list(activity.steps()) and get_step_part(k):
                    continue
            wf_p = crate.dereference(to_wf_p(k))
            print("  k =", k, "| wf_p =", wf_p)
            k = get_fragment(k)
            v = rel.entity()
            print("  v =", v)
            value = self.convert_param(v, crate)
            if {"ro:Folder", "wf4ever:File"} & set(str(_) for _ in v.types()):
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
        type_names = frozenset(str(_) for _ in prov_param.types())
        if "wf4ever:File" in type_names:
            hash_ = next(prov_param.specializationOf()).id.localpart
            path = self.root / Path("data") / hash_[:2] / hash_
            action_p = crate.dereference(path.name)
            if not action_p:
                action_p = crate.add_file(path, path.name)
            return action_p
        if "ro:Folder" in type_names:
            hashes = []
            for prov_file in self.get_dict(prov_param).values():
                hash_ = next(prov_file.specializationOf()).id.localpart
                hashes.append(hash_)
            m = hashlib.sha1()
            m.update("".join(sorted(hashes)).encode())
            basename = m.hexdigest()
            action_p = crate.dereference(basename)
            if not action_p:
                action_p = crate.add_directory(basename)
                for hash_ in hashes:
                    path = self.root / Path("data") / hash_[:2] / hash_
                    dest = Path(basename) / path.name
                    part = crate.dereference(dest.as_posix())
                    if not part:
                        part = crate.add_file(self.root / path, dest)
                    action_p.append_to("hasPart", part)
            return action_p
        if prov_param.value is not None:
            return str(prov_param.value)
        if "prov:Dictionary" in type_names:
            return dict(
                (k, self.convert_param(v, crate))
                for k, v in self.get_dict(prov_param).items()
                if k != "@id"
            )
        if "prov:Collection" in type_names:
            return [self.convert_param(_, crate) for _ in self.get_members(prov_param)]
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
