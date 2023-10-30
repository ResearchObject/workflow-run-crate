"""\
Generate RO-Crate for the crcc convert run.
"""

import argparse
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
