#!/usr/bin/env bash

set -euo pipefail

die() {
    echo $1 1>&2
    exit 1
}

nargs=1
if [ $# -ne ${nargs} ]; then
    die "Usage: $0 runcrate_repo_dir"
fi
runcrate_repo_dir=$1

this="${BASH_SOURCE-$0}"
this_dir=$(cd -P -- "$(dirname -- "${this}")" && pwd -P)
example_dir="${this_dir}"/../docs/examples/draft

for name in revsort type-zoo; do
    echo ${name}
    echo "  regenerating crate"
    ro="${runcrate_repo_dir}"/tests/data/${name}-run-1
    crate="${example_dir}"/${name}-run-1-crate
    runcrate convert -o "${crate}" -l "Apache-2.0" "${ro}"
    echo "  regenerating preview"
    docker run -u $(id -u):$(id -g) --rm -v "${crate}":/crate simleo/rochtml /crate/ro-crate-metadata.json
done
