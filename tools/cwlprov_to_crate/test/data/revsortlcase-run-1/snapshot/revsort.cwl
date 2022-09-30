class: Workflow
cwlVersion: v1.0

inputs:
  revsort_in:
    type: File
  reverse_sort:
    type: boolean
    default: false
outputs:
  revsort_out:
    type: File
    outputSource: sorted/sort_out

steps:
  rev:
    in:
      rev_in: revsort_in
    out: [rev_out]
    run: revtool.cwl
  sorted:
    in:
      sort_in: rev/rev_out
      reverse: reverse_sort
    out: [sort_out]
    run: sorttool.cwl
