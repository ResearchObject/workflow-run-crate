class: Workflow
doc: Test workflow with a collection
label: collection_workflow
cwlVersion: v1.2
inputs:
  input collection 1:
    doc: collection 1
    id: input collection 1
    type: File[]
  input collection 2:
    doc: collection 2
    id: input collection 2
    type: File[]
  num_lines_param:
    doc: number of lines to select
    id: num_lines_param
    type: int
outputs:
  _anonymous_output_1:
    outputSource: num_lines_param
    type: File
  output_collection:
    outputSource: merge collections tool
    type: File
  concatenated_collection:
    outputSource: concat collection/out_file1
    type: File
  output:
    outputSource: select lines/out_file1
    type: File
steps:
  merge collections tool:
    doc: merged collections
    run:
      class: Operation
      doc: merged collections
      inputs: {}
      outputs: {}
    in:
      inputs_0|input:
        source: input collection 1
      inputs_1|input:
        source: input collection 2
    out: []
  concat collection:
    doc: concatenate collection
    run:
      class: Operation
      doc: concatenate collection
      inputs: {}
      outputs: {}
    in:
      input1:
        source: merge collections tool
    out:
    - out_file1
  select lines:
    doc: select 3 lines
    run:
      class: Operation
      doc: select 3 lines
      inputs: {}
      outputs: {}
    in:
      lineNum:
        source: num_lines_param
      input:
        source: concat collection/out_file1
    out:
    - out_file1
