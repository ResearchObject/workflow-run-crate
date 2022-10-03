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

from cwlprov_to_crate import main
from rocrate.rocrate import ROCrate


CWL_ID = "https://w3id.org/workflowhub/workflow-ro-crate#cwl"
GALAXY_ID = "https://w3id.org/workflowhub/workflow-ro-crate#galaxy"


class Args:
    pass


def test_revsort(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "revsort-run-1"
    args.output = tmpdir / "revsort-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = "RevSort"
    args.workflow_type = None
    main(args)
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
    input_map = {_.id.rsplit("/", 1)[-1]: _ for _ in inputs}
    assert input_map["input"]["additionalType"] == "File"
    assert "encodingFormat" in input_map["input"]
    assert input_map["input"]["defaultValue"] == "file:///home/stain/src/cwltool/tests/wf/hello.txt"
    assert input_map["reverse_sort"]["additionalType"] == "Boolean"
    assert input_map["reverse_sort"]["defaultValue"] == "True"
    assert outputs[0]["additionalType"] == "File"
    assert workflow["programmingLanguage"].id == CWL_ID
    sel = [_ for _ in crate.contextual_entities if "OrganizeAction" in _.type]
    assert len(sel) == 1
    engine_action = sel[0]
    assert "SoftwareApplication" in engine_action["instrument"].type
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 3
    sel = [_ for _ in actions if _["instrument"] is workflow]
    assert len(sel) == 1
    wf_action = sel[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    assert engine_action["result"] is wf_action
    control_actions = engine_action["object"]
    assert len(control_actions) == 2
    assert all(_.type == "ControlAction" for _ in control_actions)
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
    assert all(_.type == "HowToStep" for _ in steps)
    for control_a in control_actions:
        step = control_a["instrument"]
        create_a = control_a["object"]
        instrument = create_a["instrument"]
        assert instrument is step["workExample"]
        assert instrument in tools
        objects = create_a["object"]
        results = create_a["result"]
        if step.id.endswith("rev"):
            assert len(objects) == 1
            assert len(results) == 1
            rev_input_file = objects[0]
            assert rev_input_file is wf_input_file
            rev_output_file = results[0]
            assert "File" in rev_output_file.type
            assert step["position"] == "0"
        elif step.id.endswith("sorted"):
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
            assert step["position"] == "1"
        else:
            assert False, f"unexpected step id: {step.id}"
    # parameter connections
    sorted_output = crate.get("packed.cwl#sorttool.cwl/output")
    main_output = crate.get("packed.cwl#main/output")
    assert sorted_output["connectedTo"] is main_output
    main_input = crate.get("packed.cwl#main/input")
    rev_input = crate.get("packed.cwl#revtool.cwl/input")
    assert main_input["connectedTo"] is rev_input
    rev_output = crate.get("packed.cwl#revtool.cwl/output")
    sorted_input = crate.get("packed.cwl#sorttool.cwl/input")
    assert rev_output["connectedTo"] is sorted_input
    main_reverse_sort = crate.get("packed.cwl#main/reverse_sort")
    sorted_reverse = crate.get("packed.cwl#sorttool.cwl/reverse")
    assert main_reverse_sort["connectedTo"] is sorted_reverse
    # file contents
    in_text = (args.root / "data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376").read_text()
    assert (args.output / wf_input_file.id).read_text() == in_text
    rev_out_text = (args.root / "data/97/97fe1b50b4582cebc7d853796ebd62e3e163aa3f").read_text()
    assert (args.output / rev_output_file.id).read_text() == rev_out_text
    out_text = (args.root / "data/b9/b9214658cc453331b62c2282b772a5c063dbd284").read_text()
    assert (args.output / wf_output_file.id).read_text() == out_text


def test_no_input(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "no-input-run-1"
    args.output = tmpdir / "no-input-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    args.workflow_type = None
    main(args)
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
    sel = [_ for _ in crate.contextual_entities if "OrganizeAction" in _.type]
    assert len(sel) == 1
    engine_action = sel[0]
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 1
    wf_action = actions[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    assert engine_action["result"] is wf_action
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
    args.workflow_type = None
    main(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    inputs = workflow["input"]
    outputs = workflow["output"]
    assert len(inputs) == 11
    assert len(outputs) == 1
    for entity in inputs + outputs:
        assert "FormalParameter" in entity.type
    input_map = {_.id.rsplit("/", 1)[-1]: _ for _ in inputs}
    assert input_map["in_array"]["additionalType"] == "Text"
    assert input_map["in_array"]["multipleValues"] == "True"
    assert input_map["in_any"]["additionalType"] == "DataType"
    assert input_map["in_str"]["additionalType"] == "Text"
    assert input_map["in_bool"]["additionalType"] == "Boolean"
    assert input_map["in_int"]["additionalType"] == "Integer"
    assert input_map["in_long"]["additionalType"] == "Integer"
    assert input_map["in_float"]["additionalType"] == "Float"
    assert input_map["in_double"]["additionalType"] == "Float"
    assert input_map["in_enum"]["additionalType"] == "Text"
    assert input_map["in_enum"]["valuePattern"] == "A|B"
    assert input_map["in_record"]["additionalType"] == "PropertyValue"
    assert input_map["in_record"]["multipleValues"] == "True"
    assert set(input_map["in_multi"]["additionalType"]) == {"Integer", "Float"}
    assert input_map["in_multi"]["defaultValue"] == "9.99"
    assert input_map["in_multi"]["valueRequired"] == "False"
    out = outputs[0]
    assert out["additionalType"] == "File"
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 1
    action = actions[0]
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


def test_dir_io(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "grepucase-run-1"
    args.output = tmpdir / "grepucase-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    args.workflow_type = None
    main(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    assert workflow.id == "packed.cwl"
    tools = workflow["hasPart"]
    assert len(tools) == 2
    inputs = workflow["input"]
    outputs = workflow["output"]
    assert len(inputs) == 2
    assert len(outputs) == 1
    input_map = {_.id.rsplit("/", 1)[-1]: _ for _ in inputs}
    assert input_map["in_dir"]["additionalType"] == "Dataset"
    assert input_map["pattern"]["additionalType"] == "Text"
    assert outputs[0]["additionalType"] == "Dataset"
    action_map = {_["instrument"].id: _ for _ in crate.contextual_entities
                  if "CreateAction" in _.type}
    assert len(action_map) == 3
    wf_action = action_map["packed.cwl"]
    assert wf_action["instrument"] is workflow
    wf_objects = wf_action["object"]
    wf_results = wf_action["result"]
    assert len(wf_objects) == 2
    assert len(wf_results) == 1
    for entity in wf_objects:
        if entity.id.endswith("pattern"):
            assert "PropertyValue" in entity.type
            assert entity["value"] == "lazy"
        else:
            assert "Dataset" in entity.type
            wf_input_dir = entity
    wf_output_dir = wf_results[0]
    assert "Dataset" in wf_output_dir.type
    greptool_action = action_map["packed.cwl#greptool.cwl"]
    greptool_objects = greptool_action["object"]
    greptool_results = greptool_action["result"]
    assert len(greptool_objects) == 2
    assert len(greptool_results) == 1
    for entity in greptool_objects:
        if entity.id.endswith("pattern"):
            assert "PropertyValue" in entity.type
            assert entity["value"] == "lazy"
        else:
            assert "Dataset" in entity.type
            greptool_input_dir = entity
    assert greptool_input_dir is wf_input_dir
    greptool_output_dir = greptool_results[0]
    assert "Dataset" in greptool_output_dir.type
    ucasetool_action = action_map["packed.cwl#ucasetool.cwl"]
    ucasetool_objects = ucasetool_action["object"]
    ucasetool_results = ucasetool_action["result"]
    assert len(ucasetool_objects) == 1
    assert len(ucasetool_results) == 1
    ucasetool_input_dir = ucasetool_objects[0]
    assert ucasetool_input_dir is greptool_output_dir
    ucasetool_output_dir = ucasetool_results[0]
    assert "Dataset" in ucasetool_output_dir.type
    # file contents
    in_text = {
        (args.root / "data/8d/8d84ef91f0aba379f5edc3836b4b5f6727920f22").read_text(),
        (args.root / "data/d6/d60dd58346cf7e533252f35399cd510b1b1467f7").read_text(),
    }
    assert set((args.output / _.id).read_text() for _ in wf_input_dir["hasPart"]) == in_text
    grep_out_text = {
        (args.root / "data/85/8545949f96b96cb721485066bafad9b768bc4e52").read_text(),
        (args.root / "data/5a/5aa9aa3b336778cf2a7db648fc530892c3b3dabb").read_text(),
    }
    assert set(
        (args.output / _.id).read_text() for _ in greptool_output_dir["hasPart"]
    ) == grep_out_text
    out_text = {
        (args.root / "data/3c/3ccdc7533084b641e6c941cc6dbb091d2e5f8a41").read_text(),
        (args.root / "data/ec/ec0270052a78321508502ed915815c4daf75fe46").read_text(),
    }
    assert set((args.output / _.id).read_text() for _ in wf_output_dir["hasPart"]) == out_text


def test_no_output(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "no-output-run-1"
    args.output = tmpdir / "no-output-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    args.workflow_type = None
    main(args)
    crate = ROCrate(args.output)
    assert crate.root_dataset["license"] == "Apache-2.0"
    workflow = crate.mainEntity
    tools = workflow["hasPart"]
    assert len(tools) == 2
    for entity in tools:
        assert "SoftwareApplication" in entity.type
    inputs = workflow["input"]
    assert not workflow.get("output")
    assert len(inputs) == 3
    for entity in inputs:
        assert "FormalParameter" in entity.type
    input_map = {_.id.rsplit("/", 1)[-1]: _ for _ in inputs}
    for n in "sabdab_file", "pdb_array":
        assert input_map[f"{n}"]["additionalType"] == "File"
    assert input_map["pdb_array"]["multipleValues"] == "True"
    assert input_map["pdb_dir"]["additionalType"] == "Dataset"
    sel = [_ for _ in crate.contextual_entities if "OrganizeAction" in _.type]
    assert len(sel) == 1
    engine_action = sel[0]
    assert "SoftwareApplication" in engine_action["instrument"].type
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 5
    sel = [_ for _ in actions if _["instrument"] is workflow]
    assert len(sel) == 1
    wf_action = sel[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    assert engine_action["result"] is wf_action
    control_actions = engine_action["object"]
    assert len(control_actions) == 3
    assert all(_.type == "ControlAction" for _ in control_actions)
    wf_objects = wf_action["object"]
    assert not wf_action.get("result")
    assert len(wf_objects) == 3
    wf_object_map = {_.id.rsplit("-", 1)[-1]: _ for _ in wf_objects}
    in_array = wf_object_map["main/pdb_array"]
    assert "PropertyValue" in in_array.type
    assert in_array["exampleOfWork"] is input_map["pdb_array"]
    array_files = in_array["value"]
    assert len(array_files) == 2
    for e in array_files:
        assert "File" in e.type
    in_file = wf_object_map["5e026d2a039e60827d3834596a8c30256aa85e57"]
    assert "File" in in_file.type
    assert input_map["sabdab_file"] in in_file["exampleOfWork"]
    in_dir = [_ for _ in wf_objects if _ is not in_array and _ is not in_file][0]
    assert "Dataset" in in_dir.type
    assert input_map["pdb_dir"] in in_dir["exampleOfWork"]
    dir_files = in_dir["hasPart"]
    for e in dir_files:
        assert "File" in e.type
    steps = workflow["step"]
    assert len(steps) == 3
    assert all(_.type == "HowToStep" for _ in steps)
    for control_a in control_actions:
        step = control_a["instrument"]
        step_tag = step.id.rsplit("/", 1)[-1]
        create_actions = control_a["object"]
        if step_tag == "date2_step":
            assert isinstance(create_actions, list)
            assert len(create_actions) == 2
            date2_in_files = [_["object"][0] for _ in create_actions]
            assert set(date2_in_files) == set(array_files)
        else:
            create_actions = [create_actions]
        for create_a in create_actions:
            instrument = create_a["instrument"]
            assert instrument is step["workExample"]
            assert instrument in tools
            objects = create_a["object"]
            assert not create_a.get("result")
            if step_tag == "date_step":
                assert len(objects) == 1
                date_in_file = objects[0]
                assert date_in_file is in_file
            elif step_tag == "echo_step":
                assert len(objects) == 2
                for obj in objects:
                    if "Dataset" in obj.type:
                        assert obj is in_dir
                    else:
                        assert obj is in_file
            elif step_tag == "date2_step":
                assert len(objects) == 1
    # parameter connections
    main_file = crate.get("packed.cwl#main/sabdab_file")
    main_dir = crate.get("packed.cwl#main/pdb_dir")
    main_array = crate.get("packed.cwl#main/pdb_array")
    date_file = crate.get("packed.cwl#date.cwl/file")
    echo_file = crate.get("packed.cwl#echo.cwl/input_file")
    echo_dir = crate.get("packed.cwl#echo.cwl/input_dir")
    assert set(main_file["connectedTo"]) == {date_file, echo_file}
    assert main_dir["connectedTo"] is echo_dir
    assert main_array["connectedTo"] is date_file
    # file contents
    text_7mb7 = (args.root / "data/4b/4b22356928446475c8ae5869968c9777374a76e8").read_text()
    text_7zxf = (args.root / "data/4e/4ebd7d222d9b6095fa96ee395905ce7f6d415381").read_text()
    assert set((args.output / _.id).read_text() for _ in array_files) == {text_7mb7, text_7zxf}
    text_sabdab = (args.root / "data/5e/5e026d2a039e60827d3834596a8c30256aa85e57").read_text()
    assert (args.output / in_file.id).read_text() == text_sabdab
    text_1ahw = (args.root / "data/bc/bc2f32ad8584e85e6e3b184a6dc565bdd6571821").read_text()
    text_1kip = (args.root / "data/da/da261f1082f318fbda173dc3228d7475433fd886").read_text()
    assert set((args.output / _.id).read_text() for _ in dir_files) == {text_1ahw, text_1kip}


def test_scatter_pvs(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "echo-scatter-run-1"
    args.output = tmpdir / "echo-scatter-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    args.workflow_type = None
    main(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    tools = workflow["hasPart"]
    assert len(tools) == 1
    wf_inputs = workflow["input"]
    assert not workflow.get("output")
    assert len(wf_inputs) == 1
    wf_in = wf_inputs[0]
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    assert len(actions) == 3
    sel = [_ for _ in actions if _["instrument"] is workflow]
    assert len(sel) == 1
    wf_action = sel[0]
    wf_objects = wf_action["object"]
    assert len(wf_objects) == 1
    wf_obj = wf_objects[0]
    assert "PropertyValue" in wf_obj.type
    assert wf_obj["exampleOfWork"] is wf_in
    assert set(wf_obj["value"]) == {"foo", "bar"}
    job_values = set()
    for a in actions:
        if a is wf_action:
            continue
        objects = a["object"]
        assert len(objects) == 1
        job_values.add(objects[0]["value"])
    assert job_values == {"foo", "bar"}


def test_subworkflows(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "revsortlcase-run-1"
    args.output = tmpdir / "revsortlcase-run-1-crate"
    args.license = "Apache-2.0"
    args.workflow_name = None
    args.workflow_type = None
    main(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    wf_inputs = {_.id: _ for _ in workflow["input"]}
    assert set(wf_inputs) == {
        "packed.cwl#main/descending_sort",
        "packed.cwl#main/revsortlcase_in"
    }
    wf_outputs = {_.id: _ for _ in workflow["output"]}
    assert set(wf_outputs) == {
        "packed.cwl#main/revsortlcase_out"
    }
    wf_tools = {_.id: _ for _ in workflow["hasPart"]}
    assert set(wf_tools) == {
        "packed.cwl#revsort.cwl",
        "packed.cwl#lcasetool.cwl"
    }
    wf_steps = {_.id: _ for _ in workflow["step"]}
    assert set(wf_steps) == {
        "packed.cwl#main/revsort",
        "packed.cwl#main/lcase"
    }
    revsort = wf_tools["packed.cwl#revsort.cwl"]
    assert set(revsort.type) == {"SoftwareSourceCode", "ComputationalWorkflow", "HowTo"}
    assert revsort["programmingLanguage"] is workflow["programmingLanguage"]
    rs_inputs = {_.id: _ for _ in revsort["input"]}
    assert set(rs_inputs) == {
        "packed.cwl#revsort.cwl/reverse_sort",
        "packed.cwl#revsort.cwl/revsort_in"
    }
    rs_outputs = {_.id: _ for _ in revsort["output"]}
    assert set(rs_outputs) == {
        "packed.cwl#revsort.cwl/revsort_out"
    }
    rs_tools = {_.id: _ for _ in revsort["hasPart"]}
    assert set(rs_tools) == {
        "packed.cwl#revtool.cwl",
        "packed.cwl#sorttool.cwl"
    }
    rs_steps = {_.id: _ for _ in revsort["step"]}
    assert set(rs_steps) == {
        "packed.cwl#revsort.cwl/rev",
        "packed.cwl#revsort.cwl/sorted"
    }
    rev = rs_tools["packed.cwl#revtool.cwl"]
    rev_inputs = {_.id: _ for _ in rev["input"]}
    assert set(rev_inputs) == {
        "packed.cwl#revtool.cwl/rev_in"
    }
    rev_outputs = {_.id: _ for _ in rev["output"]}
    assert set(rev_outputs) == {
        "packed.cwl#revtool.cwl/rev_out"
    }
    sort = rs_tools["packed.cwl#sorttool.cwl"]
    sort_inputs = {_.id: _ for _ in sort["input"]}
    assert set(sort_inputs) == {
        "packed.cwl#sorttool.cwl/sort_in",
        "packed.cwl#sorttool.cwl/reverse"
    }
    sort_outputs = {_.id: _ for _ in sort["output"]}
    assert set(sort_outputs) == {
        "packed.cwl#sorttool.cwl/sort_out"
    }
    lcase = wf_tools["packed.cwl#lcasetool.cwl"]
    lcase_inputs = {_.id: _ for _ in lcase["input"]}
    assert set(lcase_inputs) == {
        "packed.cwl#lcasetool.cwl/lcase_in",
    }
    lcase_outputs = {_.id: _ for _ in lcase["output"]}
    assert set(lcase_outputs) == {
        "packed.cwl#lcasetool.cwl/lcase_out"
    }
    actions = {_["instrument"].id: _ for _ in crate.contextual_entities
               if "CreateAction" in _.type}
    assert set(actions) == {
        "packed.cwl",
        "packed.cwl#revsort.cwl",
        "packed.cwl#revtool.cwl",
        "packed.cwl#sorttool.cwl",
        "packed.cwl#lcasetool.cwl",
    }
    wf_action = actions["packed.cwl"]
    wf_objects = {_.type: _ for _ in wf_action["object"]}
    assert set(wf_objects) == {"File", "PropertyValue"}
    assert wf_objects["PropertyValue"]["value"] == "True"
    wf_results = {_.type: _ for _ in wf_action["result"]}
    assert set(wf_results) == {"File"}
    # revsort_in missing from retrospective provenance (cwltool bug?)
    # also, the value for reverse_sort is False
    rs_action = actions["packed.cwl#revsort.cwl"]
    # rs_objects = {_.type: _ for _ in rs_action["object"]}
    # assert set(rs_objects) == {"File", "PropertyValue"}
    # assert rs_objects["PropertyValue"]["value"] == "True"
    rs_results = {_.type: _ for _ in rs_action["result"]}
    assert set(rs_results) == {"File"}
    rev_action = actions["packed.cwl#revtool.cwl"]
    rev_objects = {_.type: _ for _ in rev_action["object"]}
    assert set(rev_objects) == {"File"}
    rev_results = {_.type: _ for _ in rev_action["result"]}
    assert set(rev_results) == {"File"}
    sort_action = actions["packed.cwl#sorttool.cwl"]
    sort_objects = {_.type: _ for _ in sort_action["object"]}
    assert set(sort_objects) == {"File", "PropertyValue"}
    assert sort_objects["PropertyValue"]["value"] == "True"
    sort_results = {_.type: _ for _ in sort_action["result"]}
    assert set(sort_results) == {"File"}
    lcase_action = actions["packed.cwl#lcasetool.cwl"]
    lcase_objects = {_.type: _ for _ in lcase_action["object"]}
    assert set(lcase_objects) == {"File"}
    lcase_results = {_.type: _ for _ in lcase_action["result"]}
    assert set(lcase_results) == {"File"}
    # parameter connections
    assert wf_inputs["packed.cwl#main/revsortlcase_in"]["connectedTo"] == \
        rs_inputs["packed.cwl#revsort.cwl/revsort_in"]
    assert wf_inputs["packed.cwl#main/descending_sort"]["connectedTo"] == \
        rs_inputs["packed.cwl#revsort.cwl/reverse_sort"]
    assert lcase_outputs["packed.cwl#lcasetool.cwl/lcase_out"]["connectedTo"] == \
        wf_outputs["packed.cwl#main/revsortlcase_out"]
    assert rs_inputs["packed.cwl#revsort.cwl/revsort_in"]["connectedTo"] == \
        rev_inputs["packed.cwl#revtool.cwl/rev_in"]
    assert rs_inputs["packed.cwl#revsort.cwl/reverse_sort"]["connectedTo"] == \
        sort_inputs["packed.cwl#sorttool.cwl/reverse"]
    assert sort_outputs["packed.cwl#sorttool.cwl/sort_out"]["connectedTo"] == \
        rs_outputs["packed.cwl#revsort.cwl/revsort_out"]
    assert rev_outputs["packed.cwl#revtool.cwl/rev_out"]["connectedTo"] == \
        sort_inputs["packed.cwl#sorttool.cwl/sort_in"]
    assert rs_outputs["packed.cwl#revsort.cwl/revsort_out"]["connectedTo"] == \
        lcase_inputs["packed.cwl#lcasetool.cwl/lcase_in"]
    # file contents
    in_text = (args.root / "data/7c/7cb1a4da14ba3e91b983b30e7689e3902bcd2034").read_text()
    assert (args.output / wf_objects["File"].id).read_text() == in_text
    rev_out_text = (args.root / "data/54/542758e6e55bb880c05e2de68a3897bfab37c990").read_text()
    assert (args.output / rev_results["File"].id).read_text() == rev_out_text
    sorted_text = (args.root / "data/13/134bede4fd3827851f861713ed34168b6efb2806").read_text()
    assert (args.output / sort_results["File"].id).read_text() == sorted_text
    out_text = (args.root / "data/aa/aaf167286572f8b5d5c592b94aff678d0997947f").read_text()
    assert (args.output / wf_results["File"].id).read_text() == out_text


def test_ga_export(data_dir, tmpdir):
    args = Args()
    args.root = data_dir / "test_ga_history_export" / "history_export"
    args.output = tmpdir / "ga-export-crate"
    args.license = None
    args.workflow_name = None
    args.workflow_type = "galaxy"
    main(args)
    crate = ROCrate(args.output)
    workflow = crate.mainEntity
    assert workflow.id == "ga_export.ga"
    assert workflow["programmingLanguage"].id == GALAXY_ID
    sel = [_ for _ in crate.contextual_entities if "OrganizeAction" in _.type]
    assert len(sel) == 1
    engine_action = sel[0]
    assert "SoftwareApplication" in engine_action["instrument"].type
    actions = [_ for _ in crate.contextual_entities if "CreateAction" in _.type]
    sel = [_ for _ in actions if _["instrument"] is workflow]
    assert len(sel) == 1
    wf_action = sel[0]
    assert crate.root_dataset["mentions"] == [wf_action]
    assert engine_action["result"] is wf_action
    control_actions = engine_action["object"]
    assert all(_.type == "ControlAction" for _ in control_actions)
