#!/usr/bin/env nextflow

data_matrix = file(params.data_matrix)
outdir = file(params.outputsDir)
result = outdir.mkdirs()
println result ? "Created directory $outdir" : "Cannot create output directory: $outdir"

separator = params.sep
index_col = params.index_col
gmt_filepath = file(params.hallmark_gene_sets_file != '' ? params.hallmark_gene_sets_file : '.empty.')
samples_on_rows = params.samples_on_rows

// We are telling we want the result in this specific subdirectory
// of the outdir
// When empty string is no subdir
cosifer_input = Channel.of([data_matrix,outdir,''])
//cosifer_input = Channel.of([data_matrix,outdir,'proc1'])

process cosifer {
    container "tsenit/cosifer:b4d5af45d2fc54b6bff2a9153a8e9054e560302e"

    publishDir "${destdir}", saveAs: { filename -> (destsubdir!='' ? "${destsubdir}/" : '') + filename.minus('resdir/') }

    input:
	tuple matrix, destdir, val(destsubdir) from cosifer_input
	file gmt_filepath
	val separator
	val index_col
	val samples_on_rows

    output:
	path "resdir/**" into cosifer_output

    """
    cosifer -i "${matrix}" "--sep=${separator}" ${index_col!='' ? '--index ' + index_col : ''}  ${gmt_filepath.name != '.empty.' ? '--gmt_filepath ' + gmt_filepath : ''} -o "resdir" ${samples_on_rows ? '--samples_on_rows' : ''}
    """
}

cosifer_output.subscribe{ result -> println "Output:" + result.name }
