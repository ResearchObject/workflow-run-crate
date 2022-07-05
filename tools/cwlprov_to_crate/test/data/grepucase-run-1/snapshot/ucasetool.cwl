class: CommandLineTool
cwlVersion: v1.0

baseCommand: ["bash", "-c"]

inputs:
  u_in_dir:
    type: Directory
outputs:
  u_out_dir:
    type: Directory
    outputBinding:
      glob: ucase_out

arguments:
  - position: 0
    valueFrom: |
      mkdir -p ucase_out
      find $(inputs.u_in_dir.path)/ -type f | while read f; do
        awk '{print toupper(\$0)}' < \${f} > ucase_out/`basename \${f}`.out
      done
