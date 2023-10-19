# Copyright 2022-2023 CRS4.
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
Replace copies of the Mirax2-Fluorescence-2 files with symlinks.

This is specific to CWLProv RO-Bundles and Workflow Run RO-Crates that store
files using their sha1 checksum as their name.
"""

from pathlib import Path
import argparse
import hashlib
import os


THIS_DIR = Path(__file__).absolute().parent


def sha1sum(path):
    m = hashlib.sha1()
    with open(path, "rb") as f:
        m.update(f.read())
    return m.hexdigest()


def map_sums_to_paths():
    root_dir = THIS_DIR / "Mirax2-Fluorescence-2"
    sub_dir = root_dir / "Mirax2-Fluorescence-2"
    rval = {}
    main_file = root_dir / "Mirax2-Fluorescence-2.mrxs"
    rval[sha1sum(main_file)] = main_file
    for entry in os.scandir(sub_dir):
        rval[sha1sum(entry.path)] = Path(entry.path)
    return rval


def main(args):
    args.root = Path(args.root).resolve()
    sum_to_path = map_sums_to_paths()
    for root, dirs, files in os.walk(args.root):
        root = Path(root)
        for name in files:
            try:
                orig_path = sum_to_path[name]
            except KeyError:
                continue
            path = root / name
            assert name == sha1sum(path)
            link_target = os.path.relpath(orig_path, root)
            print(f"{path} => {link_target}")
            path.unlink()
            path.symlink_to(link_target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("root", metavar="ROOT DIRECTORY",
                        help="where to search for files to replace with links")
    main(parser.parse_args())
