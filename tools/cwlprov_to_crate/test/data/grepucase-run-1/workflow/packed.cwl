{
    "$graph": [
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "bash",
                "-c"
            ],
            "inputs": [
                {
                    "type": "Directory",
                    "id": "#greptool.cwl/g_in_dir"
                },
                {
                    "type": "string",
                    "id": "#greptool.cwl/g_pattern"
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "valueFrom": "mkdir -p grep_out\nfind $(inputs.g_in_dir.path)/ -type f | while read f; do\n  grep $(inputs.g_pattern) \\${f} > grep_out/`basename \\${f}`.out\ndone\n"
                }
            ],
            "id": "#greptool.cwl",
            "outputs": [
                {
                    "type": "Directory",
                    "outputBinding": {
                        "glob": "grep_out"
                    },
                    "id": "#greptool.cwl/g_out_dir"
                }
            ]
        },
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "Directory",
                    "id": "#main/in_dir"
                },
                {
                    "type": "string",
                    "id": "#main/pattern"
                }
            ],
            "outputs": [
                {
                    "type": "Directory",
                    "outputSource": "#main/ucase/u_out_dir",
                    "id": "#main/out_dir"
                }
            ],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#main/in_dir",
                            "id": "#main/grep/g_in_dir"
                        },
                        {
                            "source": "#main/pattern",
                            "id": "#main/grep/g_pattern"
                        }
                    ],
                    "out": [
                        "#main/grep/g_out_dir"
                    ],
                    "run": "#greptool.cwl",
                    "id": "#main/grep"
                },
                {
                    "in": [
                        {
                            "source": "#main/grep/g_out_dir",
                            "id": "#main/ucase/u_in_dir"
                        }
                    ],
                    "out": [
                        "#main/ucase/u_out_dir"
                    ],
                    "run": "#ucasetool.cwl",
                    "id": "#main/ucase"
                }
            ],
            "id": "#main"
        },
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "bash",
                "-c"
            ],
            "inputs": [
                {
                    "type": "Directory",
                    "id": "#ucasetool.cwl/u_in_dir"
                }
            ],
            "outputs": [
                {
                    "type": "Directory",
                    "outputBinding": {
                        "glob": "ucase_out"
                    },
                    "id": "#ucasetool.cwl/u_out_dir"
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "valueFrom": "mkdir -p ucase_out\nfind $(inputs.u_in_dir.path)/ -type f | while read f; do\n  awk '{print toupper(\\$0)}' < \\${f} > ucase_out/`basename \\${f}`.out\ndone\n"
                }
            ],
            "id": "#ucasetool.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}