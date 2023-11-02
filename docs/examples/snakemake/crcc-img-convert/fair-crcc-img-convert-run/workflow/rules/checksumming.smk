
rule compute_file_checksum:
    input:
        tiff = "tiffs/{slide}.tiff"
    output:
        chksum = "tiffs/{slide}.tiff.sha"
    log:
        "logs/compute_file_checksum/{slide}.tiff.sha.log"
    benchmark:
        "bench/compute_file_checksum/{slide}.tiff.sha.bench"
    params:
        checksum_alg = 256
    resources:
        mem_mb = 64
    shell:
        """
        sha{params.checksum_alg}sum {input:q} > {output:q} 2> {log:q}
        """

