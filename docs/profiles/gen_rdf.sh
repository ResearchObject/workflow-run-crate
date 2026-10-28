#!/usr/bin/env bash

set -euo pipefail

for v in 0.5 0.6; do
    for p in process workflow provenance; do
	pushd ${v}/${p}_run_crate
	docker run --rm -v $(pwd):/data stain/jena riot --formatted=nt /data/ro-crate-metadata.jsonld > ro-crate-metadata.nt
	docker run --rm -v $(pwd):/data stain/jena riot --formatted=ttl /data/ro-crate-metadata.jsonld > ro-crate-metadata.ttl
	docker run --rm -v $(pwd):/data stain/jena riot --formatted="RDF/XML" /data/ro-crate-metadata.jsonld > ro-crate-metadata.rdf
	popd
    done
done
