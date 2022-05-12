cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ echo, '-n', '{"answer": 42}' ]
stdout: cwl.output.json
inputs: []
outputs:
  answer: int
