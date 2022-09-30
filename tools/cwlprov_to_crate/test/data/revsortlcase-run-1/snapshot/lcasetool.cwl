class: CommandLineTool
cwlVersion: v1.0

baseCommand: ["awk", "{print tolower($0)}"]

inputs:
  lcase_in:
    type: stdin
outputs:
  lcase_out:
    type: File
    outputBinding:
      glob: lcase_out.txt
stdout: lcase_out.txt
