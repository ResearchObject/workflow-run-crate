{
    "$graph": [
        {
            "class": "Workflow",
            "id": "#main",
            "label": "cosifer-workflow",
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/data_matrix"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "id": "#main/gmt_filepath"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "id": "#main/index_col"
                },
                {
                    "type": "string",
                    "id": "#main/outdir"
                },
                {
                    "type": [
                        "null",
                        "boolean"
                    ],
                    "id": "#main/samples_on_rows"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "id": "#main/separator"
                }
            ],
            "steps": [
                {
                    "run": "#cosifer.cwl",
                    "in": [
                        {
                            "source": "#main/data_matrix",
                            "id": "#main/cosifer/data_matrix"
                        },
                        {
                            "source": "#main/gmt_filepath",
                            "id": "#main/cosifer/gmt_filepath"
                        },
                        {
                            "source": "#main/index_col",
                            "id": "#main/cosifer/index_col"
                        },
                        {
                            "source": "#main/outdir",
                            "id": "#main/cosifer/outdir"
                        },
                        {
                            "source": "#main/samples_on_rows",
                            "id": "#main/cosifer/samples_on_rows"
                        },
                        {
                            "source": "#main/separator",
                            "id": "#main/cosifer/separator"
                        }
                    ],
                    "out": [
                        "#main/cosifer/resdir"
                    ],
                    "id": "#main/cosifer"
                }
            ],
            "outputs": [
                {
                    "type": "Directory",
                    "outputSource": "#main/cosifer/resdir",
                    "id": "#main/resdir"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#cosifer.cwl",
            "label": "cosifer",
            "requirements": [
                {
                    "dockerPull": "tsenit/cosifer:b4d5af45d2fc54b6bff2a9153a8e9054e560302e",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "cosifer"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-i"
                    },
                    "id": "#cosifer.cwl/cosifer/data_matrix"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--gmt_filepath"
                    },
                    "id": "#cosifer.cwl/cosifer/gmt_filepath"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "inputBinding": {
                        "position": 3,
                        "prefix": "--index"
                    },
                    "id": "#cosifer.cwl/cosifer/index_col"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "position": 5,
                        "prefix": "-o"
                    },
                    "id": "#cosifer.cwl/cosifer/outdir"
                },
                {
                    "type": [
                        "null",
                        "boolean"
                    ],
                    "inputBinding": {
                        "position": 6,
                        "prefix": "--samples_on_rows"
                    },
                    "id": "#cosifer.cwl/cosifer/samples_on_rows"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "position": 2,
                        "prefix": "--sep=",
                        "separate": false
                    },
                    "id": "#cosifer.cwl/cosifer/separator"
                }
            ],
            "outputs": [
                {
                    "type": "Directory",
                    "outputBinding": {
                        "glob": "*"
                    },
                    "id": "#cosifer.cwl/cosifer/resdir"
                }
            ]
        }
    ],
    "cwlVersion": "v1.0"
}
