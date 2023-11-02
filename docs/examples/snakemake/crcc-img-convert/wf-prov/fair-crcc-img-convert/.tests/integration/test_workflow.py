

import logging
import os
import shutil
import subprocess
import sys
import tempfile
import yaml

from pathlib import Path
from typing import Any, Iterable, Mapping
from zipfile import ZipFile


_logger = logging.getLogger(__file__)


def extract_mirax(repository: Path, archive: Path) -> Path:
    """
    Returns the path to the .mrxs file that was unzipped.
    """
    with ZipFile(archive) as f:
        f.extractall(path=repository)
    try:
        mirax_path = next(p for p in Path(repository).rglob("*.mrxs"))
        _logger.info("Extracted mirax slide %s", mirax_path)
        return mirax_path
    except StopIteration:
        raise RuntimeError(f".mrxs file is missing from archive at {archive}")


def create_config(repository_path: Path, *image_paths: Iterable[Path]) -> Mapping[str, Any]:
    config = {
        'repository': { 'path': str(repository_path) },
        'sources': { 'items': [ str(p.resolve().relative_to(repository_path)) for p in image_paths ] },
        'keypair': { 'private': 'repo.sec',
                     'public': 'repo.pub' },
        'output': {
            'format': 'ome-tiff',
            'compression': "jpeg",
            'quality': 90,
            'tile_size': 512,
            'thumbnail_width': 2048,
        }
    }
    return config


def get_repo_path() -> Path:
    return Path(*Path(__file__).parts[0:-3])


def get_workflow_path() -> Path:
    # compute the repository dir by taking .tests/integration/test_workflow.py
    # off the __file__ path.
    root_dir = get_repo_path()
    workflow_path = root_dir / 'workflow' / 'Snakefile'
    return workflow_path


def setup_working_dir(scratch_path: Path, cfg: Mapping[str, Any]) -> None:
    with open(scratch_path / 'config.yml', 'w') as cfg_file:
        cfg_text = yaml.dump(cfg)
        cfg_file.write(cfg_text)
        _logger.debug("Workflow run configuration:\n%s", cfg_text)
    keys = [Path(get_repo_path(), '.tests', 'data', filename)
            for filename in ('repo.sec', 'repo.pub')]
    for key in keys:
        shutil.copy2(key, Path(scratch_path, key.name))


def print_log_files(base_dir: Path, fp) -> None:
    log_files = (Path(root, f) for root, _, files in os.walk(base_dir)
                 for f in files if f.endswith('.log'))
    for log in log_files:
        with open(log) as f:
            fp.write(f"Filename: {log}\n")
            fp.write(f.read())
            fp.write(40 * '=+' + '\n\n')


def test_workflow(empty_repository, mirax_1_zip):
    mrxs_file = extract_mirax(empty_repository, mirax_1_zip)
    cfg = create_config(empty_repository, mrxs_file)
    with tempfile.TemporaryDirectory() as scratch_dir:
        scratch_path = Path(scratch_dir)
        setup_working_dir(scratch_path, cfg)

        snakemake_exec = next(Path(p, 'snakemake')
                              for p in os.get_exec_path()
                              if Path(p, 'snakemake').exists())
        snakemake_cmd = [
            snakemake_exec,
            '--configfile', 'config.yml',
            '--snakefile', get_workflow_path().resolve(),
            '--use-singularity', '--verbose', '--cores', 'all',
            'all_encrypted_tiffs']
        try:
            subprocess.check_output(snakemake_cmd, cwd=scratch_path)
        except subprocess.CalledProcessError:
            print_log_files(scratch_path, sys.stderr)
            raise

        tiff_files = list((scratch_path / 'tiffs').rglob('*.tiff'))
        assert len(tiff_files) == 1
        thumbnail_files = list((scratch_path / 'tiffs').rglob('*_thumb.jpg'))
        assert len(thumbnail_files) == 1
        c4gh_files = list((scratch_path / 'c4gh').rglob('*.c4gh'))
        assert len(c4gh_files) == 2
        tiff_checksums = scratch_path / 'tiffs' / 'tiff_checksums'
        assert tiff_checksums.exists()
        with open(tiff_checksums) as f:
            assert len(list(line for line in f)) == 1
