# Copyright 2023-2024 CRS4.
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

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path


from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity


THIS_DIR = Path(__file__).absolute().parent
WF_PATH = THIS_DIR / "tutorial.nf"
TRACE_PATH = THIS_DIR / "trace-20230517-52413675.txt"
CONFIG_PATH = THIS_DIR / "nextflow.config"
WROC_PROFILE_VERSION = "1.0"
PROFILES_BASE = "https://w3id.org/ro/wfrun"
PROFILES_VERSION = "0.1"


EXTRA_TERMS = {
    "resourceUsage": "https://w3id.org/ro/terms/workflow-run#resourceUsage",
}
NF_TRACE_NS = "https://w3id.org/ro/terms/nf-trace"


def add_profiles(crate):
    profiles = []
    for p in "process", "workflow", "provenance":
        id_ = f"{PROFILES_BASE}/{p}/{PROFILES_VERSION}"
        profiles.append(crate.add(ContextEntity(crate, id_, properties={
            "@type": "CreativeWork",
            "name": f"{p.title()} Run Crate",
            "version": PROFILES_VERSION,
        })))
    wroc_profile_id = f"https://w3id.org/workflowhub/workflow-ro-crate/{WROC_PROFILE_VERSION}"
    profiles.append(crate.add(ContextEntity(crate, wroc_profile_id, properties={
        "@type": "CreativeWork",
        "name": "Workflow RO-Crate",
        "version": WROC_PROFILE_VERSION,
    })))
    crate.root_dataset["conformsTo"] = profiles


def add_tasks(crate):
    workflow = crate.mainEntity
    with open(TRACE_PATH) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for record in reader:
            action_id = "#" + record["hash"]
            action_name = record["name"]
            tool_name = action_name.split()[0]
            start = datetime.fromtimestamp(float(record["submit"])/1000)
            end = start + timedelta(milliseconds=int(record["duration"]))
            tool_id = f"{workflow.id}#{tool_name}"
            tool = crate.get(tool_id)
            if not tool:
                tool = crate.add(ContextEntity(crate, tool_id, properties={
                    "@type": "SoftwareApplication",
                    "name": tool_name
                }))
                workflow.append_to("hasPart", tool)
            action = crate.add(ContextEntity(crate, action_id, properties={
                "@type": "CreateAction",
                "name": action_name,
            }))
            action["instrument"] = tool
            action["startTime"] = start.isoformat()
            action["endTime"] = end.isoformat()
            resource_usage = []
            stat = "realTime"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["realtime"]),
                    "unitCode": "https://qudt.org/vocab/unit/MilliSEC",
                }))
            )
            stat = "percentCPU"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["%cpu"])
                }))
            )
            stat = "peakRSS"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["peak_rss"]),
                    "unitCode": "https://qudt.org/vocab/unit/BYTE",
                }))
            )
            stat = "peakVMEM"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["peak_vmem"]),
                    "unitCode": "https://qudt.org/vocab/unit/BYTE",
                }))
            )
            stat = "rChar"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["rchar"]),
                    "unitCode": "https://qudt.org/vocab/unit/BYTE",
                }))
            )
            stat = "wChar"
            resource_usage.append(
                crate.add(ContextEntity(crate, f"{action_id}-{stat}", properties={
                    "@type": "PropertyValue",
                    "name": stat,
                    "propertyID": f"{NF_TRACE_NS}#{stat}",
                    "value": str(record["wchar"]),
                    "unitCode": "https://qudt.org/vocab/unit/BYTE",
                }))
            )
            action["resourceUsage"] = resource_usage


def main(args):
    crate = ROCrate(gen_preview=False)
    crate.metadata.extra_terms.update(EXTRA_TERMS)
    crate.root_dataset["license"] = "https://creativecommons.org/licenses/by-sa/4.0/"
    add_profiles(crate)
    wf_properties = {
        "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow", "HowTo"],
    }
    workflow = crate.add_workflow(
        WF_PATH, WF_PATH.name, main=True, lang="nextflow",
        gen_cwl=False, properties=wf_properties
    )
    crate.add_file(CONFIG_PATH, properties={
        "description": "Nextflow configuration file"
    })
    crate.add_file(THIS_DIR / "README.md")
    add_tasks(crate)
    action = crate.add(ContextEntity(crate, properties={
        "@type": "CreateAction",
        "name": f"Execution of {WF_PATH.name}",
    }))
    action["instrument"] = workflow
    crate.root_dataset["mentions"] = [action]
    crate.write(args.out_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir", metavar="OUTPUT_DIRECTORY",
                        help="output directory for the crate")
    main(parser.parse_args())
