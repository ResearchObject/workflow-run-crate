{
    "$graph": [
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "date",
                "-r"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#date.cwl/file"
                }
            ],
            "id": "#date.cwl",
            "outputs": []
        },
        {
            "class": "CommandLineTool",
            "baseCommand": "echo",
            "arguments": [
                "$(inputs.input_file.path)",
                "$(inputs.input_dir.path)"
            ],
            "inputs": [
                {
                    "type": "Directory",
                    "id": "#echo.cwl/input_dir"
                },
                {
                    "type": "File",
                    "id": "#echo.cwl/input_file"
                }
            ],
            "outputs": [],
            "id": "#echo.cwl"
        },
        {
            "class": "Workflow",
            "requirements": [
                {
                    "class": "ScatterFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "id": "#main/pdb_array"
                },
                {
                    "type": "Directory",
                    "id": "#main/pdb_dir"
                },
                {
                    "type": "File",
                    "format": "https://www.iana.org/assignments/media-types/text/tab-separated-values",
                    "id": "#main/sabdab_file"
                }
            ],
            "outputs": [],
            "steps": [
                {
                    "label": "Prints date of input files",
                    "scatter": "#main/date2_step/file",
                    "in": [
                        {
                            "source": "#main/pdb_array",
                            "id": "#main/date2_step/file"
                        }
                    ],
                    "out": [],
                    "run": "#date.cwl",
                    "id": "#main/date2_step"
                },
                {
                    "label": "Prints date of input file",
                    "in": [
                        {
                            "source": "#main/sabdab_file",
                            "id": "#main/date_step/file"
                        }
                    ],
                    "out": [],
                    "run": "#date.cwl",
                    "id": "#main/date_step"
                },
                {
                    "label": "Echo paths of input file & directory",
                    "in": [
                        {
                            "source": "#main/pdb_dir",
                            "id": "#main/echo_step/input_dir"
                        },
                        {
                            "source": "#main/sabdab_file",
                            "id": "#main/echo_step/input_file"
                        }
                    ],
                    "out": [],
                    "run": "#echo.cwl",
                    "id": "#main/echo_step"
                }
            ],
            "id": "#main"
        }
    ],
    "cwlVersion": "v1.2"
}