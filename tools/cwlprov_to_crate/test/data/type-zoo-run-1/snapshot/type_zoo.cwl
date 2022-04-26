cwlVersion: v1.0
class: CommandLineTool

baseCommand: echo

stdout: output.txt

inputs:
  in_array:
    type: string[]
    inputBinding:
      position: 1
  in_any:
    type: Any
    inputBinding:
      prefix: --in-any
  in_str:
    type: string
    inputBinding:
      prefix: --in-str
  in_bool:
    type: boolean
    inputBinding:
      prefix: --in-bool
  in_int:
    type: int
    inputBinding:
      prefix: --in-int
  in_long:
    type: long
    inputBinding:
      prefix: --in-long
  in_float:
    type: float
    inputBinding:
      prefix: --in-float
  in_double:
    type: double
    inputBinding:
      prefix: --in-double
  in_multi:
    type: [int, float, "null"]
    default: 9.99
    inputBinding:
      prefix: --in-multi
  in_enum:
    type:
      type: enum
      symbols: ["A", "B"]
    inputBinding:
      prefix: --in-enum
  in_record:
    type:
      type: record
      name: in_record
      fields:
        in_record_A:
          type: string
          inputBinding:
            prefix: --in-record-A
        in_record_B:
          type: string
          inputBinding:
            prefix: --in-record-B

outputs:
  cl_dump:
    type: stdout
