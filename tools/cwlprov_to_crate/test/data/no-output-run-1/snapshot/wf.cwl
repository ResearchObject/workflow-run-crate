#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

requirements:
  ScatterFeatureRequirement: {}

inputs:
  sabdab_file: 
    type: File
    format: https://www.iana.org/assignments/media-types/text/tab-separated-values
  pdb_dir: Directory
  pdb_array: File[]

outputs: []

steps:
  date_step:
    label: Prints date of input file
    in:
      file: sabdab_file
    out: []
    run: ./date.cwl
  echo_step:
    label: Echo paths of input file & directory
    in:
      input_file: sabdab_file
      input_dir: pdb_dir
    out: []
    run: ./echo.cwl
  date2_step:
    label: Prints date of input files
    scatter: file
    in:
      file: pdb_array
    out: []
    run: ./date.cwl





