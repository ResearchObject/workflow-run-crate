"""\
Generate RO-Crate for the crcc convert run.
"""

import argparse
import os
from pathlib import Path
from rocrate.model import ContextEntity
from rocrate.rocrate import ROCrate

PROFILES_BASE = "https://w3id.org/ro/wfrun"
PROFILES_VERSION = "0.1"
PROCESS_PROFILE_BASE = f"{PROFILES_BASE}/process"
WORKFLOW_PROFILE_BASE = f"{PROFILES_BASE}/workflow"
PROCESS_PROFILE = f"{PROCESS_PROFILE_BASE}/{PROFILES_VERSION}"
WORKFLOW_PROFILE = f"{WORKFLOW_PROFILE_BASE}/{PROFILES_VERSION}"
TERMS_NAMESPACE = "https://w3id.org/ro/terms/workflow-run"
CRATE_LICENSE = "https://creativecommons.org/licenses/by/4.0/"


def add_inputs(crate, action, input_dir):
    action["object"] = [
        crate.add_file(
            input_dir / "Biobank_CMB-PCA_v1/CMB-PCA/MSB-02917-01-02.svs",
            "CMB-PCA/MSB-02917-01-02.svs"
        ),
        crate.add_file(input_dir / "workspace/config.yml", "config.yml"),
        crate.add_file(input_dir / "workspace/user.pub", "user.pub"),
        crate.add_file(input_dir / "workspace/user.sec", "user.sec")
    ]


def add_outputs(crate, action, input_dir):
    result = []
    source_dir = input_dir / "workspace" / "c4gh" / "CMB-PCA"
    dest_dir = "c4gh/CMB-PCA"
    for e in os.scandir(source_dir):
        assert e.is_file()
        source = source_dir / e.name
        dest = f"{dest_dir}/{e.name}"
        result.append(crate.add_file(source, dest))
    action["result"] = result


def main(args):
    args.input = Path(args.input)
    wf_dir = args.input / "fair-crcc-img-convert" / "workflow"
    crate = ROCrate()
    crate.metadata.extra_contexts.append(TERMS_NAMESPACE)
    crate.root_dataset["license"] = CRATE_LICENSE
    workflow = crate.add_workflow(
        wf_dir / "Snakefile", "workflow/Snakefile", main=True,
        lang="snakemake", gen_cwl=False, properties={
            "license": "GPL-3.0"
        }
    )
    crate.add_directory(wf_dir / "rules", "workflow/rules")
    crate.add_directory(wf_dir / "schemas", "workflow/schemas")
    action = crate.add(ContextEntity(crate, properties={
        "@type": "CreateAction",
        "name": "execution of fair-crcc-img-convert workflow",
    }))
    action["instrument"] = workflow
    add_inputs(crate, action, args.input)
    add_outputs(crate, action, args.input)
    crate.root_dataset.append_to("mentions", action)
    crate.write(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input", metavar="input_dir", help="input dir")
    parser.add_argument("-o", "--output", metavar="string",
                        help="output crate dir",
                        default="fair-crcc-img-convert-run")
    main(parser.parse_args())
