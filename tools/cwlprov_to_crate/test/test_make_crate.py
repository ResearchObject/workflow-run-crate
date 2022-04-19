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
    for a in actions:
        if a is wf_action:
            continue
        instrument = a["instrument"]
        assert instrument in tools
        if instrument.id.endswith("rev"):
            objects = a["object"]
            results = a["result"]
            assert len(objects) == 1
            assert len(results) == 1
            rev_input_file = objects[0]
            assert rev_input_file is wf_input_file
            rev_output_file = results[0]
            assert "File" in rev_output_file.type
        elif instrument.id.endswith("sorted"):
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
            assert False, f"unexpected instrument for action {a.id}"
