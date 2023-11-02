
rule slide_to_ometiff:
    input:
        lambda wildcard: gen_rule_input_path(wildcard)
    output:
        protected("tiffs/{slide}.ome.tiff")
    log:
        "logs/slide_to_ometiff/{slide}.log"
    benchmark:
        "bench/slide_to_ometiff/{slide}.bench"
    params:
        compression = config['output']['compression'],
        quality = config['output']['quality'],
        tile_size = config['output']['tile_size'],
    container:
        "docker://ilveroluca/fair-crcc-vips:0.1.1"
    resources:
        mem_mb = 2000,
    threads:
        2
    shell:
        """
        mkdir -p $(dirname {output:q}) &&
        slide_to_ometiff \
            --compression={params.compression} \
            --quality={params.quality} \
            --tile-size={params.tile_size} \
            {input:q} {output:q} &> {log:q}
        """


rule slide_to_thumbnail:
    input:
        lambda wildcard: gen_rule_input_path(wildcard)
    output:
        protected("tiffs/{slide}_thumb.jpg")
    log:
        "logs/slide_to_thumbnail/{slide}_thumb.log"
    benchmark:
        "bench/slide_to_thumbnail/{slide}_thumb.bench"
    params:
        width = config['output']['thumbnail_width']
    container:
        "docker://ilveroluca/fair-crcc-vips:0.1.1"
    resources:
        mem_mb = 2000,
    threads:
        1
    shell:
        """
        mkdir -p $(dirname {output:q}) &&
        slide_to_thumbnail \
            --width {params.width} \
            {input:q} {output:q} &> {log:q}
        """
