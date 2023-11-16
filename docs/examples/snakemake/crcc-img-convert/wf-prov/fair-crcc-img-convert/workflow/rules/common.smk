
import os
import sys

from pathlib import Path
from typing import Iterable, Union

from snakemake.utils import validate


#### Constants ####
Extensions = ('.mrxs', '.svs', '.ndpi')


#### Configuration ####
validate(config, schema="../schemas/config.schema.yml")  # also sets default values


##### Helper functions #########

def log(*args) -> None:
    print(*args, file=sys.stderr)


def get_repository_path() -> Path:
    return Path(config['repository']['path']).resolve()


def glob_source_paths() -> Iterable[Path]:
    base_dir = get_repository_path()
    source_paths = [ Path(p) for p in config['sources']['items'] ]
    if any(p.is_absolute() for p in source_paths):
        raise ValueError("Source paths must be relative to repository.path (absolute paths found).")
    # glob any directories for files that end with any of the Extensions
    try:
        cwd = Path.cwd()
        os.chdir(base_dir)
        # We glob with os.walk rather than Path.rglob to catch any of the supported
        # in a single directory traversal (with rglob we can only scan for one extension)
        source_files = \
            [ Path(root, slide)
                for p in source_paths if p.is_dir()
                for root, _, files in os.walk(p)
                for slide in files if any(slide.endswith(ext) for ext in Extensions) ] + \
            [ Path(p) for p in source_paths if p.is_file() and any(p.suffix == ext for ext in Extensions) ]
    finally:
        os.chdir(cwd)
    return source_files


###### Input functions ######
def gen_rule_input_path(wildcard):
    """
    Given the wildcard, tries all Extensions until it
    finds one that matches a file name in the repository.
    """
    for suffix in Extensions:
        path = get_repository_path() / f"{wildcard.slide}{suffix}"
        if path.exists():
            return path
    return ''


###### Environment configuration functions ######
def configure_environment():
    shell.prefix("set -o pipefail; ")

    if workflow.use_singularity:
        # Bind mount the repository path into container.
        # Ideally we want to mount the repository in read-only mode.
        # To avoid making the working directory read-only should it be inside
        # or the same path as the working directory, we check for this case
        # and if true we mount read-write.
        repository = Path(config['repository']['path']).resolve()
        work_dir = Path.cwd()
        if repository == work_dir or repository in work_dir.parents:
            mount_options = 'rw'
        else:
            mount_options = 'ro'
        workflow.singularity_args += ' '.join([
            # Use --cleanenv to work around singularity exec overriding env
            # vars from docker image with host values (https://github.com/sylabs/singularity/issues/533)
            " --cleanenv",
            f" --bind {repository}:{repository}:{mount_options}"])
