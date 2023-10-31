rule crypt_file:
    input:
        tiff = "tiffs/{slide}"
    output:
        crypt = protected("c4gh/{slide}.c4gh"),
        checksum = "c4gh/{slide}.c4gh.sha"
    log:
        "logs/crypt_file/{slide}.log"
    benchmark:
        "bench/crypt_file/{slide}.bench"
    params:
        checksum_alg = 256,
        private_key = lambda _: config['keypair']['private'],
        public_key = lambda _: config['keypair']['public']
    resources:
        mem_mb = 1024 # guessed and probably overestimated
    container:
        "docker://ilveroluca/crypt4gh:1.5"
    shell:
        """
        mkdir -p $(dirname {output.crypt:q}) $(dirname {output.checksum:q}) &&
        crypt4gh encrypt --sk {params.private_key:q} --recipient_pk {params.public_key:q} < {input.tiff:q} > {output.crypt:q} 2> {log:q} &&
        sha{params.checksum_alg}sum {output.crypt:q} > {output.checksum:q} 2>> {log:q}
        """
