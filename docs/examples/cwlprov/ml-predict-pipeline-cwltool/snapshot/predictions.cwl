cwlVersion: v1.1
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  slide:
    type: File
    secondaryFiles:
      - pattern: |-
          ${
            if (self.nameext == '.mrxs') {
              return {
              class: "Directory",
              location: self.location.match(/.*\//)[0] + "/" + self.nameroot,
              basename: self.nameroot};
            }
            else return null;
          }
        required: false
  tissue-low-level: int
  tissue-low-label: string
  tissue-low-chunk-size: int?
  tissue-low-batch-size: int?

  tissue-high-level: int
  tissue-high-label: string
  tissue-high-filter: string
  tissue-high-chunk-size: int?
  tissue-high-batch-size: int?

  tumor-chunk-size: int?
  tumor-level: int
  tumor-label: string
  tumor-filter: string
  tumor-batch-size: int?

  gpu: int?

outputs:
  tissue:
    type: File
    outputSource: extract-tissue-high/tissue
  tumor:
    type: File
    outputSource: classify-tumor/tumor

steps:
  extract-tissue-low:
    run: extract_tissue.cwl
    in:
      src: slide
      level: tissue-low-level
      label: tissue-low-label
      gpu: gpu
      chunk-size: tissue-low-chunk-size
      batch-size: tissue-low-batch-size
    out: [tissue]

  extract-tissue-high:
    run: extract_tissue.cwl
    in:
      src: slide
      level: tissue-high-level
      label: tissue-high-label
      filter_slide: extract-tissue-low/tissue
      filter: tissue-high-filter
      gpu: gpu
      chunk-size: tissue-high-chunk-size
      batch-size: tissue-high-batch-size
    out: [tissue]

  classify-tumor:
    run: classify_tumor.cwl
    in:
      src: slide
      level: tumor-level
      label: tumor-label
      filter_slide: extract-tissue-low/tissue
      filter: tumor-filter
      gpu: gpu
      chunk-size: tumor-chunk-size
      batch-size: tumor-batch-size
    out:
      [tumor]
