class: Workflow
cwlVersion: v1.0

requirements:
  SubworkflowFeatureRequirement: {}

inputs:
  revsortlcase_in:
    type: File
  descending_sort:
    type: boolean
    default: false
outputs:
  revsortlcase_out:
    type: File
    outputSource: lcase/lcase_out

steps:
  revsort:
    in:
      revsort_in: revsortlcase_in
      reverse_sort: descending_sort
    out: [revsort_out]
    run: revsort.cwl
  lcase:
    in:
      lcase_in: revsort/revsort_out
    out: [lcase_out]
    run: lcasetool.cwl
