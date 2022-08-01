cwlVersion: v1.0
class: Workflow
requirements:
  ScatterFeatureRequirement: {}
inputs:
  messages: string[] 
steps:
  echo:
    run: echo.cwl
    scatter: msg
    in:
      msg: messages
    out: []
outputs: []
