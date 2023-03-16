class: CommandLineTool
cwlVersion: v1.0
id: cosifer
label: cosifer

requirements:
  DockerRequirement:
    dockerPull: 'tsenit/cosifer:b4d5af45d2fc54b6bff2a9153a8e9054e560302e'

baseCommand: [cosifer]

inputs:
  data_matrix:
    type: File
    inputBinding:
      position: 1
      prefix: '-i'
  separator:
    type: string?
    inputBinding:
      position: 2
      prefix: '--sep='
      separate: false
  index_col:
    type: int?
    inputBinding:
      position: 3
      prefix: '--index'
  gmt_filepath:
    type: File?
    inputBinding:
      position: 4
      prefix: '--gmt_filepath'
  outdir:
    type: string?
    inputBinding:
      position: 5
      prefix: '-o'
  samples_on_rows:
    type: boolean?
    inputBinding:
      position: 6
      prefix: '--samples_on_rows'

outputs:
  resdir:
    type: Directory
    outputBinding:
      glob: '*'
