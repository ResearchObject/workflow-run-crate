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

from cwlprov_to_crate import make_crate
from rocrate.rocrate import ROCrate


CWL_ID = "https://w3id.org/workflowhub/workflow-ro-crate#cwl"


class Args:
    pass


def test_make_crate(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "revsort-run-1"
    args.output = tmpdir / "revsort-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = "RevSort"
    make_crate(args)
    crate = ROCrate(args.output)
    assert crate.root_dataset["license"] == "Apache-2.0"
    workflow = crate.mainEntity
    assert workflow.id == "packed.cwl"
    assert workflow["name"] == "RevSort"
    tools = workflow["hasPart"]
    assert len(tools) == 2
    for entity in tools:
        assert "SoftwareApplication" in entity.type
    inputs = workflow["input"]
    outputs = workflow["output"]
    assert len(inputs) == 2
    assert len(outputs) == 1
    for entity in inputs + outputs:
        assert "FormalParameter" in entity.type
    assert workflow["programmingLanguage"].id == CWL_ID
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 3
    sel = [_ for _ in actions if _["instrument"] is workflow]
    assert len(sel) == 1
    wf_action = sel[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    wf_objects = wf_action["object"]
    wf_results = wf_action["result"]
    assert len(wf_objects) == 2
    assert len(wf_results) == 1
    for entity in wf_objects:
        if entity.id.endswith("reverse_sort"):
            assert "PropertyValue" in entity.type
            assert entity["value"] == "True"
        else:
            assert "File" in entity.type
            wf_input_file = entity
    wf_output_file = wf_results[0]
    assert "File" in wf_output_file.type
    steps = workflow["step"]
    assert len(steps) == 2
    implements = {}
    for s in steps:
        assert "HowToStep" in s.type
        instrument = s["itemListElement"]
        implements[instrument.id] = s
    for a in actions:
        if a is wf_action:
            continue
        instrument = a["instrument"]
        assert instrument in tools
        step = implements[instrument.id]
        if step.id.endswith("rev"):
            objects = a["object"]
            results = a["result"]
            assert len(objects) == 1
            assert len(results) == 1
            rev_input_file = objects[0]
            assert rev_input_file is wf_input_file
            rev_output_file = results[0]
            assert "File" in rev_output_file.type
        elif step.id.endswith("sorted"):
            objects = a["object"]
            results = a["result"]
            assert len(objects) == 2
            assert len(results) == 1
            for entity in objects:
                if entity.id.endswith("reverse"):
                    assert "PropertyValue" in entity.type
                    assert entity["value"] == "True"
                else:
                    assert entity is rev_output_file
            sorted_output_file = results[0]
            assert sorted_output_file is wf_output_file
        else:
            assert False, f"unexpected step id for action {a.id}: {step.id}"


def test_no_input(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "no-input-run-1"
    args.output = tmpdir / "no-input-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    make_crate(args)
    crate = ROCrate(args.output)
    # The "workflow" is actually a single tool; should we generate a Process
    # Run Crate instead in this case?
    workflow = crate.mainEntity
    assert not workflow.get("hasPart")
    assert not workflow.get("input")
    outputs = workflow["output"]
    assert len(outputs) == 1
    out = outputs[0]
    assert "FormalParameter" in out.type
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 1
    wf_action = actions[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    assert not wf_action.get("object")
    wf_results = wf_action["result"]
    assert len(wf_results) == 1
    res = wf_results[0]
    assert "PropertyValue" in res.type
    assert res["value"] == "42"
    assert res["exampleOfWork"] == out


def test_param_types(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "type-zoo-run-1"
    args.output = tmpdir / "type-zoo-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    make_crate(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    inputs = workflow["input"]
    outputs = workflow["output"]
    assert len(inputs) == 11
    assert len(outputs) == 1
    for entity in inputs + outputs:
        assert "FormalParameter" in entity.type
    input_map = {_.id.rsplit("/", 1)[-1]: _ for _ in inputs}
    # For in_any and in_multi, the type is that of the actual value:
    # the additional information is not reported by cwltool
    assert input_map["in_array"]["additionalType"] == "Text"
    assert input_map["in_any"]["additionalType"] == "Text"
    assert input_map["in_str"]["additionalType"] == "Text"
    assert input_map["in_bool"]["additionalType"] == "Boolean"
    assert input_map["in_int"]["additionalType"] == "Integer"
    assert input_map["in_long"]["additionalType"] == "Integer"
    assert input_map["in_float"]["additionalType"] == "Float"
    assert input_map["in_double"]["additionalType"] == "Float"
    assert input_map["in_enum"]["additionalType"] == "Text"
    assert input_map["in_record"]["additionalType"] == "PropertyValue"
    assert input_map["in_multi"]["additionalType"] == "Float"
    out = outputs[0]
    assert out["additionalType"] == "File"
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 1
    action = actions[0]
    assert crate.root_dataset["mentions"] == [action]
    objects = action["object"]
    assert len(objects) == 11
    for obj in objects:
        assert "PropertyValue" in obj.type
    obj_map = {_.id.rsplit("/", 1)[-1]: _ for _ in objects}
    assert obj_map["in_array"]["value"] == ["foo", "bar"]
    assert obj_map["in_any"]["value"] == "tar"
    assert obj_map["in_str"]["value"] == "spam"
    assert obj_map["in_bool"]["value"] == "True"
    assert obj_map["in_int"]["value"] == "42"
    assert obj_map["in_long"]["value"] == "420"
    assert obj_map["in_float"]["value"] == "3.14"
    assert obj_map["in_double"]["value"] == "3.142"
    assert obj_map["in_enum"]["value"] == "B"
    record_pv = obj_map["in_record"]
    v_A = crate.dereference(f"{record_pv.id}/in_record_A")
    assert v_A["value"] == "Tom"
    v_B = crate.dereference(f"{record_pv.id}/in_record_B")
    assert v_B["value"] == "Jerry"
    assert set(record_pv["value"]) == {v_A, v_B}
    assert obj_map["in_multi"]["value"] == "9.99"
    results = action["result"]
    assert len(results) == 1
    res = results[0]
    assert "File" in res.type
