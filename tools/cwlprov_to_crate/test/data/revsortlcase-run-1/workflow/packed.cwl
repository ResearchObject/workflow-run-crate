{
    "$graph": [
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "awk",
                "{print tolower($0)}"
            ],
            "inputs": [
                {
                    "type": "File",
                    "id": "#lcasetool.cwl/lcase_in"
                }
            ],
            "stdout": "lcase_out.txt",
            "id": "#lcasetool.cwl",
            "stdin": "$(inputs.lcase_in.path)",
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "lcase_out.txt"
                    },
                    "id": "#lcasetool.cwl/lcase_out"
                }
            ]
        },
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "boolean",
                    "default": false,
                    "id": "#revsort.cwl/reverse_sort"
                },
                {
                    "type": "File",
                    "id": "#revsort.cwl/revsort_in"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#revsort.cwl/sorted/sort_out",
                    "id": "#revsort.cwl/revsort_out"
                }
            ],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#revsort.cwl/revsort_in",
                            "id": "#revsort.cwl/rev/rev_in"
                        }
                    ],
                    "out": [
                        "#revsort.cwl/rev/rev_out"
                    ],
                    "run": "#revtool.cwl",
                    "id": "#revsort.cwl/rev"
                },
                {
                    "in": [
                        {
                            "source": "#revsort.cwl/reverse_sort",
                            "id": "#revsort.cwl/sorted/reverse"
                        },
                        {
                            "source": "#revsort.cwl/rev/rev_out",
                            "id": "#revsort.cwl/sorted/sort_in"
                        }
                    ],
                    "out": [
                        "#revsort.cwl/sorted/sort_out"
                    ],
                    "run": "#sorttool.cwl",
                    "id": "#revsort.cwl/sorted"
                }
            ],
            "id": "#revsort.cwl"
        },
        {
            "class": "Workflow",
            "requirements": [
                {
                    "class": "SubworkflowFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": "boolean",
                    "default": false,
                    "id": "#main/descending_sort"
                },
                {
                    "type": "File",
                    "id": "#main/revsortlcase_in"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/lcase/lcase_out",
                    "id": "#main/revsortlcase_out"
                }
            ],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#main/revsort/revsort_out",
                            "id": "#main/lcase/lcase_in"
                        }
                    ],
                    "out": [
                        "#main/lcase/lcase_out"
                    ],
                    "run": "#lcasetool.cwl",
                    "id": "#main/lcase"
                },
                {
                    "in": [
                        {
                            "source": "#main/descending_sort",
                            "id": "#main/revsort/reverse_sort"
                        },
                        {
                            "source": "#main/revsortlcase_in",
                            "id": "#main/revsort/revsort_in"
                        }
                    ],
                    "out": [
                        "#main/revsort/revsort_out"
                    ],
                    "run": "#revsort.cwl",
                    "id": "#main/revsort"
                }
            ],
            "id": "#main"
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