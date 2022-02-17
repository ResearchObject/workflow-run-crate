class: Workflow
cwlVersion: v1.2
http://commonwl.org/cwltool#original_cwlVersion: v1.1
id: file:///cwl/predictions.cwl
inputs:
- id: file:///cwl/predictions.cwl#gpu
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#mode
  type:
  - 'null'
  - string
- id: file:///cwl/predictions.cwl#slide
  type: File
- id: file:///cwl/predictions.cwl#tissue-high-batch
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tissue-high-chunk
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tissue-high-filter
  type: string
- id: file:///cwl/predictions.cwl#tissue-high-label
  type: string
- id: file:///cwl/predictions.cwl#tissue-high-level
  type: int
- id: file:///cwl/predictions.cwl#tissue-low-batch
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tissue-low-chunk
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tissue-low-label
  type: string
- id: file:///cwl/predictions.cwl#tissue-low-level
  type: int
- id: file:///cwl/predictions.cwl#tumor-batch
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tumor-chunk
  type:
  - 'null'
  - int
- id: file:///cwl/predictions.cwl#tumor-filter
  type: string
- id: file:///cwl/predictions.cwl#tumor-label
  type: string
- id: file:///cwl/predictions.cwl#tumor-level
  type: int
outputs:
- id: file:///cwl/predictions.cwl#tissue
  outputSource: file:///cwl/predictions.cwl#extract-tissue-high/tissue
  type: File
- id: file:///cwl/predictions.cwl#tumor
  outputSource: file:///cwl/predictions.cwl#classify-tumor/tumor
  type: File
steps:
- id: file:///cwl/predictions.cwl#classify-tumor
  in:
  - id: file:///cwl/predictions.cwl#classify-tumor/batch
    source: file:///cwl/predictions.cwl#tumor-batch
  - id: file:///cwl/predictions.cwl#classify-tumor/chunk
    source: file:///cwl/predictions.cwl#tumor-chunk
  - id: file:///cwl/predictions.cwl#classify-tumor/filter
    source: file:///cwl/predictions.cwl#tumor-filter
  - id: file:///cwl/predictions.cwl#classify-tumor/filter_slide
    source: file:///cwl/predictions.cwl#extract-tissue-low/tissue
  - id: file:///cwl/predictions.cwl#classify-tumor/gpu
    source: file:///cwl/predictions.cwl#gpu
  - id: file:///cwl/predictions.cwl#classify-tumor/label
    source: file:///cwl/predictions.cwl#tumor-label
  - id: file:///cwl/predictions.cwl#classify-tumor/level
    source: file:///cwl/predictions.cwl#tumor-level
  - id: file:///cwl/predictions.cwl#classify-tumor/mode
    source: file:///cwl/predictions.cwl#mode
  - id: file:///cwl/predictions.cwl#classify-tumor/src
    source: file:///cwl/predictions.cwl#unzip/mrxs
  out:
  - file:///cwl/predictions.cwl#classify-tumor/tumor
  run:
    arguments:
    - -o
    - $(runtime.outdir)
    - --writer
    - zip
    class: CommandLineTool
    cwlVersion: v1.1
    id: _:5721fb1b-b8d0-418a-a28d-05c75550a565
    inputs:
    - id: file:///cwl/predictions.cwl#classify-tumor/run/batch
      inputBinding:
        prefix: --batch
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#classify-tumor/run/chunk
      inputBinding:
        prefix: --chunk
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#classify-tumor/run/filter
      inputBinding:
        prefix: -F
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#classify-tumor/run/filter_slide
      inputBinding:
        prefix: --filter-slide
      type:
      - 'null'
      - File
    - id: file:///cwl/predictions.cwl#classify-tumor/run/gpu
      inputBinding:
        prefix: --gpu
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#classify-tumor/run/label
      inputBinding:
        prefix: -f
      type: string
    - id: file:///cwl/predictions.cwl#classify-tumor/run/level
      inputBinding:
        prefix: -l
      type: int
    - id: file:///cwl/predictions.cwl#classify-tumor/run/mode
      inputBinding:
        prefix: --mode
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#classify-tumor/run/src
      inputBinding:
        position: 1
      secondaryFiles:
      - pattern: "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"\
          File\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n\
          \    basename: self.nameroot};\n  }\n  else return null;\n}"
        required: false
      type: File
    outputs:
    - id: file:///cwl/predictions.cwl#classify-tumor/run/tumor
      outputBinding:
        glob: $(inputs.src.basename).zip
        outputEval: ${self[0].basename=inputs.label + '.zip'; return self;}
      type: File
    requirements:
    - class: DockerRequirement
      dockerPull: slaid:0.60.4-develop-tumor_model-level_1
    - class: InitialWorkDirRequirement
      listing:
      - $(inputs.src)
    - class: InlineJavascriptRequirement
