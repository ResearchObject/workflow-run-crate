#!/usr/bin/env bash

set -euo pipefail

this="${BASH_SOURCE-$0}"
this_dir=$(cd -P -- "$(dirname -- "${this}")" && pwd -P)
example_dir="${this_dir}"/../docs/examples/draft

for name in revsort type-zoo; do
    echo ${name}
    echo "  regenerating crate"
    ro="${this_dir}"/cwlprov_to_crate/test/data/${name}-run-1
    crate="${example_dir}"/${name}-run-1-crate
    python "${this_dir}"/cwlprov_to_crate/cwlprov_to_crate.py -o "${crate}" "${ro}"
    echo "  regenerating preview"
    docker run -u $(id -u):$(id -g) --rm -v "${crate}":/crate simleo/rochtml /crate/ro-crate-metadata.json
done
