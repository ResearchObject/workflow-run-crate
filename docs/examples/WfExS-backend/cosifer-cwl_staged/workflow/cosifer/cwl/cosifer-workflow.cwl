class: Workflow
cwlVersion: v1.0
id: cosifer_workflow
label: cosifer-workflow

inputs:
  data_matrix: {type: File}
  gmt_filepath: {type: "File?"}
  index_col: {type: "int?"}
  outdir: {type: string}
  separator: {type: "string?"}
  samples_on_rows: {type: "boolean?"}

outputs:
  resdir: {type: Directory, outputSource: cosifer/resdir}

steps:
  cosifer:
    run: ./cosifer.cwl
    in:
      data_matrix: data_matrix
      separator: separator
      index_col: index_col
      gmt_filepath: gmt_filepath
      outdir: outdir
      samples_on_rows: samples_on_rows
    out: [resdir]
