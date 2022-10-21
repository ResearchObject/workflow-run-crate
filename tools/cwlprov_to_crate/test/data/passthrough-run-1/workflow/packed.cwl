{
    "$graph": [
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/dummy_in"
                },
                {
                    "type": "boolean",
                    "default": false,
                    "id": "#main/reverse_sort"
                },
                {
                    "type": "File",
                    "id": "#main/revsort_in"
                }
            ],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#main/revsort_in",
                            "id": "#main/rev/rev_in"
                        }
                    ],
                    "out": [
                        "#main/rev/rev_out"
                    ],
                    "run": "#revtool.cwl",
                    "id": "#main/rev"
                },
                {
                    "in": [
                        {
                            "source": "#main/reverse_sort",
                            "id": "#main/sorted/reverse"
                        },
                        {
                            "source": "#main/rev/rev_out",
                            "id": "#main/sorted/sort_in"
                        }
                    ],
                    "out": [
                        "#main/sorted/sort_out"
                    ],
                    "run": "#sorttool.cwl",
                    "id": "#main/sorted"
                }
            ],
            "id": "#main",
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/dummy_in",
                    "id": "#main/dummy_out"
                },
                {
                    "type": "File",
                    "outputSource": "#main/sorted/sort_out",
                    "id": "#main/revsort_out"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "baseCommand": "rev",
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {},
                    "id": "#revtool.cwl/rev_in"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "rev_out.txt"
                    },
                    "id": "#revtool.cwl/rev_out"
                }
            ],
            "stdout": "rev_out.txt",
            "id": "#revtool.cwl"
        },
        {
            "class": "CommandLineTool",
            "baseCommand": "sort",
            "inputs": [
                {
                    "type": "boolean",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "--reverse"
                    },
                    "id": "#sorttool.cwl/reverse"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#sorttool.cwl/sort_in"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "sort_out.txt"
                    },
                    "id": "#sorttool.cwl/sort_out"
                }
            ],
            "stdout": "sort_out.txt",
            "id": "#sorttool.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}