- id: file:///cwl/predictions.cwl#extract-tissue-high
  in:
  - id: file:///cwl/predictions.cwl#extract-tissue-high/batch
    source: file:///cwl/predictions.cwl#tissue-high-batch
  - id: file:///cwl/predictions.cwl#extract-tissue-high/chunk
    source: file:///cwl/predictions.cwl#tissue-high-chunk
  - id: file:///cwl/predictions.cwl#extract-tissue-high/filter
    source: file:///cwl/predictions.cwl#tissue-high-filter
  - id: file:///cwl/predictions.cwl#extract-tissue-high/filter_slide
    source: file:///cwl/predictions.cwl#extract-tissue-low/tissue
  - id: file:///cwl/predictions.cwl#extract-tissue-high/gpu
    source: file:///cwl/predictions.cwl#gpu
  - id: file:///cwl/predictions.cwl#extract-tissue-high/label
    source: file:///cwl/predictions.cwl#tissue-high-label
  - id: file:///cwl/predictions.cwl#extract-tissue-high/level
    source: file:///cwl/predictions.cwl#tissue-high-level
  - id: file:///cwl/predictions.cwl#extract-tissue-high/mode
    source: file:///cwl/predictions.cwl#mode
  - id: file:///cwl/predictions.cwl#extract-tissue-high/src
    source: file:///cwl/predictions.cwl#unzip/mrxs
  out:
  - file:///cwl/predictions.cwl#extract-tissue-high/tissue
  run:
    arguments:
    - -o
    - $(runtime.outdir)
    - --writer
    - zip
    class: CommandLineTool
    cwlVersion: v1.1
    id: _:94c10448-c2f4-47e1-83ad-0cbd2254349f
    inputs:
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/batch
      inputBinding:
        prefix: --batch
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/chunk
      inputBinding:
        prefix: --chunk
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/filter
      inputBinding:
        prefix: -F
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/filter_slide
      inputBinding:
        prefix: --filter-slide
      type:
      - 'null'
      - File
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/gpu
      inputBinding:
        prefix: --gpu
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/label
      inputBinding:
        prefix: -f
      type: string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/level
      inputBinding:
        prefix: -l
      type: int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/mode
      inputBinding:
        prefix: --mode
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/src
      inputBinding:
        position: 1
      secondaryFiles:
      - pattern: "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"\
          File\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n\
          \    basename: self.nameroot};\n  }\n  else return null;\n}"
        required: false
      type: File
    outputs:
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/tissue
      outputBinding:
        glob: $(inputs.src.basename).zip
        outputEval: ${self[0].basename=inputs.label + '.zip'; return self;}
      type: File
    requirements:
    - class: DockerRequirement
      dockerPull: slaid:0.60.4-develop-tissue_model-extract_tissue_eddl_1.1
    - class: InitialWorkDirRequirement
      listing:
      - $(inputs.src)
    - class: InlineJavascriptRequirement
- id: file:///cwl/predictions.cwl#extract-tissue-low
  in:
  - id: file:///cwl/predictions.cwl#extract-tissue-low/batch
    source: file:///cwl/predictions.cwl#tissue-low-batch
  - id: file:///cwl/predictions.cwl#extract-tissue-low/chunk
    source: file:///cwl/predictions.cwl#tissue-low-chunk
  - id: file:///cwl/predictions.cwl#extract-tissue-low/gpu
    source: file:///cwl/predictions.cwl#gpu
  - id: file:///cwl/predictions.cwl#extract-tissue-low/label
    source: file:///cwl/predictions.cwl#tissue-low-label
  - id: file:///cwl/predictions.cwl#extract-tissue-low/level
    source: file:///cwl/predictions.cwl#tissue-low-level
  - id: file:///cwl/predictions.cwl#extract-tissue-low/mode
    source: file:///cwl/predictions.cwl#mode
  - id: file:///cwl/predictions.cwl#extract-tissue-low/src
    source: file:///cwl/predictions.cwl#unzip/mrxs
  out:
  - file:///cwl/predictions.cwl#extract-tissue-low/tissue
  run:
    arguments:
    - -o
    - $(runtime.outdir)
    - --writer
    - zip
    class: CommandLineTool
    cwlVersion: v1.1
    id: _:94c10448-c2f4-47e1-83ad-0cbd2254349f
    inputs:
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/batch
      inputBinding:
        prefix: --batch
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/chunk
      inputBinding:
        prefix: --chunk
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/filter
      inputBinding:
        prefix: -F
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/filter_slide
      inputBinding:
        prefix: --filter-slide
      type:
      - 'null'
      - File
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/gpu
      inputBinding:
        prefix: --gpu
      type:
      - 'null'
      - int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/label
      inputBinding:
        prefix: -f
      type: string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/level
      inputBinding:
        prefix: -l
      type: int
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/mode
      inputBinding:
        prefix: --mode
      type:
      - 'null'
      - string
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/src
      inputBinding:
        position: 1
      secondaryFiles:
      - pattern: "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"\
          File\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n\
          \    basename: self.nameroot};\n  }\n  else return null;\n}"
        required: false
      type: File
    outputs:
    - id: file:///cwl/predictions.cwl#extract-tissue-high/run/tissue
      outputBinding:
        glob: $(inputs.src.basename).zip
        outputEval: ${self[0].basename=inputs.label + '.zip'; return self;}
      type: File
    requirements:
    - class: DockerRequirement
      dockerPull: slaid:0.60.4-develop-tissue_model-extract_tissue_eddl_1.1
    - class: InitialWorkDirRequirement
      listing:
      - $(inputs.src)
    - class: InlineJavascriptRequirement
- id: file:///cwl/predictions.cwl#unzip
  in:
  - id: file:///cwl/predictions.cwl#unzip/src
    source: file:///cwl/predictions.cwl#slide
  out:
  - file:///cwl/predictions.cwl#unzip/mrxs
  run:
    baseCommand: unzip-slide
    class: CommandLineTool
    id: _:071ede3f-8647-42f4-820e-b69610aebd87
    inputs:
    - id: file:///cwl/predictions.cwl#unzip/run/src
      inputBinding:
        position: 1
      type: File
    outputs:
    - id: file:///cwl/predictions.cwl#unzip/run/mrxs
      outputBinding:
        glob: $(inputs.src.nameroot).*
      secondaryFiles:
      - pattern: "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"\
          Directory\",\n    path: self.nameroot};\n  }\n  else return null;\n}"
        required: false
      type: File
    requirements:
    - class: InitialWorkDirRequirement
      listing:
      - $(inputs.src)
    - class: InlineJavascriptRequirement
