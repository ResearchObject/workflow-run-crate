#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

baseCommand: echo

arguments:
- $(inputs.input_file.path)
- $(inputs.input_dir.path)

inputs:
  input_file: File
  input_dir: Directory

outputs: []



