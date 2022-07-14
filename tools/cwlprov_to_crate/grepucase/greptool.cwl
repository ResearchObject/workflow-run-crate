class: CommandLineTool
cwlVersion: v1.0

baseCommand: ["bash", "-c"]

inputs:
  g_in_dir:
    type: Directory
  g_pattern:
    type: string
outputs:
  g_out_dir:
    type: Directory
    outputBinding:
      glob: grep_out

arguments:
  - position: 0
    valueFrom: |
      mkdir -p grep_out
      find $(inputs.g_in_dir.path)/ -type f | while read f; do
        grep $(inputs.g_pattern) \${f} > grep_out/`basename \${f}`.out
      done
