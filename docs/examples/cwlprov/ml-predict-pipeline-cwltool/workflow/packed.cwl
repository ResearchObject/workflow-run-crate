{
    "$graph": [
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "dockerPull": "crs4/slaid:1.1.0-beta.25-tumor_model-level_1-v2.2-cudnn",
                    "class": "DockerRequirement"
                },
                {
                    "listing": [
                        "$(inputs.src)"
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#classify_tumor.cwl/batch-size"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#classify_tumor.cwl/chunk-size"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "prefix": "-F"
                    },
                    "id": "#classify_tumor.cwl/filter"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "prefix": "--filter-slide"
                    },
                    "id": "#classify_tumor.cwl/filter_slide"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "inputBinding": {
                        "prefix": "--gpu"
                    },
                    "id": "#classify_tumor.cwl/gpu"
                },
                {
                    "type": "string",
                    "inputBinding": {
                        "prefix": "-L"
                    },
                    "id": "#classify_tumor.cwl/label"
                },
                {
                    "type": "int",
                    "inputBinding": {
                        "prefix": "-l"
                    },
                    "id": "#classify_tumor.cwl/level"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "secondaryFiles": [
                        {
                            "pattern": "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"Directory\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n    basename: self.nameroot};\n  }\n  else return null;\n}",
                            "required": false
                        }
                    ],
                    "id": "#classify_tumor.cwl/src"
                }
            ],
            "arguments": [
                "fixed-batch",
                "-o",
                "$(runtime.outdir)",
                "--writer",
                "zip"
            ],
            "id": "#classify_tumor.cwl",
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "$(inputs.src.basename).zip",
                        "outputEval": "${self[0].basename=inputs.label + '.zip'; return self[0];}"
                    },
                    "id": "#classify_tumor.cwl/tumor"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "dockerPull": "crs4/slaid:1.1.0-beta.25-tissue_model-eddl_2-cudnn",
                    "class": "DockerRequirement"
                },
                {
                    "listing": [
                        "$(inputs.src)"
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#extract_tissue.cwl/batch-size"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#extract_tissue.cwl/chunk-size"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "prefix": "-F"
                    },
                    "id": "#extract_tissue.cwl/filter"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "prefix": "--filter-slide"
                    },
                    "id": "#extract_tissue.cwl/filter_slide"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "inputBinding": {
                        "prefix": "--gpu"
                    },
                    "id": "#extract_tissue.cwl/gpu"
                },
                {
                    "type": "string",
                    "inputBinding": {
                        "prefix": "-L"
                    },
                    "id": "#extract_tissue.cwl/label"
                },
                {
                    "type": "int",
                    "inputBinding": {
                        "prefix": "-l"
                    },
                    "id": "#extract_tissue.cwl/level"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "secondaryFiles": [
                        {
                            "pattern": "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"Directory\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n    basename: self.nameroot};\n  }\n  else return null;\n}",
                            "required": false
                        }
                    ],
                    "id": "#extract_tissue.cwl/src"
                }
            ],
            "arguments": [
                "fixed-batch",
                "-o",
                "$(runtime.outdir)",
                "--writer",
                "zip"
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "$(inputs.src.basename).zip",
                        "outputEval": "${self[0].basename=inputs.label + '.zip'; return self[0];}"
                    },
                    "id": "#extract_tissue.cwl/tissue"
                }
            ],
            "id": "#extract_tissue.cwl"
        },
        {
            "class": "Workflow",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/gpu"
                },
                {
                    "type": "File",
                    "secondaryFiles": [
                        {
                            "pattern": "${\n  if (self.nameext == '.mrxs') {\n    return {\n    class: \"Directory\",\n    location: self.location.match(/.*\\//)[0] + \"/\" + self.nameroot,\n    basename: self.nameroot};\n  }\n  else return null;\n}",
                            "required": false
                        }
                    ],
                    "id": "#main/slide"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tissue-high-batch-size"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tissue-high-chunk-size"
                },
                {
                    "type": "string",
                    "id": "#main/tissue-high-filter"
                },
                {
                    "type": "string",
                    "id": "#main/tissue-high-label"
                },
                {
                    "type": "int",
                    "id": "#main/tissue-high-level"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tissue-low-batch-size"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tissue-low-chunk-size"
                },
                {
                    "type": "string",
                    "id": "#main/tissue-low-label"
                },
                {
                    "type": "int",
                    "id": "#main/tissue-low-level"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tumor-batch-size"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/tumor-chunk-size"
                },
                {
                    "type": "string",
                    "id": "#main/tumor-filter"
                },
                {
                    "type": "string",
                    "id": "#main/tumor-label"
                },
                {
                    "type": "int",
                    "id": "#main/tumor-level"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/extract-tissue-high/tissue",
                    "id": "#main/tissue"
                },
                {
                    "type": "File",
                    "outputSource": "#main/classify-tumor/tumor",
                    "id": "#main/tumor"
                }
            ],
            "steps": [
                {
                    "run": "#classify_tumor.cwl",
                    "in": [
                        {
                            "source": "#main/tumor-batch-size",
                            "id": "#main/classify-tumor/batch-size"
                        },
                        {
                            "source": "#main/tumor-chunk-size",
                            "id": "#main/classify-tumor/chunk-size"
                        },
                        {
                            "source": "#main/tumor-filter",
                            "id": "#main/classify-tumor/filter"
                        },
                        {
                            "source": "#main/extract-tissue-low/tissue",
                            "id": "#main/classify-tumor/filter_slide"
                        },
                        {
                            "source": "#main/gpu",
                            "id": "#main/classify-tumor/gpu"
                        },
                        {
                            "source": "#main/tumor-label",
                            "id": "#main/classify-tumor/label"
                        },
                        {
                            "source": "#main/tumor-level",
                            "id": "#main/classify-tumor/level"
                        },
                        {
                            "source": "#main/slide",
                            "id": "#main/classify-tumor/src"
                        }
                    ],
                    "out": [
                        "#main/classify-tumor/tumor"
                    ],
                    "id": "#main/classify-tumor"
                },
                {
                    "run": "#extract_tissue.cwl",
                    "in": [
                        {
                            "source": "#main/tissue-high-batch-size",
                            "id": "#main/extract-tissue-high/batch-size"
                        },
                        {
                            "source": "#main/tissue-high-chunk-size",
                            "id": "#main/extract-tissue-high/chunk-size"
                        },
                        {
                            "source": "#main/tissue-high-filter",
                            "id": "#main/extract-tissue-high/filter"
                        },
                        {
                            "source": "#main/extract-tissue-low/tissue",
                            "id": "#main/extract-tissue-high/filter_slide"
                        },
                        {
                            "source": "#main/gpu",
                            "id": "#main/extract-tissue-high/gpu"
                        },
                        {
                            "source": "#main/tissue-high-label",
                            "id": "#main/extract-tissue-high/label"
                        },
                        {
                            "source": "#main/tissue-high-level",
                            "id": "#main/extract-tissue-high/level"
                        },
                        {
                            "source": "#main/slide",
                            "id": "#main/extract-tissue-high/src"
                        }
                    ],
                    "out": [
                        "#main/extract-tissue-high/tissue"
                    ],
                    "id": "#main/extract-tissue-high"
                },
                {
                    "run": "#extract_tissue.cwl",
                    "in": [
                        {
                            "source": "#main/tissue-low-batch-size",
                            "id": "#main/extract-tissue-low/batch-size"
                        },
                        {
                            "source": "#main/tissue-low-chunk-size",
                            "id": "#main/extract-tissue-low/chunk-size"
                        },
                        {
                            "source": "#main/gpu",
                            "id": "#main/extract-tissue-low/gpu"
                        },
                        {
                            "source": "#main/tissue-low-label",
                            "id": "#main/extract-tissue-low/label"
                        },
                        {
                            "source": "#main/tissue-low-level",
                            "id": "#main/extract-tissue-low/level"
                        },
                        {
                            "source": "#main/slide",
                            "id": "#main/extract-tissue-low/src"
                        }
                    ],
                    "out": [
                        "#main/extract-tissue-low/tissue"
                    ],
                    "id": "#main/extract-tissue-low"
                }
            ],
            "id": "#main"
        }
    ],
    "cwlVersion": "v1.1"
}