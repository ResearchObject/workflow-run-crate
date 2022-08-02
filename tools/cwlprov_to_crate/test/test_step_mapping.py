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

from cwlprov_to_crate import get_workflow, ProvCrateBuilder


def test_step_maps(data_dir):
    wf_basename = "exome-alignment-packed.cwl"
    wf_path = data_dir / wf_basename
    cwl_defs = get_workflow(wf_path)
    step_maps = ProvCrateBuilder._get_step_maps(cwl_defs)
    assert set(step_maps) == {wf_basename}
    sm = step_maps[wf_basename]
    assert len(sm) == 8
    assert sm["main/bwa_index"]["tool"] == "bwa-index.cwl"
    assert sm["main/bwa_mem"]["tool"] == "bwa-mem.cwl"
    assert sm["main/cutadapt"]["tool"] == "cutadapt.cwl"
    assert sm["main/gunzip"]["tool"] == "gunzip.cwl"
    assert sm["main/picard_dictionary"]["tool"] == "picard_dictionary.cwl"
    assert sm["main/picard_markduplicates"]["tool"] == "picard_markduplicates.cwl"
    assert sm["main/samtools_faidx"]["tool"] == "samtools_faidx.cwl"
    assert sm["main/samtools_sort"]["tool"] == "samtools_sort.cwl"
    assert sm["main/cutadapt"]["pos"] < sm["main/bwa_mem"]["pos"]
    for n in "picard_dictionary", "bwa_index", "samtools_faidx":
        assert sm["main/gunzip"]["pos"] < sm[f"main/{n}"]["pos"]
    assert sm["main/bwa_index"]["pos"] < sm["main/bwa_mem"]["pos"]
    assert sm["main/bwa_mem"]["pos"] < sm["main/samtools_sort"]["pos"]
    assert sm["main/samtools_sort"]["pos"] < sm["main/picard_markduplicates"]["pos"]


def test_step_maps_disconnected(data_dir):
    wf_path = data_dir / "no-output-run-1/workflow/packed.cwl"
    cwl_defs = get_workflow(wf_path)
    step_maps = ProvCrateBuilder._get_step_maps(cwl_defs)
    assert set(step_maps) == {"packed.cwl"}
    sm = step_maps["packed.cwl"]
    assert set(sm) == {"main/date_step", "main/echo_step", "main/date2_step"}
    assert sm["main/date_step"]["tool"] == "date.cwl"
    assert sm["main/echo_step"]["tool"] == "echo.cwl"
    assert sm["main/date2_step"]["tool"] == "date.cwl"
