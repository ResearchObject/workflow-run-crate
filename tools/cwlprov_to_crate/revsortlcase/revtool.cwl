class: CommandLineTool
cwlVersion: v1.0

baseCommand: rev

inputs:
  rev_in:
    type: File
    inputBinding: {}
outputs:
  rev_out:
    type: File
    outputBinding:
      glob: rev_out.txt
stdout: rev_out.txt
