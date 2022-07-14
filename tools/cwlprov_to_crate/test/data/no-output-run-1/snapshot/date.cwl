#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [date, "-r"]

inputs:
  file: 
    type: File
    inputBinding:
      position: 1

outputs: []



