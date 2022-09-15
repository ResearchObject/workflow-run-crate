class: Workflow
cwlVersion: v1.0

inputs:
  in_dir:
    type: Directory
  pattern:
    type: string
outputs:
  out_dir:
    type: Directory
    outputSource: ucase/u_out_dir

steps:
  grep:
    in:
      g_in_dir: in_dir
      g_pattern: pattern
    out: [g_out_dir]
    run: greptool.cwl
  ucase:
    in:
      u_in_dir: grep/g_out_dir
    out: [u_out_dir]
    run: ucasetool.cwl
